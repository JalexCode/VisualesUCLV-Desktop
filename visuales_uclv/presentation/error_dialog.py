from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QLabel, QApplication
from PySide6.QtCore import Qt
import os

class ErrorDialog(QDialog):
    def __init__(self, title, message, details="", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(500, 400)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(f"<b>{message}</b>"))

        self.details_edit = QTextEdit()
        self.details_edit.setReadOnly(True)
        self.details_edit.setText(details)
        layout.addWidget(self.details_edit)

        btn_layout = QHBoxLayout()

        copy_btn = QPushButton("Copiar al Portapapeles")
        copy_btn.clicked.connect(self.copy_to_clipboard)
        btn_layout.addWidget(copy_btn)

        save_btn = QPushButton("Guardar en Archivo")
        save_btn.clicked.connect(self.save_to_file)
        btn_layout.addWidget(save_btn)

        close_btn = QPushButton("Cerrar")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)

        layout.addLayout(btn_layout)

    def copy_to_clipboard(self):
        QApplication.clipboard().setText(self.details_edit.toPlainText())

    def save_to_file(self):
        from datetime import datetime
        filename = f"error_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.details_edit.toPlainText())
        os.startfile(filename) if os.name == 'nt' else None
