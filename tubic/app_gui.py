import sys
import PyQt6.QtWidgets as qtw

from tubic.qt_wrap.tubic_main_window import MainWindow


def run():
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    run()
