from PyQt5.QtCore import QObject, pyqtSignal
from model.process import Request
class RequestThread(QObject):
    info_signal = pyqtSignal(object)
    progress_signal = pyqtSignal(object, object, object)
    error_signal = pyqtSignal(object)
    finish_signal = pyqtSignal(object)
    def __init__(self):
        QObject.__init__(self)

    def request_file(self):
        request = Request()
        request.signals(self.info_signal, self.progress_signal, self.error_signal, self.finish_signal)
        request.request_file()

    def download_file(self):
        request = Request()
        request.signals(self.info_signal, self.progress_signal, self.error_signal, self.finish_signal)
        request.download_file()

    def get_page(self, url:str, parent:str):
        request = Request()
        request.signals(self.info_signal, self.progress_signal, self.error_signal, self.finish_signal)
        request.get_page(url=url, parent=parent)