from concurrent.futures import thread
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg
import PyQt6.QtCore as qtc

from qt.py.main_window import MainWindowBase
from yt_dlp_wrap.link_wrapper import LinkWrapper, InvalidYoutubeLinkFormat
from qt.workers import DownloadVideoWorker


class MainWindow(MainWindowBase):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.yt_link_wrap: LinkWrapper = LinkWrapper.get_dummy()

        self.pb_download_video.clicked.connect(
            lambda: self.try_download(self.yt_link_wrap)
        )
        self.pb_download_audio.clicked.connect(
            lambda: self.try_download(self.yt_link_wrap.audio())
        )
        self.set_status_line("ready")

    def try_download(self, yt_link_wrap_obj: LinkWrapper):
        download_folder = qtw.QFileDialog.getExistingDirectory(self, "Select Directory")
        if download_folder:
            yt_link_wrap_obj = yt_link_wrap_obj.to(download_folder)

        self.set_status_line("preparations")

        thread = DownloadVideoWorker.create_thread(self, yt_link_wrap_obj)
        thread.start()

        self.lock_input()
        thread.finished.connect(self.unlock_input)

    def focusInEvent(self, event) -> None:
        youtube_link: str = qtw.QApplication.clipboard().text()

        try:
            new_yt_link = LinkWrapper(youtube_link=youtube_link)
            if (
                new_yt_link.video_id == self.yt_link_wrap.video_id
                and self.le_youtube_link.text()
            ):
                # the user trys to replace with the same link, so ...
                return  # ... my job here is done!
            self.le_youtube_link.setText(new_yt_link.video_url)
            self.yt_link_wrap = new_yt_link
        except InvalidYoutubeLinkFormat as ex:
            print(f"InvalidYoutubeLinkFormat: {ex}")
            return

        pm_thumbnail = qtg.QPixmap()
        pm_thumbnail.loadFromData(self.yt_link_wrap.download_thumbnail_bytes())
        self.l_thumbnail.setPixmap(pm_thumbnail)
        self.status_line_descriptor = self.yt_link_wrap.video_id
        self.set_status_line("ready")

        # the download buttons are initially locked
        self.unlock_input()
