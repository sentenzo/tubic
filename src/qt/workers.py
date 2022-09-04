import PyQt6.QtCore as qtc

from yt_dlp_wrap.link_wrapper import LinkWrapper


class DownloadWorker(qtc.QObject):
    finished = qtc.pyqtSignal()

    def __init__(self, yt_link_wrap_obj: LinkWrapper):
        super().__init__()
        self.link_wrap = yt_link_wrap_obj

    def run(self):
        self.link_wrap.download()
        self.finished.emit()

    @staticmethod
    def create_thread(yt_link_wrap_obj: LinkWrapper):
        thread = qtc.QThread()
        worker = DownloadWorker(yt_link_wrap_obj)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)

        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)

        return worker
