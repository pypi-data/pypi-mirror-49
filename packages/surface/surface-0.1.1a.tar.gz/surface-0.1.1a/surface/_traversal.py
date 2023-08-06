""" Traverse an API heirarchy """


# TODO: import module by name
# TODO: get its global name, and path
# TODO: cache path names to module name for efficiency

# TODO: walk through everything it exposes at the top level
# TODO: eg: names not starting with underscores
# TODO: or anything in the __all__ variable.

# TODO: create a simplified representation of the signatures found (names and types)

# BONUS: collect type information as part of the signatures
# BONUS: traverse heirarchy for specified types, recursively getting their api
# BONUS: so later a type can be compared by value, not just name

import re
import logging
import os.path
import inspect
import sigtools  # type: ignore
from surface._base import *
from surface._type import get_type, get_type_func
from importlib import import_module

if False:  # type checking
    from typing import List, Set, Any, Iterable

__all__ = ["recurse", "APITraversal"]

LOG = logging.getLogger(__name__)

import_reg = re.compile(r"__init__\.(py[cd]?|so)$")


def recurse(name):  # type: (str) -> List[str]
    """ Given a module path, return paths to its children. """

    stack = [name]
    paths = []

    while stack:
        import_name = stack.pop()
        module = import_module(import_name)
        paths.append(import_name)
        try:
            module_path = module.__file__
        except AttributeError:
            continue

        if not import_reg.search(module_path):
            paths.append(import_name)
            continue

        package = os.path.dirname(module_path)
        submodules = os.listdir(package)
        for submodule in submodules:
            if submodule.startswith("_"):
                pass
            elif submodule.endswith(".py"):
                paths.append("{}.{}".format(import_name, submodule[:-3]))
            elif os.path.isfile(os.path.join(package, submodule, "__init__.py")):
                stack.append("{}.{}".format(import_name, submodule))
    return paths


class APITraversal(object):
    def __init__(self, exclude_modules=False, all_filter=True):
        self.exclude_modules = exclude_modules
        self.all_filter = all_filter

    def traverse(self, obj):  # type: (Any) -> Iterable[Any]
        """ Entry point to generating an API representation. """
        attributes = [
            attr for attr in inspect.getmembers(obj) if self._is_public(attr[0])
        ]
        if self.all_filter:
            # __all__ attribute restricts import with *,
            # and displays what is intended to be public
            whitelist = getattr(obj, "__all__", [])
            if whitelist:
                attributes = [attr for attr in attributes if attr[0] in whitelist]

        # Sort the attributes by name for readability, and diff-ability (is that a word?)
        attributes.sort(key=lambda a: a[0])

        # Walk the surface of the object, and extract the information
        for name, value in attributes:
            if not name:
                continue
            # TODO: How to ensure we find the original classes and methods, and not wrappers?
            # TODO: Handle recursive endless looping traversal.

            try:
                if inspect.ismodule(value):
                    if self.exclude_modules:
                        continue
                    yield self._handle_module(name, value)
                elif inspect.isclass(value):
                    yield self._handle_class(name, value)
                # Python2
                elif inspect.ismethod(value):
                    yield self._handle_method(name, value)
                elif inspect.isfunction(value):
                    # python3
                    if inspect.isclass(obj):
                        yield self._handle_method(name, value)
                    else:
                        yield self._handle_function(name, value)
                elif name != "__init__":
                    yield self._handle_variable(name, value)
            except SyntaxError as err:
                LOG.warn("Failed to parse {} {}.\n{}".format(name, value, err))

    def _handle_function(self, name, value):  # type: (str, Any) -> Func
        sig = sigtools.signature(value)
        param_types, return_type = get_type_func(value)
        return Func(
            name,
            tuple(
                Arg(
                    n,
                    t,
                    self._convert_arg_kind(str(p.kind))
                    | (0 if p.default is sig.empty else DEFAULT),
                )
                for (n, p), t in zip(sig.parameters.items(), param_types)
            ),
            return_type,
        )

    def _handle_method(self, name, value):  # type: (str, Any) -> Func
        sig = sigtools.signature(value)
        params = list(sig.parameters.items())
        param_types, return_type = get_type_func(value)
        if not "@staticmethod" in inspect.getsource(value):
            params = params[1:]
            param_types = param_types[1:]
        return Func(
            name,
            tuple(
                Arg(
                    n,
                    t,
                    self._convert_arg_kind(str(p.kind))
                    | (0 if p.default is sig.empty else DEFAULT),
                )
                for (n, p), t in zip(params, param_types)
            ),
            return_type,
        )

    def _handle_class(self, name, value):  # type: (str, Any) -> Class
        return Class(name, tuple(self.traverse(value)))

    @staticmethod
    def _handle_variable(name, value):  # type: (str, Any) -> Var
        return Var(name, get_type(value))

    def _handle_module(self, name, value):  # type: (str, Any) -> Module
        return Module(name, value.__name__, tuple(self.traverse(value)))

    @staticmethod
    def _is_public(name):  # type: (str) -> bool
        return name == "__init__" or not name.startswith("_")

    @staticmethod
    def _convert_arg_kind(kind):  # type: (str) -> int
        if kind == "POSITIONAL_ONLY":
            return POSITIONAL
        if kind == "KEYWORD_ONLY":
            return KEYWORD
        if kind == "POSITIONAL_OR_KEYWORD":
            return POSITIONAL | KEYWORD
        if kind == "VAR_POSITIONAL":
            return POSITIONAL | VARIADIC
        if kind == "VAR_KEYWORD":
            return KEYWORD | VARIADIC
        raise TypeError("Unknown type.")
