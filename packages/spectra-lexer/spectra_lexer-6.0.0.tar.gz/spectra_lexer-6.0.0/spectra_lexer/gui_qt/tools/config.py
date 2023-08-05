from collections import defaultdict

from PyQt5.QtWidgets import QCheckBox, QFormLayout, QFrame, QLabel, QLayout, QLineEdit, QMessageBox, QTabWidget, \
    QVBoxLayout

from .base import GUIQT_TOOL
from .dialog import DialogContainer, FormDialog
from spectra_lexer.resource import ConfigDictionary

# Each supported option type uses a specific editing widget with basic getter and setter methods.
_W_TYPES = {bool: (QCheckBox, QCheckBox.isChecked, QCheckBox.setChecked),
            str:  (QLineEdit, QLineEdit.text,      QLineEdit.setText)}


def _save_dict(d:dict) -> dict:
    """ Call the save method on all values in a dict and replace them in a new dict with their return values. """
    return {k: v.save() for k, v in d.items()}


class OptionRow(list):

    def __init__(self, val:object, opt_tp:type, label:str, desc:str):
        """ Create a new widget row for a config option based on its attributes. Only basic types are supported.
            If an unsupported type is given, it is handled as a string (the native format for ConfigParser). """
        w_tp = opt_tp if opt_tp in _W_TYPES else str
        w_factory, getter, setter = _W_TYPES[w_tp]
        w = w_factory()
        w.setToolTip(desc)
        w_label = QLabel(label)
        w_label.setToolTip(desc)
        super().__init__([w_label, w])
        # Option values must convert to the widget's native type on load, and back to the option's type on save.
        setter(w, w_tp(val))
        self.save = lambda: opt_tp(getter(w))


class OptionPage(QFrame):

    def __init__(self, opt_dict:dict):
        """ Create a new page widget from one component's config info dict. """
        super().__init__()
        rows = {name: OptionRow(*opt) for name, opt in opt_dict.items()}
        layout = QFormLayout(self)
        for name, row in rows.items():
            layout.addRow(*row)
        self.save = lambda: _save_dict(rows)


class ConfigDialog(FormDialog):
    """ Outermost Qt config dialog window object. """

    TITLE = "Spectra Configuration"
    SIZE = (250, 300)

    def new_layout(self, info:dict) -> QLayout:
        """ Make and add the central widget using info from the dict and set the save callback. """
        layout = QVBoxLayout(self)
        w_tabs = QTabWidget(self)
        pages = {sect: OptionPage(info[sect]) for sect in sorted(info)}
        for sect, page in pages.items():
            w_tabs.addTab(page, sect)
        layout.addWidget(w_tabs)
        self.save = lambda: _save_dict(pages)
        return layout

    def submit(self) -> dict:
        """ Validate all config values from each page and widget. Show a popup if there are one or more errors.
            Return a dict with the new values (not the setup info) to the callback on dialog accept. """
        try:
            return ConfigDictionary(self.save())
        except TypeError:
            QMessageBox.warning(self, "Config Error", "One or more config types was invalid.")
        except ValueError:
            QMessageBox.warning(self, "Config Error", "One or more config values was invalid.")


class QtConfigTool(GUIQT_TOOL):
    """ Config manager; allows editing of config values for any component. """

    _dialog: DialogContainer

    def __init__(self):
        self._dialog = DialogContainer(ConfigDialog)

    def tools_config_open(self) -> None:
        self._dialog.open(self.WINDOW, self.submit, self._get_info())

    def submit(self, cfg:ConfigDictionary) -> None:
        self.CONFIG = cfg
        self.RSConfigSave(cfg)
        self.VIEWConfigUpdate(cfg)

    def _get_info(self) -> dict:
        """ Make a dict with detailed config info from active components and data from disk. """
        info = defaultdict(dict)
        data = defaultdict(dict, self.CONFIG)
        for sect, name, default, desc in self.CONFIG_INFO:
            v = data[sect].get(name, default)
            tp = type(v)
            label = name.replace("_", " ").title()
            info[sect][name] = [v, tp, label, desc]
        return info
