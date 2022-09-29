import PyQt6.QtWidgets as qtw

from tubic.qt_wrap.py.settings_window import SettingsWindowBase
from tubic.config import (
    SETTINGS,
    save_settings,
    get_settings_by_path,
    set_settings_by_path,
)


class SettingsWindow(SettingsWindowBase):
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
        for path, info in SettingsWindow.SETTINGS_CONTROLS.items():
            type, id = info
            type2type = {qtw.QCheckBox: bool, qtw.QComboBox: str, qtw.QLineEdit: str}
            val = get_settings_by_path(path, type2type[type])
            control: type = self.findChild(type, id)
            if type == qtw.QCheckBox:
                control.setChecked(val)
            elif type == qtw.QComboBox:
                for i in range(control.count()):
                    text = control.itemText(i)
                    if text.startswith(val):
                        control.setCurrentIndex(i)
                        break
            elif type == qtw.QLineEdit:
                control.setText(val)

    def save_settings(self) -> bool:
        try:
            for path, (type, id) in SettingsWindow.SETTINGS_CONTROLS.items():
                control: type = self.findChild(type, id)
                val = None
                if type == qtw.QCheckBox:
                    val = str(control.isChecked())
                elif type == qtw.QComboBox:
                    val = control.currentText()
                elif type == qtw.QLineEdit:
                    val = control.text()
                set_settings_by_path(path, val)
            save_settings(SETTINGS)
            return True
        except Exception as ex:
            return False

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.pb_apply.clicked.connect(lambda: self.save_settings() and self.close())
        self.pb_cancel.clicked.connect(self.close)

        self.load_settings()
