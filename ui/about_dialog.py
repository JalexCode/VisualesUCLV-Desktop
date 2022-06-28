from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog
from ui.about import Ui_Dialog
from util.const import *

class AboutDialog(Ui_Dialog, QDialog):
    def __init__(self) -> None:
        QDialog.__init__(self)
        self.setupUi(self)
        #
        self.setWindowIcon(QIcon(":/icons/images/start.ico"))
        #
        self.app_name.setText(f"{AppInfo.NAME} v{AppInfo.version()}")
        self.colaborators.setPlainText(AppInfo.COLABORATORS)
        self.about.setPlainText(AppInfo.ABOUT)
