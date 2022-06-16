from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor, QPainter
from PyQt5.QtWidgets import QLabel, QSizePolicy


class PixmapLabel(QLabel):
    def __init__(self):
        QLabel.__init__(self)
        #self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(10, 10)

    def resizeEvent(self, event):
        pixmap = self.pixmap().scaled(self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        #pixmap.fill(QColor('#000000'))
        self.setPixmap(pixmap)
        # self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # self.setAlignment(Qt.AlignCenter)
        # self.setMinimumSize(10, 10)
