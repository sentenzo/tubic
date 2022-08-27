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
    le_youtube_link = window.findChild(qtw.QLineEdit, "le_youtube_link")
    youtube_link = le_youtube_link.text()
    download_videos([youtube_link])


window.findChild(qtw.QPushButton, "pb_download_all").clicked.connect(do__download_all)

if __name__ == "__main__":

    window.show()
    app.exec()
