import sys
import PyQt6.QtWidgets as qtw

from qt.yt_main_window import YtMainWindow

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = YtMainWindow()
    window.show()
    app.exec()
