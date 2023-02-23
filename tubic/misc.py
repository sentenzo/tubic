import os.path
import sys


def fix_path(path: str) -> str:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        # _MEIPASS - the env-var pyinstaller sets when the packed application launches
        #  - it contains the path to the temp directory with the distribution
        return os.path.join(sys._MEIPASS, path)
    else:
        return path


def parse_int_with_suffix(int_with_suff: str, default: int = 0) -> int:
    int_with_suff = list(int_with_suff)
    while int_with_suff and not int_with_suff[-1].isdigit():
        int_with_suff.pop()
    if not int_with_suff:
        return default
    return int("".join(int_with_suff))


def try_get_from_dict(dictionary, key_path: str, default=None):
    key_path = key_path.split(".")
    cur = dictionary
    for key in key_path:
        if key in cur:
            cur = cur[key]
        elif isinstance(cur, list) and len(cur) > 0 and key in cur[0]:
            cur = cur[0][key]
        else:
            return default
    return cur
