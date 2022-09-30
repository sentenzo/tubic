import PyQt6.QtWidgets as qtw

from tubic.qt_wrap.py.main_window import MainWindowBase
from tubic.qt_wrap.workers import DownloadVideoWorker, DownloadThumbnailWorker
from tubic.yt_dlp_wrap.link_wrapper import LinkWrapper, InvalidYoutubeLinkFormat
from tubic.qt_wrap.tubic_settings_window import SettingsWindow
from tubic.config import SETTINGS, save_settings
from tubic.qt_wrap.misc import choose_destination_folder, try_get_youtube_link_from_cb


class MainWindow(MainWindowBase):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.yt_link_wrap: LinkWrapper = LinkWrapper.get_dummy()

        self.pb_download_video.clicked.connect(
            lambda: self.try_download(
                self.yt_link_wrap.preset_video(), hide=self.pb_download_video
            )
        )
        self.pb_download_audio.clicked.connect(
            lambda: self.try_download(
                self.yt_link_wrap.preset_audio(), hide=self.pb_download_audio
            )
        )
        self.pb_abort_download.clicked.connect(self.abort_one_worker)
        self.set_status_line("ready")

        self.pb_settings.clicked.connect(self.show_settings)

        self.le_youtube_link.cursorPositionChanged.connect(self.youtube_link_click_slot)

    def show_settings(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()

    def try_download(
        self, yt_link_wrap_obj: LinkWrapper, hide: qtw.QWidget | None = None
    ):
        section = "AUDIO" if hide == self.pb_download_audio else "VIDEO"
        download_folder = choose_destination_folder(
            self,
            f"Select directory to download {section.lower()}",
            SETTINGS[section].get("download_folder", "."),
            silent=not SETTINGS["GENERAL"].getboolean(
                "always_ask_to_conform_the_destination_folder", True
            ),
        )
        if download_folder:
            yt_link_wrap_obj = yt_link_wrap_obj.to(download_folder)
            SETTINGS[section]["download_folder"] = download_folder
            save_settings(SETTINGS)
        else:
            return

        self.activate_download_folder(download_folder, section.lower())

        self.set_status_line("preparations")

        thread = DownloadVideoWorker.create_thread(self, yt_link_wrap_obj)
        if hide and hide.isVisible():
            hide.setVisible(False)
            self.pb_abort_download.setVisible(True)
            thread.finished.connect(
                lambda: [
                    hide.setVisible(True),
                    self.pb_abort_download.setVisible(False),
                ]  # a hack to run multiple lines in a lambda
            )
        thread.start()

    def _set_youtube_link(self, youtube_link: str):
        self.yt_link_wrap = LinkWrapper(youtube_link=youtube_link)
        self.le_youtube_link.setText(youtube_link)

        self.set_status_line("fetching thumbnail")
        thread = DownloadThumbnailWorker.create_thread(self, self.yt_link_wrap)
        thread.start()

    def focusInEvent(self, event) -> None:
        youtube_link: str = try_get_youtube_link_from_cb()
        if not youtube_link:
            return
        if (
            self.yt_link_wrap.video_url == youtube_link
            and self.pb_download_video.isEnabled()
        ):
            # the user trys to replace with the same link, so ...
            return  # ... my job here is done!
        self._set_youtube_link(youtube_link)

    def youtube_link_click_slot(self) -> None:
        new_yt_link: str | None = try_get_youtube_link_from_cb()
        old_yt_link: str | None = self.le_youtube_link.text()
        if new_yt_link == old_yt_link:
            self.set_status_line("ready")
        elif new_yt_link or not old_yt_link:
            self._set_youtube_link(new_yt_link)
            self.set_status_line("ready")
        elif old_yt_link:
            qtw.QApplication.clipboard().setText(old_yt_link)
            self.le_youtube_link.selectAll()
            self.set_status_line(f"{old_yt_link} - copied to clipboard")
