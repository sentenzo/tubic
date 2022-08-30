import sys
import re
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg
from PyQt6.QtCore import Qt

from qt.py_ui.main_window import Ui_MainWindow
from ytdpl_wrapper import download_videos, download_thumbnail


class YtMainWindow(qtw.QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        Ui_MainWindow().setupUi(self)
        self.setFocus()
        self.setFixedSize(self.size())

        self.le_youtube_link: qtw.QLineEdit = self.findChild(
            qtw.QLineEdit, "le_youtube_link"
        )
        pb_download_video: qtw.QPushButton = self.findChild(
            qtw.QPushButton, "pb_download_video"
        )
        pb_download_audio: qtw.QPushButton = self.findChild(
            qtw.QPushButton, "pb_download_audio"
        )
        self.l_thumbnail: qtw.QLabel = self.findChild(qtw.QLabel, "l_thumbnail")

        def do_download_video():
            youtube_link = self.le_youtube_link.text()
            download_videos([youtube_link])

        def do_download_audio():
            youtube_link = self.le_youtube_link.text()
            download_videos([youtube_link], ydl_params={"format": "bestaudio"})

        pb_download_video.clicked.connect(do_download_video)
        pb_download_audio.clicked.connect(do_download_audio)

    def focusInEvent(self, event) -> None:
        youtube_link: str = qtw.QApplication.clipboard().text()

        re_templates = [
            # https://www.youtube.com/watch?v=cmb6pTj67Nk&___any_other_stuff
            r"https\://www\.youtube\.com/watch\?v=([\w\d-]+).*",
            # https://www.youtube.com/embed/cmb6pTj67Nk?
            r"https\://www\.youtube\.com/embed/([\w\d-]+).*",
            # https://youtu.be/cmb6pTj67Nk
            r"https\://youtu\.be/([\w\d-]+).*",
        ]
        video_code = None
        for re_temp in re_templates:
            match = re.match(re_temp, youtube_link)
            if match and match.groups():
                video_code = match.groups()[0]
                self.le_youtube_link.setText(f"https://youtu.be/{video_code}")
                break
        else:
            return

        thumbnail = download_thumbnail(video_code)
        self.l_thumbnail.setPixmap(thumbnail)


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = YtMainWindow()
    window.show()
    app.exec()
