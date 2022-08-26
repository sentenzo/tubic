import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow

from qt.py_ui.main_window import Ui_MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    app.exec()
