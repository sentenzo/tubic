import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg
import PyQt6.QtCore as qtc
from PyQt6.QtWidgets import QFileDialog

from qt.pyui.main_window import Ui_MainWindow
from yt_dlp_wrap.link_wrapper import LinkWrapper, InvalidYoutubeLinkFormat


class DownloadWorker(qtc.QObject):
    finished = qtc.pyqtSignal()

    def __init__(self, yt_link_wrap_obj: LinkWrapper):
        super().__init__()
        self.link_wrap = yt_link_wrap_obj

    def run(self):
        self.link_wrap.download()
        self.finished.emit()


class YtMainWindow(qtw.QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        Ui_MainWindow().setupUi(self)
        self.setFocus()
        self.setFixedSize(self.size())

        self.le_youtube_link: qtw.QLineEdit = self.findChild(
            qtw.QLineEdit, "le_youtube_link"
        )
        self.pb_download_video: qtw.QPushButton = self.findChild(
            qtw.QPushButton, "pb_download_video"
        )
        self.pb_download_audio: qtw.QPushButton = self.findChild(
            qtw.QPushButton, "pb_download_audio"
        )
        self.l_thumbnail: qtw.QLabel = self.findChild(qtw.QLabel, "l_thumbnail")

        self.yt_link_wrap: LinkWrapper = LinkWrapper.get_dummy()

        self.pb_download_video.clicked.connect(
            lambda: self.try_download(self.yt_link_wrap)
        )
        self.pb_download_audio.clicked.connect(
            lambda: self.try_download(self.yt_link_wrap.audio())
        )

    def try_download(self, yt_link_wrap_obj: LinkWrapper):
        download_folder = qtw.QFileDialog.getExistingDirectory(self, "Select Directory")
        if download_folder:
            yt_link_wrap_obj = yt_link_wrap_obj.to(download_folder)
        self.thread = qtc.QThread()
        self.worker = DownloadWorker(yt_link_wrap_obj)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

        self.setControlsEnabled(False)
        self.thread.finished.connect(lambda: self.setControlsEnabled(True))

    def setControlsEnabled(self, value: bool) -> None:
        self.pb_download_video.setEnabled(value)
        self.pb_download_audio.setEnabled(value)
        self.le_youtube_link.setEnabled(value)

        cursor = qtg.QCursor(qtc.Qt.CursorShape.WaitCursor)
        if value:
            cursor = qtg.QCursor(qtc.Qt.CursorShape.ArrowCursor)
        self.setCursor(cursor)
        self.l_thumbnail.setCursor(cursor)

    def focusInEvent(self, event) -> None:
        youtube_link: str = qtw.QApplication.clipboard().text()

        try:
            new_yt_link = LinkWrapper(youtube_link=youtube_link)
            if (
                new_yt_link.video_id == self.yt_link_wrap.video_id
                and self.le_youtube_link.text()
            ):
                # trying to replace with the same link
                return
            self.le_youtube_link.setText(new_yt_link.video_url)
            self.yt_link_wrap = new_yt_link
        except InvalidYoutubeLinkFormat as ex:
            print(ex)
            return

        pm_thumbnail = qtg.QPixmap()
        pm_thumbnail.loadFromData(self.yt_link_wrap.download_thumbnail_bytes())
        self.l_thumbnail.setPixmap(pm_thumbnail)

        self.setControlsEnabled(True)
