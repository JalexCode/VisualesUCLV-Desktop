from PySide6.QtWidgets import QDialog
from visuales_uclv.presentation.ui.about_ui import Ui_Dialog

class AboutDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        # In a real app we'd get these from a central AppInfo
        self.app_name.setText("Visuales UCLV Explorer v0.5.0")
        self.colaborators.setPlainText("Rolando Juan Rio Garaboa\nDavid Valdespino Pavón")
        self.about.setPlainText("Explorador local para el repositorio visuales.uclv.cu")
