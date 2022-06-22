from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QFrame, \
    QDockWidget, QWidget, QPlainTextEdit, QLabel

from util.const import AppEnums, AppSettings


class PreviewDock(QDockWidget):
    """
    A Dock widget that contains an image viewer and a text reader
    """

    def __init__(self, parent=None):
        QDockWidget.__init__(self)
        self._parent = parent
        # window
        self.setWindowTitle("Visualizador")
        self.setWindowIcon(QIcon(":/icons/images/start.ico"))
        self.setFeatures(QDockWidget.AllDockWidgetFeatures)
        self.setContentsMargins(0, 0, 0, 0)
        # edit text
        self.text_viewer = QPlainTextEdit()
        # customing edit text
        self.text_viewer.setFrameShape(QFrame.NoFrame)
        self.text_viewer.setReadOnly(True)
        self.text_viewer.setVisible(False)
        # label
        self.image_viewer = QLabel()  # PixmapLabel()
        self.image_viewer.setText("")
        # self.image_viewer.setScaledContents(True)
        self.image_viewer.setVisible(False)
        self.image_viewer.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        # widget container
        self.main_widget = QWidget(self)
        # layout
        self.layout = QVBoxLayout(self.main_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.text_viewer)
        self.layout.addWidget(self.image_viewer)
        # set default layout
        self.main_widget.setLayout(self.layout)
        #
        self.setWidget(self.main_widget)

    #
    def load(self, the_type: str, data):
        if the_type == AppEnums.TEXT:
            self.image_viewer.setVisible(False)
            self.text_viewer.setVisible(True)
            #
            self.text_viewer.setPlainText(data.decode("utf-8", errors="ignore"))
        else:
            self.image_viewer.setVisible(True)
            self.text_viewer.setVisible(False)
            #
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            pixmap = pixmap.scaled(AppSettings.PREVIEW_SIZE, AppSettings.PREVIEW_SIZE, Qt.KeepAspectRatioByExpanding,
                                   Qt.SmoothTransformation)
            #
            self.image_viewer.setPixmap(pixmap)

    def closeEvent(self, event) -> None:
        self._parent.preview_dock = None
        self._parent.removeDockWidget(self)
        event.accept()
