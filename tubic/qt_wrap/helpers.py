import os.path
import sys

import PyQt6.QtGui as qtg
import PyQt6.QtCore as qtc


def getWindowIcon() -> qtg.QIcon:

    rec_file = "tubic/rec/ico/file-video-{0}.png"
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        # _MEIPASS - the env-var pyinstaller sets when the packed application launches
        #  - it contains the path to the temp directory with the distribution
        rec_file = os.path.join(sys._MEIPASS, rec_file)
    app_icon = qtg.QIcon()
    app_icon.addFile(rec_file.format(24), qtc.QSize(24, 24))
    app_icon.addFile(rec_file.format(48), qtc.QSize(48, 48))
    app_icon.addFile(rec_file.format(72), qtc.QSize(72, 72))
    app_icon.addFile(rec_file.format(96), qtc.QSize(96, 96))

    return app_icon
