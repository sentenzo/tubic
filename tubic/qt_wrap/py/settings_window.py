import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg
import PyQt6.QtCore as qtc

from tubic.qt_wrap.pyui.settings_window import Ui_Settings


class SettingsWindowBase(qtw.QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        Ui_Settings().setupUi(self)
        self.setFocus()
        self.setFixedSize(self.size())

        self.pb_apply: qtw.QPushButton = self.findChild(qtw.QPushButton, "pb_apply")
        self.pb_cancel: qtw.QPushButton = self.findChild(qtw.QPushButton, "pb_cancel")

        self.pb_change_video_download_folder: qtw.QPushButton = self.findChild(
            qtw.QPushButton, "pb_change_video_download_folder"
        )
        self.pb_change_audio_download_folder: qtw.QPushButton = self.findChild(
            qtw.QPushButton, "pb_change_audio_download_folder"
        )

        self.le_video_download_folder: qtw.QLineEdit = self.findChild(
            qtw.QLineEdit, "le_video_download_folder"
        )
        self.le_audio_download_folder: qtw.QLineEdit = self.findChild(
            qtw.QLineEdit, "le_audio_download_folder"
        )
