import os

import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg
import PyQt6.QtCore as qtc

from tubic.misc import fix_path


def get_icon(title: str, sizes: list[int]) -> qtg.QIcon:
    path = f"tubic/rec/ico/{title}-" + "{0}.png"
    rec_file = fix_path(path)
    app_icon = qtg.QIcon()
    for size in sizes:
        app_icon.addFile(rec_file.format(size), qtc.QSize(size, size))
    return app_icon


def choose_destination_folder(
    parent: qtw.QWidget,
    title: str,
    init_path: str,
    default_init_path: str = ".",
    silent: bool = False,
) -> qtw.QFileDialog:
    init_path_exists = os.path.isdir(init_path)
    if silent:
        if init_path_exists and init_path != default_init_path:
            return init_path
    elif not init_path_exists:
        init_path = default_init_path
    return qtw.QFileDialog.getExistingDirectory(parent, title, init_path)
