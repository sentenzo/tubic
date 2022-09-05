# from abc import ABC, abstractmethod
import PyQt6.QtCore as qtc
from qt.py.main_window import MainWindowBase

from yt_dlp_wrap.link_wrapper import LinkWrapper


class Worker(qtc.QObject):
    finished = qtc.pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

    def run(self):
        pass

    @classmethod
    def create_thread(cls, window: MainWindowBase, *args):
        thread = qtc.QThread()

        window.thread_pool.add(thread)  # we need thread not to be killed by GC

        worker = cls(*args)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)

        thread.worker = worker  # without this line worker disappears from the scope before the thread launches it

        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(lambda: window.thread_pool.remove(thread))
        thread.finished.connect(thread.deleteLater)

        return thread


class DownloadVideoWorker(Worker):
    def __init__(self, yt_link_wrap_obj: LinkWrapper):
        super().__init__()
        self.link_wrap = yt_link_wrap_obj

    def run(self):
        self.link_wrap.download()
        self.finished.emit()


# class DownloadThumbnailWorker(Worker):
#     ...
