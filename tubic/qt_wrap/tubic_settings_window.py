import PyQt6.QtWidgets as qtw

from tubic.qt_wrap.py.settings_window import SettingsWindowBase
from tubic.config import SETTINGS, save_settings


class SettingsWindow(SettingsWindowBase):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
