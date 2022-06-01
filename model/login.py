import requests
from exceptions import BadServerResponseCode, LoginError
from net import login


class Login:
    def __init__(self, user: str, passw: str):
        # credentials
        self._user = user
        self._passw = passw

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def passw(self):
        return self._passw

    @passw.setter
    def passw(self, value):
        self._passw = value

    def signals(self, post_request_signal, error, finish):
        self.post_request_signal = post_request_signal
        self.error_signal = error
        self.finish_signal = finish

    def post_data(self):
        try:
            self.post_request_signal.emit()
            login(user=self.user, passw=self.passw)
            self.finish_signal()
        except Exception as error:
            self.error_signal.emit(error)