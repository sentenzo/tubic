import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg

from qt.pyui.main_window import Ui_MainWindow
from yt_dlp_wrap.link_wrapper import LinkWrapper, InvalidYoutubeLinkFormat


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

        self.setControlsEnabled(False)

        self.yt_link_wrap: LinkWrapper = LinkWrapper.get_dummy()

        self.pb_download_video.clicked.connect(lambda: self.yt_link_wrap.download())
        self.pb_download_audio.clicked.connect(
            lambda: self.yt_link_wrap.audio().download()
        )

    def setControlsEnabled(self, value: bool) -> None:
        self.pb_download_video.setEnabled(value)
        self.pb_download_audio.setEnabled(value)

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
