from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
from treelib import Tree, Node
from model.tree_loader import load_visuales_tree
from util.net import *
from util.util import *
import webbrowser
import ui.app_rc

class VisualesUCLV(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("ui/main.ui", self)
        #
        self.connections()
        self.add_some_elements_to_ui()
        # init Tree
        self.tree:Tree = Tree()
        self.url_list = []
        # load local data
        self.load_local_repo()
    
    def add_some_elements_to_ui(self):
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setMaximumWidth(100)
        self.progress.setVisible(False)
        self.state_label = QLabel("Visuales UCLV Desktop")
        self.statusbar.addWidget(self.state_label)
        self.statusbar.addPermanentWidget(self.progress)
        #
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nombre")
        self.search_input.setClearButtonEnabled(True)
        self.search_action_button = QToolButton()
        self.search_action_button.setText("Buscar")
        self.search_action_button.clicked.connect(self.deep_search)
        self.search_container = QWidget()
        self.layout = QHBoxLayout(self.search_container)
        self.layout.addWidget( self.search_input)
        self.layout.addWidget( self.search_action_button)
        self.search_container.setLayout(self.layout)
        self.search_container.setVisible(False)
        self.statusbar.addWidget(self.search_container)
        #
        self.toolbar = QToolBar("Toolbar")
        #
        self.search_button = QToolButton()
        self.search_button.setText("Buscar")
        self.search_button.setIcon(QIcon(":/icons/images/search.png"))
        self.search_button.setCheckable(True)
        self.search_button.clicked.connect(self.show_hide_search_widget)
        self.toolbar.addWidget(self.search_button)
        #
        self.addToolBar(self.toolbar)
    
    def show_hide_search_widget(self):
        is_visible = self.search_container.isVisible()
        if is_visible:
            self.search_container.setVisible(False)
            self.state_label.setVisible(True)
        else:
            self.search_container.setVisible(True)
            self.search_input.setFocus()
            self.state_label.setVisible(False)
            
    def deep_search(self):
        text = self.search_input.text()
        result = search(self.tree, text)
        #
        self.clear_table()
        # fill table
        for node in result:
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            if isinstance(node.tag, FileNode):
                icon_item = QTableWidgetItem()
                pixmap = QPixmap(FILE_TYPES[node.tag.type])
                pixmap = pixmap.scaled(ICON_SIZE, ICON_SIZE)
                icon = QIcon(pixmap)
                icon_item.setIcon(icon)
                self.tableWidget.setItem(row, 0, icon_item)
                self.tableWidget.setItem(row, 1, QTableWidgetItem(node.tag.filename))
                self.tableWidget.setItem(row, 2, QTableWidgetItem(node.tag.modification_date))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(nz(node.tag.size)))
                # add to urls to list
                self.url_list.append(node.tag.href)
            else:
                icon_item = QTableWidgetItem()
                pixmap = QPixmap(":/icons/images/folder.png")
                pixmap = pixmap.scaled(ICON_SIZE, ICON_SIZE)
                icon = QIcon(pixmap)
                icon_item.setIcon(icon)
                self.tableWidget.setItem(row, 0, icon_item)
                self.tableWidget.setItem(row, 1, QTableWidgetItem(node.tag))
                self.tableWidget.setItem(row, 2, QTableWidgetItem("-"))
                self.tableWidget.setItem(row, 3, QTableWidgetItem("-"))
                # add to urls to list
                self.url_list.append(node.identifier)
        #print(self.url_list)
        self.tableWidget.resizeColumnsToContents()
    
    def load_local_repo(self):
        # load serialized tree file
        try:
            print(f"Cargando archivo {TREE_DATA_FILE_NAME}")
            self.tree = load_all_dirs_n_files_tree()
            print("Llenando árbol...")
            self.fill_tree(None, self.tree.get_node(self.tree.root))
            return True
        except TreeFileDoesntExistException as e:
            print(f"\tTarea fallida [{TREE_DATA_FILE_NAME}]")
            print("\t" + str(e.args[0]))
            #
            self.read_html_file()
    
    def read_html_file(self):
        print(f"Leyendo archivo {DIRS_FILE_NAME}")
        try:
            html_str = get_directories()
            self.tree = load_visuales_tree(html_str)
            self.fill_tree(None, self.tree.get_node(self.tree.root))
            return True
        except DirsFileDoesntExistException as e:
            print(f"\tTarea fallida [{TREE_DATA_FILE_NAME}]")
            print("\t" + str(e.args[0]))
    
    def download_remote_repo(self):
        print(f"Descargando archivo {LISTADO_HTML_FILE}")
        try:
            download_listado_file()
        except Exception as e:
            print(f"\tTarea fallida [{TREE_DATA_FILE_NAME}]")
            print("\t" + str(e.args))
            self.state_label.setText(CONNECTION_FAIL)
        else:
            self.read_html_file()
        
    def connections(self):
        self.treeWidget.itemExpanded.connect(self.get_expanded_item)
        self.treeWidget.itemClicked.connect(self.add_children_to_item)
        self.tableWidget.itemDoubleClicked.connect(self.open_in_explorer)
        # menu
        self.load_data_action.triggered.connect(self.load_local_repo)
        self.save_local_repo_action.triggered.connect(save_all_dirs_n_files_tree)
        self.download_remote_repo_action.triggered.connect(self.download_remote_repo)
        
    def open_in_explorer(self):
        i = self.tableWidget.currentRow()
        webbrowser.open(self.url_list[i], new=1, autoraise=False)
    
    def add_children_to_item(self, selected_item:QTreeWidgetItem):
        node:Node = self.tree.get_node(selected_item.text(1))
        if not have_children(self.tree, node):
            try:
                childrens = get_page(selected_item.text(1), node.identifier)
                add_file_nodes_2_tree(tree=self.tree, parent=node, nodes=childrens)
            except Exception as e:
                self.state_label.setText(CONNECTION_FAIL)
        node = self.tree.get_node(selected_item.text(1))
        self.fill_files_table(node)
    
    def clear_table(self):
        # clear table
        while self.tableWidget.rowCount () > 0:
            self.tableWidget.removeRow (0)
        self.url_list.clear()
    
    def fill_files_table(self, node:Node):
        self.clear_table()
        # get children
        children = self.tree.children(node.identifier)
        # fill table
        for node in children:
            node = node.tag
            if isinstance(node, FileNode):
                row = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row)
                icon_item = QTableWidgetItem()
                pixmap = QPixmap(FILE_TYPES[node.type])
                pixmap = pixmap.scaled(ICON_SIZE, ICON_SIZE)
                icon = QIcon(pixmap)
                icon_item.setIcon(icon)
                self.tableWidget.setItem(row, 0, icon_item)
                self.tableWidget.setItem(row, 1, QTableWidgetItem(node.filename))
                self.tableWidget.setItem(row, 2, QTableWidgetItem(node.modification_date))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(nz(node.size)))
                
                # add to urls to list
                self.url_list.append(node.href)
        print(self.url_list)
        self.tableWidget.resizeColumnsToContents()
    
    def get_expanded_item(self, expanded_item:QTreeWidgetItem):
        self.fill_tree(expanded_item, self.tree.get_node(expanded_item.text(1)))
        
    def error(self, msg):
        QMessageBox.critical(self, 'Error', str(msg))

    def fill_tree(self, parent:QTreeWidgetItem, node:Node):
        if parent is None:
            qchild = QTreeWidgetItem(["Visuales UCLV", node.tag + "/"])
            qchild.addChild(QTreeWidgetItem(["-", "None"]))
            self.treeWidget.insertTopLevelItem(0, qchild)
            return
        if not node.is_leaf():
            if parent.child(0).text(1) == "None":
                parent.removeChild(parent.child(0))
                for child in self.tree.children(node.identifier):
                    if not isinstance(child.tag, FileNode):
                        qchild = QTreeWidgetItem([child.tag, child.identifier])
                        if not child.is_leaf():
                            qchild.addChild(QTreeWidgetItem(["-", "None"]))
                        parent.addChild(qchild)
                        
    def closeEvent(self, event) -> None:
        save_all_dirs_n_files_tree(self.tree)
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    import qdarkstyle
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    visuales = VisualesUCLV()
    visuales.show()
    app.exec()