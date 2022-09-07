import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg
import PyQt6.QtCore as qtc

from tubic.qt_wrap.pyui.main_window import Ui_MainWindow
import tubic.qt_wrap.helpers as helpers


class MainWindowBase(qtw.QMainWindow):
    """
    The interlayer baseclass between QMainWindow and the functional MainWindow class.
    It refines the UI functionality in a way hardly achievable with auto-generated code.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        Ui_MainWindow().setupUi(self)
        self.setFocus()
        self.setFixedSize(self.size())
        self.setWindowIcon(helpers.getWindowIcon())

        self.status_line_descriptor = (
            "-" * 11
        )  # youtube video id usually contains 11 symbols

        _f = self.findChild
        self.le_youtube_link: qtw.QLineEdit = _f(qtw.QLineEdit, "le_youtube_link")
        self.pb_download_video: qtw.QPushButton = _f(
            qtw.QPushButton, "pb_download_video"
        )
        self.pb_download_audio: qtw.QPushButton = _f(
            qtw.QPushButton, "pb_download_audio"
        )
        self.l_thumbnail: qtw.QLabel = _f(qtw.QLabel, "l_thumbnail")
        self.l_status: qtw.QLabel = _f(qtw.QLabel, "l_status")

        self.thread_pool = set()

    def _set_lock_input(self, locked) -> None:
        self.pb_download_video.setEnabled(locked == False)
        self.pb_download_audio.setEnabled(locked == False)
        self.le_youtube_link.setEnabled(locked == False)

        cursor = qtg.QCursor(qtc.Qt.CursorShape.ArrowCursor)
        if locked:
            cursor = qtg.QCursor(qtc.Qt.CursorShape.WaitCursor)
        self.setCursor(cursor)
        self.l_thumbnail.setCursor(cursor)

    def lock_input(self) -> None:
        self._set_lock_input(True)

    def unlock_input(self) -> None:
        self._set_lock_input(False)

    def set_status_line(self, status_line: str, descriptor: str = None) -> None:
        descriptor = descriptor or self.status_line_descriptor
        text = f"[{descriptor}]: {status_line}"
        self.l_status.setText(text)
