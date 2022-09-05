# from abc import ABC, abstractmethod
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
from qt.py.main_window import MainWindowBase

from yt_dlp_wrap.link_wrapper import LinkWrapper


class Worker(qtc.QObject):
    finished = qtc.pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

    def run(self):
        pass

    @classmethod
    def create_thread(cls, window: MainWindowBase, *args) -> qtc.QThread:
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
    def __init__(self, link_wrap_obj: LinkWrapper):
        super().__init__()
        self.link_wrap = link_wrap_obj

    def run(self):
        self.link_wrap.download()
        self.finished.emit()

    @classmethod
    def create_thread(cls, window: MainWindowBase, link_wrap_obj: LinkWrapper):
        def progress_hook(msg):
            status = msg["status"]
            if status == "downloading":
                downloaded = msg["downloaded_bytes"]
                total = msg["total_bytes"]
                print("\n", f"downloaded={downloaded}, total={total}")
                total = max(total, 1)  # ZeroDivisionError prevention (just in case)
                percent = 100 * downloaded / total
                window.set_status_line(f"downloading -  {percent:05.2f}%")
            elif status == "finished":
                window.set_status_line(r"downloading - 100.00% - finished")
            # print("\n", msg["status"], list(msg.keys()))
            qtg.QGuiApplication.processEvents()  # refresh status_line text

        link_wrap_obj = link_wrap_obj.progress_hook(progress_hook)

        thread = super().create_thread(window, link_wrap_obj)
        thread.started.connect(window.lock_input)
        return thread


# class DownloadThumbnailWorker(Worker):
#     def __init__(self, link_wrap_obj: LinkWrapper):
#         super().__init__()
#         self.link_wrap = link_wrap_obj
