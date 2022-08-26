import sys
import PyQt6.QtWidgets as qtw

# from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QTextEdit

from qt.py_ui.main_window import Ui_MainWindow
from ytdpl_wrapper import download_videos

app = qtw.QApplication(sys.argv)
window = qtw.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)


def do__download_all():
    te_youtube_links = window.findChild(qtw.QTextEdit, "te_youtube_links")
    youtube_links = te_youtube_links.toPlainText().split()
    download_videos(youtube_links)


window.findChild(qtw.QPushButton, "pb_download_all").clicked.connect(do__download_all)

if __name__ == "__main__":

    window.show()
    app.exec()
