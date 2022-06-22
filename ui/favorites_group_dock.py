from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QAbstractItemView, QFrame, \
    QDockWidget, QWidget
from treelib import Tree

from model.folder_node import FolderNode
from util.const import FileTypes, AppSettings
from util.util import filter_favorites


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
        self.tableWidget.itemClicked.connect(
            lambda item: self._parent.async_get_page(self.tableWidget.item(item.row(), 2)))
        self.tableWidget.itemClicked.connect(self.locate)
        # widget container
        self.main_widget = QWidget(self)
        # layout
        self.layout = QVBoxLayout(self.main_widget)
        self.layout.addWidget(self.tableWidget)

        self.main_widget.setLayout(self.layout)
        #
        self.setWidget(self.main_widget)

    def load(self, tree: Tree):
        '''
        Fill table widget with Favorite nodes
        '''
        result: list = filter_favorites(tree)
        #
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        #
        for node in result:
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            #
            icon_item = QTableWidgetItem()
            if isinstance(node.tag, FolderNode):
                pixmap = QPixmap(":/icons/images/folder.png")
            else:
                pixmap = QPixmap(FileTypes[node.tag.type])
            pixmap = pixmap.scaled(AppSettings.ICON_SIZE, AppSettings.ICON_SIZE)
            icon = QIcon(pixmap)
            icon_item.setIcon(icon)
            self.tableWidget.setItem(row, 0, icon_item)
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(node.tag)))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(node.identifier))
        self.tableWidget.resizeColumnsToContents()

    def locate(self):
        i = self.tableWidget.currentRow()
        id = self.tableWidget.item(i, 2).text()
        self._parent.show_in_tree(id)

    def closeEvent(self, event) -> None:
        self._parent.favorite_group_button.setChecked(False)
        event.accept()
