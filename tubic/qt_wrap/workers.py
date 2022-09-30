import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg

from tubic.qt_wrap.py.main_window import MainWindowBase
from tubic.yt_dlp_wrap.link_wrapper import LinkWrapper


class WorkerAborted(Exception):
    pass


class Worker(qtc.QObject):
    finished = qtc.pyqtSignal()
    aborted = qtc.pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

    def run(self):
        pass

    def abort(self):
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
        worker.aborted.connect(worker.abort)
        thread.finished.connect(lambda: window.thread_pool.remove(thread))
        thread.finished.connect(window.unlock_input)
        thread.finished.connect(thread.deleteLater)

        return thread


class DownloadVideoWorker(Worker):
    def __init__(self, link_wrap_obj: LinkWrapper):
        super().__init__()
        self.link_wrap = link_wrap_obj

    def run(self):
        try:
            self.link_wrap.download()
        except WorkerAborted as ex:
            self.aborted.emit()
        self.finished.emit()

    def abort(self):
        pass

    @classmethod
    def create_thread(cls, window: MainWindowBase, link_wrap_obj: LinkWrapper):
        def abortion_check(status_line: str):
            if window._abort_one_worker:
                window._abort_one_worker = False
                window.set_status_line(status_line)
                raise WorkerAborted(status_line)

        def progress_bar_pseudo_graphic(value: int, total: int) -> str:
            pb_str_len = 30  # the length of the pseudo graphic progress bar
            full, empty = "■", "□"
            if value >= total:
                return full * pb_str_len
            full_count = int(pb_str_len * value / total)
            empty_count = pb_str_len - full_count
            return full * full_count + empty * empty_count

        # the arrow is pointing to the "Open download folder" icon-button
        finish_message = "finished            --------------->"

        def p_hook(msg):
            abortion_check("download was aborted")
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
                window.set_status_line(finish_message)

        def pp_hook(msg):
            abortion_check("post-processing was aborted")
            status = msg["status"]
            postprocessor = msg["postprocessor"]
            status_lines = {
                ("started", "ExtractAudio"): "extracting audio",
                ("started", "MoveFiles"): "moving files",
                ("finished", "MoveFiles"): finish_message,
            }
            status_line = status_lines.get((status, postprocessor), None)
            if status_line:
                window.set_status_line(status_line)

        link_wrap_obj = link_wrap_obj.progress_hook(p_hook).postprocessor_hook(pp_hook)

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
