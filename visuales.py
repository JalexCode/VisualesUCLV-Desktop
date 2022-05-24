from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QTreeWidgetItem, QMessageBox
from PyQt5 import uic

import sys
class VisualesUCLV(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("main.ui", self)

    def error(self, msg):
        QMessageBox.critical(self, 'Error', str(msg))

    def fill_tree(self, tree):
        try:
            self.treeWidget.clear()
            pixmaps = {"lista": "ui/img/list.png", "objeto": "ui/img/object.png", "herencia": "ui/img/heredity.png",
                       "atributo": "ui/img/attribute.png"}
            root = True
            items = []
            for n in classes_tree:
                valor = n.valor
                if root:
                    items.append(QTreeWidgetItem([*valor]))
                    root = False
                    continue
                padre = n.padre.valor
                for x in range(len(items)):
                    if items[x].text(0) == padre[0]:
                        qtree_item = QTreeWidgetItem(items[x], [*valor])
                        if "Lista" in valor[1]:
                            qtree_item.setIcon(0, QIcon(QPixmap(pixmaps["lista"])))
                        elif "Padre" in valor[1]:
                            qtree_item.setIcon(0, QIcon(QPixmap(pixmaps["objeto"])))
                        elif "Hijo" in valor[1]:
                            qtree_item.setIcon(0, QIcon(QPixmap(pixmaps["herencia"])))
                        elif "Atributo" in valor[1]:
                            qtree_item.setIcon(0, QIcon(QPixmap(pixmaps["atributo"])))
                        items.append(qtree_item)
            self.treeWidget.addTopLevelItems(items)
            self.treeWidget.expandAll()
            self.treeWidget.resizeColumnToContents(0)
            self.treeWidget.resizeColumnToContents(1)
            # self.treeWidget.clear()
            # items = []
            # for n in classes_tree:
            #     valor = n.valor
            #     if n.es_raiz():
            #         items.append(QTreeWidgetItem(valor))
            #         continue
            #     padre = n.padre.valor
            #     for x in range(len(items)):
            #         if items[x].text(1) == padre[1]:
            #             items.append(QTreeWidgetItem(items[x], valor))
            # self.treeWidget.addTopLevelItems(items)
            # self.treeWidget.expandAll()
            # self.treeWidget.resizeColumnToContents(0)
            # #self.treeWidget.resizeColumnToContents(1)
        except Exception as e:
            self.error("Vista -> Actualizando árbol: %s" % e.args[0])
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    visuales = VisualesUCLV()
    visuales.show()
    app.exec()