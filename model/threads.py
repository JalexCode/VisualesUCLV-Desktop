from PyQt5.QtCore import QObject, pyqtSignal

from login import Login

class LoginThread(QObject):
    post_request_signal = pyqtSignal()
    error_signal = pyqtSignal(object)
    finish_signal = pyqtSignal()
    def __init__(self, login_object:Login):
        QObject.__init__(self)
        self.login_object:Login = login_object

    def run(self):
        self.login_object.signals(self.post_request_signal, self.error_signal, self.finish_signal)
        self.login_object.post_data()