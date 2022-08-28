import sys
import re
import PyQt6.QtWidgets as qtw

from qt.py_ui.main_window import Ui_MainWindow
from ytdpl_wrapper import download_videos


class YtMainWindow(qtw.QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        Ui_MainWindow().setupUi(self)
        self.setFocus()
        self.setFixedSize(self.size())

        self.le_youtube_link: qtw.QLineEdit = self.findChild(
            qtw.QLineEdit, "le_youtube_link"
        )
        pb_download_all: qtw.QPushButton = self.findChild(
            qtw.QPushButton, "pb_download_all"
        )

        def do_download_all():
            youtube_link = self.le_youtube_link.text()
            download_videos([youtube_link])

        pb_download_all.clicked.connect(do_download_all)

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
        for re_temp in re_templates:
            match = re.match(re_temp, youtube_link)
            if match and match.groups():
                video_code = match.groups()[0]
                self.le_youtube_link.setText(f"https://youtu.be/{video_code}")
                return

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = YtMainWindow()
    window.show()
    app.exec()
