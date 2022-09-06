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

        thread.started.connect(window.lock_input)
        thread.started.connect(worker.run)

        thread.worker = worker  # without this line worker disappears from the scope before the thread launches it

        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(lambda: window.thread_pool.remove(thread))
        thread.finished.connect(window.unlock_input)
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
        def progress_bar_pseudo_graphic(value: int, total: int) -> str:
            pb_str_len = 30  # the length of the pseudo graphic progress bar
            full, empty = "■", "□"
            if value >= total:
                return full * pb_str_len
            full_count = int(pb_str_len * value / total)
            empty_count = pb_str_len - full_count
            return full * full_count + empty * empty_count

        def progress_hook(msg):
            status = msg["status"]
            if status == "downloading":
                downloaded = msg["downloaded_bytes"]
                total = msg["total_bytes"]
                total = max(total, 1)  # ZeroDivisionError prevention (just in case)
                percent = 100 * downloaded / total

                pbpg = progress_bar_pseudo_graphic(downloaded, total)
                window.set_status_line(f"working  - {pbpg} - {percent:05.2f}%")
            elif status == "finished":
                pbpg = progress_bar_pseudo_graphic(100, 100)
                window.set_status_line(f"finished - {pbpg} - 100.00%")

        link_wrap_obj = link_wrap_obj.progress_hook(progress_hook)

        thread = super().create_thread(window, link_wrap_obj)
        return thread


class DownloadThumbnailWorker(Worker):
    def __init__(self, link_wrap_obj: LinkWrapper):
        super().__init__()
        self.link_wrap = link_wrap_obj

    def run(self):
        self.link_wrap.get_thumbnail_bytes()
        self.finished.emit()

    @classmethod
    def create_thread(cls, window: MainWindowBase, link_wrap_obj: LinkWrapper):
        thread = super().create_thread(window, link_wrap_obj)

        def on_thread_finished():
            thumbnail_bytes = link_wrap_obj.get_thumbnail_bytes()
            pm_thumbnail = qtg.QPixmap()
            pm_thumbnail.loadFromData(thumbnail_bytes)
            window.l_thumbnail.setPixmap(pm_thumbnail)
            window.status_line_descriptor = link_wrap_obj.video_id
            window.set_status_line("ready")

        thread.finished.connect(on_thread_finished)

        return thread
