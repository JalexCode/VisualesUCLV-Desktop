from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QAbstractItemView, QFrame, \
    QDockWidget, QWidget
from treelib import Tree

from util.const import ICON_SIZE
from util.util import filter_favorites
import ui.app_rc

class FavoritesGroup(QDockWidget):
    def __init__(self, parent=None):
        QDockWidget.__init__(self)
        self._parent = parent
        # window
        self.setWindowTitle("Favoritos")
        self.setWindowIcon(QIcon(":/icons/images/favorite.png"))
        self.setFeatures(QDockWidget.AllDockWidgetFeatures)
        # table
        self.tableWidget = QTableWidget(self)
        # customing
        self.tableWidget.setFrameShape(QFrame.NoFrame)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setAlternatingRowColors(True)
        # columns
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['', 'Nombre', 'Ruta'])
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.itemClicked.connect(lambda item: self._parent.async_get_page(self.tableWidget.item(item.row(), 2)))
        # widget container
        self.main_widget = QWidget(self)
        # layout
        self.layout = QVBoxLayout(self.main_widget)
        self.layout.addWidget(self.tableWidget)

        self.main_widget.setLayout(self.layout)
        #
        self.setWidget(self.main_widget)

    def load(self, tree:Tree):
        result:list = filter_favorites(tree)
        #
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        #
        for node in result:
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            #
            icon_item = QTableWidgetItem()
            pixmap = QPixmap(":/icons/images/folder.png")
            pixmap = pixmap.scaled(ICON_SIZE, ICON_SIZE)
            icon = QIcon(pixmap)
            icon_item.setIcon(icon)
            self.tableWidget.setItem(row, 0, icon_item)
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(node.tag)))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(node.identifier))
        self.tableWidget.resizeColumnsToContents()

    def closeEvent(self, event) -> None:
        self._parent.favorite_group_button.setChecked(False)
        event.accept()