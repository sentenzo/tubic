import sys
import PyQt6.QtWidgets as qtw

from qt.yt_main_window import MainWindow

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
