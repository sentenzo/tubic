from concurrent.futures import thread
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg
import PyQt6.QtCore as qtc

from qt.py.main_window import MainWindowBase
from yt_dlp_wrap.link_wrapper import LinkWrapper, InvalidYoutubeLinkFormat
from qt.workers import DownloadVideoWorker, DownloadThumbnailWorker


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

    def focusInEvent(self, event) -> None:
        youtube_link: str = qtw.QApplication.clipboard().text()
        new_yt_link_wrap = None
        try:
            new_yt_link_wrap = LinkWrapper(youtube_link=youtube_link)
        except InvalidYoutubeLinkFormat as ex:
            return
        if (
            new_yt_link_wrap.video_id == self.yt_link_wrap.video_id
            and self.pb_download_video.isEnabled()
        ):
            # the user trys to replace with the same link, so ...
            return  # ... my job here is done!
        self.le_youtube_link.setText(new_yt_link_wrap.video_url)
        self.yt_link_wrap = new_yt_link_wrap

        self.set_status_line("fetching thumbnail")

        thread = DownloadThumbnailWorker.create_thread(self, self.yt_link_wrap)
        thread.start()
