from PyQt5.QtCore import QObject, pyqtSignal
from model.file_node import FileNode
from model.process import Request
from util.const import DOWNLOAD_DIR
class SubTaskThread(QObject):
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

    def download_file(self, file:FileNode, destiny=DOWNLOAD_DIR):
        request = Request()
        request.signals(self.info_signal, self.progress_signal, self.error_signal, self.finish_signal)
        request.download_file(file=file, destiny=destiny)

    def get_page(self, url:str, parent:str):
        request = Request()
        request.signals(self.info_signal, self.progress_signal, self.error_signal, self.finish_signal)
        request.get_page(url=url, parent=parent)

    def read_html_file(self):
        request = Request()
        request.signals(self.info_signal, self.progress_signal, self.error_signal, self.finish_signal)
        request.read_html_file()

    def get_light_weight_file(self, url:str):
        request = Request()
        request.signals(self.info_signal, self.progress_signal, self.error_signal, self.finish_signal)
        request.get_light_weight_file(url=url)