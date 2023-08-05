from functools import partial
from pkgutil import get_data
import sys

from .impl import ObjectTreeDialog
from .row import RowData
from ..base import GUIQT_TOOL
from ..dialog import DialogContainer
from spectra_lexer.types.codec import XMLElement
from spectra_lexer.utils import recurse

_ICON_PATH = "/treeicons.svg"  # File with all object tree icons.


class package(dict):
    """ Class for packaging objects and modules under string keys in a nested dict. """

    __slots__ = ()

    @classmethod
    def nested(cls, d:dict, delim:str=".", root_key:str="__init__"):
        """ Split all keys on <delim> and nest package dicts in a hierarchy based on these splits.
            If one key is a prefix of another, it may occupy a slot needed for another level of dicts.
            If this happens, move the value one level deeper under <root_key>. """
        pkg = cls()
        for k, v in d.items():
            d = pkg
            *first, last = k.split(delim)
            for i in first:
                if i not in d:
                    d[i] = cls()
                elif not isinstance(d[i], cls):
                    d[i] = cls({root_key: d[i]})
                d = d[i]
            if last not in d or not isinstance(d[last], cls):
                d[last] = v
            else:
                d[last][root_key] = v
        return pkg


class ObjectTree(GUIQT_TOOL):
    """ Base class for the object tree. The fields are expensive to create and probably unused most of the time,
        so each one is a descriptor that computes itself only when accessed. """

    class lazy_field(partial):
        """ A field that computes its value only when needed, then sets it on the instance, overriding the getter. """
        def __get__(self, instance:object, owner:type):
            val = self(instance)
            setattr(instance, self.func.__name__, val)
            return val

    @lazy_field
    def root_dict(self) -> package:
        """ Make a root dict with packages containing all modules and the first level of components. """
        root_dict = self._components_by_path()
        root_dict["modules"] = package.nested(sys.modules)
        return root_dict

    @lazy_field
    def icon_data(self) -> list:
        """ Decode the SVG icon resource file and create individual icons for each type. """
        data = get_data(__package__, _ICON_PATH)
        root = XMLElement.decode(data)
        defs = [e for e in root if e.tag == "defs"]
        icon_list = []
        for elem in recurse(root):
            # Elements with at least one type alias are valid icons.
            types = elem.get("spectra_types")
            if types:
                # Make an encoded copy of the root node with only its defs and this element.
                icon = XMLElement(*defs, elem, **root)
                icon.tag = root.tag
                icon_list.append((types.split(), icon.encode()))
        return icon_list

    def _components_by_path(self) -> package:
        """ Return a nested package dict with each component indexed by its class's module path. """
        d = {}
        for cmp in self.ALL_COMPONENTS:
            ks = type(cmp).__module__.split(".")
            if ks[-1] == "base":
                ks.pop()
            d[".".join(ks[1:])] = cmp
        return package.nested(d)


class ObjectTreeTool(ObjectTree):
    """ Component for interactive tree operations. """

    _dialog: DialogContainer
    _last_exception: Exception = None  # Holds last exception caught from the engine.

    def __init__(self) -> None:
        self._dialog = DialogContainer(ObjectTreeDialog)

    def debug_tree_open(self) -> None:
        """ Add the last engine exception to the root dict if any were caught. """
        if self._last_exception is not None:
            self.root_dict["last_exception"] = self._last_exception
        resources = {"root_data": RowData(self.root_dict), "icon_data": self.icon_data}
        self._dialog.open(self.WINDOW, resources)

    def HandleException(self, exc:Exception) -> bool:
        """ Save the last exception for introspection. If THAT fails, the system is beyond help. """
        try:
            self._last_exception = exc
        except Exception:
            pass
        return True
