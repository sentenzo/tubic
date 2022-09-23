import os.path
import sys


def fix_path(path: str) -> str:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        # _MEIPASS - the env-var pyinstaller sets when the packed application launches
        #  - it contains the path to the temp directory with the distribution
        return os.path.join(sys._MEIPASS, path)
    else:
        return path
