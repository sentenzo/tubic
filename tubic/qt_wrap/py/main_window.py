import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg
import PyQt6.QtCore as qtc

from tubic.qt_wrap.pyui.main_window import Ui_MainWindow

from tubic.qt_wrap.misc import get_icon, open_explorer


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
        self.setWindowIcon(get_icon("file-video", [24, 48, 72, 96]))

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
        self.pb_abort_download: qtw.QPushButton = _f(
            qtw.QPushButton, "pb_abort_download"
        )
        self.pb_abort_download.setVisible(False)

        self.l_thumbnail: qtw.QLabel = _f(qtw.QLabel, "l_thumbnail")
        self.l_status: qtw.QLabel = _f(qtw.QLabel, "l_status")

        self.pb_settings: qtw.QPushButton = _f(qtw.QPushButton, "pb_settings")
        self.pb_settings.setIcon(get_icon("cog", [24]))

        self.pb_open_download_folder: qtw.QPushButton = _f(
            qtw.QPushButton, "pb_open_download_folder"
        )
        self.pb_open_download_folder.setIcon(get_icon("folder-dim", [24]))
        self._open_download_folder: str = ""
        self.pb_open_download_folder.clicked.connect(
            lambda: open_explorer(self._open_download_folder)
        )

        self.thread_pool: set[qtc.QThread] = set()
        self._abort_one_worker = False

    def _set_lock_input(self, locked) -> None:
        self.pb_download_video.setEnabled(locked == False)
        self.pb_download_audio.setEnabled(locked == False)
        self.le_youtube_link.setEnabled(locked == False)
        self.pb_settings.setEnabled(locked == False)

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

    def abort_one_worker(self):
        self._abort_one_worker = True

    def activate_download_folder(self, path: str, cathegory: str | None = None):
        self._open_download_folder = path
        ico = {"audio": "folder-music", "video": "folder-video"}.get(cathegory, None)
        if ico:
            self.pb_open_download_folder.setIcon(get_icon(ico, [24]))
            self.pb_open_download_folder.setEnabled(True)
            self.pb_open_download_folder.setCursor(
                qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor)
            )
        else:
            self.pb_open_download_folder.setIcon(get_icon("folder-dim", [24]))
            self.pb_open_download_folder.setEnabled(False)
            self.pb_open_download_folder.setCursor(
                qtg.QCursor(qtc.Qt.CursorShape.ArrowCursor)
            )
