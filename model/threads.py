from typing import List

from PyQt5.QtCore import QObject, pyqtSignal

from model.file_node import FileNode
from model.process import Request
from util.const import *
from util.flags import *


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

    def download_file(self, file: FileNode, destiny=Paths.DOWNLOAD_DIR):
        request = Request()
        request.signals(self.info_signal, self.progress_signal, self.error_signal, self.finish_signal)
        request.download_file(file=file, destiny=destiny)

    def get_page(self, url: str, parent: str):
        request = Request()
        request.signals(self.info_signal, self.progress_signal, self.error_signal, self.finish_signal)
        request.get_page(url=url, parent=parent)

    def read_html_file(self):
        request = Request()
        request.signals(self.info_signal, self.progress_signal, self.error_signal, self.finish_signal)
        request.read_html_file()

    def get_light_weight_file(self, url: str):
        request = Request()
        request.signals(self.info_signal, self.progress_signal, self.error_signal, self.finish_signal)
        request.get_light_weight_file(url=url)


class DownloadThread(QObject):
    # info_signal: info:str
    file_size_signal = pyqtSignal(int, object)
    file_type_signal = pyqtSignal(int, object)
    # progress_signal: idx:int, state:str, dl_size:str, progress:int, speed:str, estimated_time:str
    progress_signal = pyqtSignal(int, object, object, object, object, object)
    # error_signal: idx:int, filename:str, error:Exception
    error_signal = pyqtSignal(object, object)
    # finish signals
    finish_one_task_signal = pyqtSignal(int, object, object, object)
    finish_all_signal = pyqtSignal()

    def __init__(self, parent=None):
        QObject.__init__(self)
        self._parent = parent

    def download(self, urls: List[FileNode], dest: str = Paths.DOWNLOAD_DIR):
        """
        Downloads all files in queue
        :param urls:
        :param dest:
        :return:
        """
        i = 0
        while len(urls) and self._parent.state != STOP_ALL:
            file = urls.pop(0)
            try:
                self.download_async(i=0, file=file, dest=dest, urls=urls)
            except Exception as e:
                self.error_signal.emit(file.filename, e)
            i += 1
        self.finish_all_signal.emit()

    def download_async(self, i: int, file: FileNode, dest: str = Paths.DOWNLOAD_DIR, urls: List[FileNode] = []):
        """
        Downloads one file
        :param i:
        :param file:
        :param dest:
        :return:
        """
        import time
        from pySmartDL import SmartDL
        #
        url = file.href
        try:
            #
            download = SmartDL(url, progress_bar=False, dest=dest, verify=False, timeout=AppSettings.TIMEOUT,
                               threads=AppSettings.THREADS)
            download.attemps_limit = AppSettings.RETRY
            download.start(blocking=False)
            #
            if not file.size:
                file.size = download.filesize
                self.file_size_signal.emit(i, download.filesize)
            # if not file.type:
            #    self.file_type_signal.emit(i, download.file_type)
            #
            while not download.isFinished():
                if self._parent.state == PAUSE:
                    download.pause()
                elif self._parent.state == REANUDE:
                    download.unpause()
                elif self._parent.state == STOP:
                    download.stop()
                    self._parent.state = ""
                elif self._parent.state == STOP_ALL:
                    download.stop()
                #
                self.progress_signal.emit(i, download.get_status(), download.get_dl_size(human=True),
                                          download.get_progress() * 100,
                                          download.get_speed(human=True), download.get_eta(human=True))
                time.sleep(AppSettings.WAIT)
            if download.isSuccessful():
                self.finish_one_task_signal.emit(i, download.get_status(), file, download)
            else:
                urls.append(file)
                print("There were some errors:")
                for e in download.get_errors():
                    self.error_signal.emit(file, e)
        except Exception as e:
            self.error_signal.emit(file, e)
