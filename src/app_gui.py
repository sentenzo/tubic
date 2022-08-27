import sys
import re
import PyQt6.QtWidgets as qtw

from qt.py_ui.main_window import Ui_MainWindow
from ytdpl_wrapper import download_videos


class YtMainWindow(qtw.QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        ui = Ui_MainWindow()
        ui.setupUi(self)
        self.setFocus()

    def focusInEvent(self, event):
        le_youtube_link: qtw.QLineEdit = window.findChild(
            qtw.QLineEdit, "le_youtube_link"
        )
        if not le_youtube_link:
            return

        youtube_link: str = qtw.QApplication.clipboard().text()
        # https://www.youtube.com/watch?v=cmb6pTj67Nk
        re_template = r"https\://www\.youtube\.com/watch\?v=[\w\d-]+"
        if not re.match(re_template, youtube_link):
            return

        le_youtube_link.setText(youtube_link)


app = qtw.QApplication(sys.argv)
window = YtMainWindow()


def do__download_all():
    le_youtube_link = window.findChild(qtw.QLineEdit, "le_youtube_link")
    youtube_link = le_youtube_link.text()
    download_videos([youtube_link])


window.findChild(qtw.QPushButton, "pb_download_all").clicked.connect(do__download_all)

if __name__ == "__main__":

    window.show()
    app.exec()
