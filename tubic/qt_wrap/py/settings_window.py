import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg
import PyQt6.QtCore as qtc

from tubic.qt_wrap.pyui.settings_window import Ui_Settings
from tubic.config import SETTINGS, save_settings, get_settings_by_path


class SettingsWindowBase(qtw.QDialog):
    SETTINGS_CONTROLS = {
        "GENERAL.always_ask_to_conform_the_destination_folder": (
            qtw.QCheckBox,
            "chb_conform_dest_folder",
        ),
        "GENERAL.import_cookies_from": (qtw.QComboBox, "cb_import_cookies_from"),
        #
        "VIDEO.download_folder": (qtw.QLineEdit, "le_video_download_folder"),
        "VIDEO.max_resolution": (qtw.QComboBox, "cb_max_video_resolution"),
        #
        "AUDIO.download_folder": (qtw.QLineEdit, "le_audio_download_folder"),
        "AUDIO.convert_to_mp3": (qtw.QCheckBox, "chb_to_mp3"),
        "AUDIO.mp3_bitrate": (qtw.QComboBox, "cb_mp3_bitrate"),
    }

    def load_settings(self):
        for path, info in SettingsWindowBase.SETTINGS_CONTROLS.items():
            type, id = info
            type2type = {qtw.QCheckBox: bool, qtw.QComboBox: str, qtw.QLineEdit: str}
            val = get_settings_by_path(path, type2type[type])
            control: type = self.findChild(type, id)
            if type == qtw.QCheckBox:
                control.setChecked = val
            elif type == qtw.QComboBox:
                for i in range(control.count()):
                    text = control.itemText(i)
                    if text.startswith(val):
                        control.setCurrentIndex(i)
                        break
            elif type == qtw.QLineEdit:
                control.setText(val)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        Ui_Settings().setupUi(self)
        self.setFocus()
        self.setFixedSize(self.size())

        # self.c: qtw.QLineEdit = self.findChild(qtw.QLineEdit, "cb_max_video_resolution")
        self.load_settings()
