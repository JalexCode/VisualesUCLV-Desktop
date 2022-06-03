import threading
from datetime import datetime
from io import StringIO

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QLabel, QProgressBar, QToolButton, QLineEdit, QWidget, QMainWindow, QHBoxLayout, QToolBar, \
    QTreeWidgetItem, QTableWidgetItem, QMessageBox, QApplication

from model.threads import RequestThread
from model.tree_loader import load_visuales_tree
from ui.about_dialog import AboutDialog
from util.logger import SENT_TO_LOG
from util.net import *
from util.settings import SETTINGS, SAVE_SETTINGS
from util.util import *
import webbrowser
import ui.app_rc
from ui.main import Ui_MainWindow


class VisualesUCLV(Ui_MainWindow, QMainWindow):
    work_in_progress = False

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        # init Tree
        self.tree: Tree = Tree()
        self.url_list = []
        #
        self.connections()
        self.add_some_elements_to_ui()
        # load local data
        self.load_local_repo()
        self.check_tree_is_empty()

    def connections(self):
        self.treeWidget.itemExpanded.connect(self.get_expanded_item)
        self.treeWidget.itemClicked.connect(self.async_get_page)
        self.tableWidget.itemClicked.connect(self.show_file_details_on_state_bar)
        self.tableWidget.itemDoubleClicked.connect(self.open_in_explorer)
        # self.tableWidget.itemClicked.connect(self.select_item_on_tree) #TODO
        # menu
        self.load_data_action.triggered.connect(self.load_local_repo)
        self.save_local_repo_action.triggered.connect(lambda: save_all_dirs_n_files_tree(self.tree))
        self.download_remote_repo_action.triggered.connect(self.request_remote_repo_file)
        #
        self.about_action.triggered.connect(self.show_about)

    def add_some_elements_to_ui(self):
        #
        self.setWindowTitle(APP_NAME)
        #
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
        #
        self.search_container = QWidget()
        self.layout = QHBoxLayout(self.search_container)
        self.layout.addWidget(self.search_input)
        self.layout.addWidget(self.search_action_button)
        self.search_container.setLayout(self.layout)
        self.search_container.setVisible(False)
        self.statusbar.addPermanentWidget(self.search_container)
        #
        self.toolbar = QToolBar("Toolbar")
        #
        self.search_button = QToolButton()
        self.search_button.setText("Buscar")
        self.search_button.setToolTip("Buscar archivos y directorios ya conocidos")
        self.search_button.setIcon(QIcon(":/icons/images/search.png"))
        self.search_button.setCheckable(True)
        self.search_button.clicked.connect(self.show_hide_search_widget)
        self.toolbar.addWidget(self.search_button)
        #
        self.favorite_button = QToolButton()
        self.favorite_button.setText("Agregar a Favoritos")
        self.favorite_button.setToolTip("Agrega a Favoritos el directorio seleccionado en el árbol")
        self.favorite_button.setIcon(QIcon(":/icons/images/favorite.png"))
        self.favorite_button.clicked.connect(self.set_node_as_favorite)
        self.toolbar.addWidget(self.favorite_button)
        #
        self.save_tree_button = QToolButton()
        self.save_tree_button.setText("Guardar árbol")
        self.save_tree_button.setToolTip("Guarda una copia local de los datos del árbol")
        self.save_tree_button.setIcon(QIcon(":/icons/images/save.png"))
        self.save_tree_button.clicked.connect(lambda: save_all_dirs_n_files_tree(self.tree))
        self.toolbar.addWidget(self.save_tree_button)
        #
        self.download_file_button = QToolButton()
        self.download_file_button.setText("Descargar repositorio remoto")
        self.download_file_button.setToolTip("Descarga los datos de los directorios del repositorio remoto")
        self.download_file_button.setIcon(QIcon(":/icons/images/download.png"))
        self.download_file_button.clicked.connect(lambda: self.request_remote_repo_file())
        self.toolbar.addWidget(self.download_file_button)
        #
        self.addToolBar(self.toolbar)
        #
        self.is_empty_message_label = QLabel(
            "No hay datos guardados localmente.\nSi está conectado a Internet, presione el botón 'Descargar repositorio remoto' para obtener el fichero de directorios del FTP e iniciar la exploración")
        self.is_empty_message_label.setAlignment(Qt.AlignCenter|Qt.AlignCenter)
        self.is_empty_message_label.setVisible(False)
        self.gridLayout.addWidget(self.is_empty_message_label)

    def set_node_as_favorite(self):
        selected_item: QTreeWidgetItem = self.treeWidget.currentItem()
        if selected_item is not None:
            node: Node = self.tree.get_node(selected_item.text(1))
            # update Favorite attribute in node
            tag = node.tag
            tag.favorite = not tag.favorite
            self.tree.update_node(node.identifier, tag=tag)
            if tag.favorite:
                self.treeWidget.currentItem().setIcon(0, QIcon(":/icons/images/favorite.png"))
            else:
                self.treeWidget.currentItem().setIcon(0, QIcon(""))

    def show_hide_search_widget(self):
        if self.tree.size(0):
            self.clear_table()
            is_visible = self.search_container.isVisible()
            self.search_container.setVisible(not is_visible)
            # self.state_label.setVisible(is_visible)
            self.dockWidget.setVisible(is_visible)
            self.search_input.setFocus()
        else:
            self.search_button.setChecked(False)

    def deep_search(self):
        text = self.search_input.text()
        result = search(self.tree, text)
        self.state_label.setText(f"Resultados: {len(result)}")
        #
        self.clear_table()
        # set horizontal header
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["", "Nombre", "Ruta", "Tamaño", "Fecha de modificación"])
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
                self.tableWidget.setItem(row, 2, QTableWidgetItem(node.identifier))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(nz(node.tag.size)))
                self.tableWidget.setItem(row, 4, QTableWidgetItem(node.tag.modification_date.strftime(DATE_FORMAT)))
                # add to urls to list
                self.url_list.append(node.tag.href)
            else:
                icon_item = QTableWidgetItem()
                pixmap = QPixmap(":/icons/images/folder.png")
                pixmap = pixmap.scaled(ICON_SIZE, ICON_SIZE)
                icon = QIcon(pixmap)
                icon_item.setIcon(icon)
                self.tableWidget.setItem(row, 0, icon_item)
                self.tableWidget.setItem(row, 1, QTableWidgetItem(str(node.tag)))
                self.tableWidget.setItem(row, 2, QTableWidgetItem(node.identifier))
                self.tableWidget.setItem(row, 3, QTableWidgetItem("-"))
                self.tableWidget.setItem(row, 4, QTableWidgetItem("-"))
                # add to urls to list
                self.url_list.append(node.identifier)
        # print(self.url_list)
        self.tableWidget.resizeColumnsToContents()

    def check_tree_is_empty(self):
        is_empty = self.tree.size(0) == 0
        self.dockWidget.setVisible(not is_empty)
        self.tableWidget.setVisible(not is_empty)
        self.is_empty_message_label.setVisible(is_empty)

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
            print(f"\tTarea fallida [{DIRS_FILE_NAME}]")
            print("\t" + str(e.args[0]))

    def set_progress(self, percent: int, speed, left_time):
        self.progress.setValue(percent)
        if speed is not None and left_time is not None:
            self.state_label.setText(f"Descargando {nz(speed)}/s {nd(left_time)}")

    def set_work_in_progress(self, b):
        self.progress.setVisible(b)
        self.work_in_progress = b

    def notificate_work_in_progress(self):
        QMessageBox.information(self, "Información", "Espere a que termine la tarea actual para proceder a realizar una nueva")

    def request_remote_repo_file(self):
        if not self.work_in_progress:
            print(f"Solicitando archivo {LISTADO_HTML_FILE}")
            try:
                self.set_work_in_progress(True)
                self.thread = RequestThread()
                self.thread.info_signal.connect(lambda text: self.state_label.setText(text))
                self.thread.error_signal.connect(lambda error: self.error(error.args))
                self.thread.finish_signal.connect(lambda response: self.download_remote_repo(response))
                thread = threading.Thread(target=self.thread.request_file)
                thread.start()
            except Exception as e:
                print(f"\tTarea fallida [{DIRS_FILE_NAME}]")
                print("\t" + str(e.args))
                self.state_label.setText(CONNECTION_FAIL)
        else:
            self.notificate_work_in_progress()

    def download_remote_repo(self, last_modified_header:str):
        # get last modified setting
        last_modified = SETTINGS.value("last_modification_date", type=str)
        # get last modified date from header
        current_last_modified = last_modified_header
        #
        if last_modified:
            last_modified = datetime.strptime(last_modified, DATE_FROM_SERVER_FORMAT)
        else:
            last_modified = current_last_modified
            SAVE_SETTINGS("last_modification_date", current_last_modified)
        # convert last_modification_date in datetime
        current_last_modified = datetime.strptime(current_last_modified, DATE_FROM_SERVER_FORMAT)
        # if file was updated
        if current_last_modified != last_modified:
            q = QMessageBox.question(self, "Información del repositorio", f"Los datos fueron actualizados el día {current_last_modified}. ¿Desea descargar los nuevos datos?",
                                     QMessageBox.Yes | QMessageBox.No)
            if q == QMessageBox.Yes:
                print(f"Descargando archivo {LISTADO_HTML_FILE}")
                try:
                    self.set_work_in_progress(True)
                    self.thread = RequestThread()
                    self.thread.info_signal.connect(lambda text: self.state_label.setText(text))
                    self.thread.progress_signal.connect(self.set_progress)
                    self.thread.error_signal.connect(lambda error: self.error(error.args))
                    self.thread.finish_signal.connect(self.success_download)
                    thread = threading.Thread(target=self.thread.download_file)
                    thread.start()
                except Exception as e:
                    print(f"\tTarea fallida [{DIRS_FILE_NAME}]")
                    print("\t" + str(e.args))
                    self.state_label.setText(CONNECTION_FAIL)
            else:
                self.set_work_in_progress(False)
        else:
            QMessageBox.information(self, "Información del repositorio",
                                 "No hay cambios en el repositorio")

    def success_download(self):
        self.set_work_in_progress(False)
        self.read_html_file()
        self.check_tree_is_empty()

    def show_file_details_on_state_bar(self):
        i = self.tableWidget.currentRow()
        is_searching = self.search_button.isChecked()
        size = self.tableWidget.item(i, 3 if is_searching else 2).text()
        modification_date = self.tableWidget.item(i, 4 if is_searching else 3).text()
        # set path in statusbar
        self.state_label.setText(
            f"Tamaño:{size}, Fecha de modificación:{modification_date}")  # , Ruta:{self.tableWidget.item(i, 2).text() if is_searching else self.url_list[i]}")

    def open_in_explorer(self):
        i = self.tableWidget.currentRow()
        is_searching = self.search_button.isChecked()
        webbrowser.open(self.tableWidget.item(i, 2).text() if is_searching else self.url_list[i], new=1,
                        autoraise=False)

    def select_item_on_tree(self):
        '''
        Shows file location in Tree Widget
        '''
        i = self.tableWidget.currentRow()
        text = "big"
        # QTreeWidget.item
        items = self.treeWidget.findItems(text, Qt.MatchFlag.MatchContains, 0)
        print(items)
        # self.treeWidget.setCurrentItem(items[0])

    def async_get_page(self, selected_item: QTreeWidgetItem):
        if not self.work_in_progress:
            # get node by column 1 text in QTreeWidgetItem
            node: Node = self.tree.get_node(selected_item.text(1))
            print(node.identifier)
            #
            if not have_children(self.tree, node):
                try:
                    if not node.tag.is_empty:
                        self.set_work_in_progress(True)
                        self.thread = RequestThread()
                        self.thread.info_signal.connect(lambda text: self.state_label.setText(text))
                        self.thread.progress_signal.connect(self.set_progress)
                        self.thread.error_signal.connect(lambda error: self.error(error.args))
                        self.thread.finish_signal.connect(
                            lambda children: self.add_children_to_item(children=children, node=node,
                                                                       selected_item=selected_item))
                        thread = threading.Thread(target=self.thread.get_page,
                                                  args=(selected_item.text(1), node.identifier,))
                        thread.start()
                except Exception as e:
                    print(e.args)
                    self.state_label.setText(CONNECTION_FAIL)
            else:
                self.fill_files_table(node)
        else:
            self.notificate_work_in_progress()

    def add_children_to_item(self, children: list, node: Node, selected_item: QTreeWidgetItem):
        #
        self.set_work_in_progress(False)
        #
        if children:
            add_file_nodes_2_tree(tree=self.tree, parent=node, nodes=children)
        else:
            tag = node.tag
            tag.is_empty = True
            self.tree.update_node(node.identifier, tag=tag)
        # fill table widget
        node = self.tree.get_node(selected_item.text(1))
        self.fill_files_table(node)

    def clear_table(self):
        # clear table
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        self.url_list.clear()

    def fill_files_table(self, node: Node):
        self.clear_table()
        # get children
        children = self.tree.children(node.identifier)
        #
        # get folder total size
        total_size = get_total_size(children)
        # set path in statusbar
        self.state_label.setText(f"Tamaño del directorio: {nz(total_size)}")
        # set horizontal header
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["", "Nombre", "Tamaño", "Fecha de modificación"])
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
                self.tableWidget.setItem(row, 1, QTableWidgetItem(str(node)))
                self.tableWidget.setItem(row, 2, QTableWidgetItem(nz(node.size)))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(node.modification_date.strftime(DATE_FORMAT)))

                # add to urls to list
                self.url_list.append(node.href)
        self.tableWidget.resizeColumnsToContents()

    def get_expanded_item(self, expanded_item: QTreeWidgetItem):
        self.fill_tree(expanded_item, self.tree.get_node(expanded_item.text(1)))

    def error(self, msg):
        self.set_work_in_progress(False)
        self.state_label.setText(AN_ERROR_WAS_OCURRED)
        QMessageBox.critical(self, 'Error', str(msg))

    def fill_tree(self, parent: QTreeWidgetItem, node: Node):
        if parent is None:
            qchild = QTreeWidgetItem(["Visuales UCLV", str(node.tag) + "/"])
            root_item = QTreeWidgetItem(["-", "None"])
            qchild.addChild(root_item)
            self.treeWidget.insertTopLevelItem(0, qchild)
            return
        print("Nodo vacio: ", str(node.tag.is_empty))
        if not node.is_leaf():
            if parent.child(0).text(1) == "None":
                # remove invisible item
                parent.removeChild(parent.child(0))
                for child in self.tree.children(node.identifier):
                    if not isinstance(child.tag, FileNode):
                        qchild = QTreeWidgetItem([str(child.tag), child.identifier])
                        # set favorite icon
                        if child.tag.favorite:
                            qchild.setIcon(0, QIcon(":/icons/images/favorite.png"))
                        # if child is not empty, add an invisible item
                        if not child.is_leaf():
                            qchild.addChild(QTreeWidgetItem(["-", "None"]))
                        parent.addChild(qchild)

    def closeEvent(self, event) -> None:
        if not self.work_in_progress:
            save_all_dirs_n_files_tree(self.tree)
            event.accept()
        else:
            QMessageBox.information(self, "Información", "No puede cerrar el programa aún porque hay una tarea activa. Si el programa se cerrase, la integridad de los datos pudiera perderse y consigo su respositorio local.\nPor favor, espere...")
            event.ignore()

    def show_about(self):
        self.about_dialog = AboutDialog()
        self.about_dialog.show()


import traceback


def excepthook(exc_type, exc_value, tracebackobj):
    """
    Global function to catch unhandled exceptions.

    Parameters
    ----------
    exc_type : str
        exception type
    exc_value : int
        exception value
    tracebackobj : traceback
        traceback object
    """
    separator = '-' * 80

    now = f'{datetime.now().strftime("%Y/%m/%d %H:%M:%S")} CRASH:'

    info = StringIO()
    traceback.print_tb(tracebackobj, None, info)
    info.seek(0)
    info = info.read()

    errmsg = '{}\t \n{}'.format(exc_type, exc_value)
    sections = [now, separator, errmsg, separator, info]
    msg = '\n'.join(sections)

    print(msg)

    SENT_TO_LOG(msg, "ERROR")


sys.excepthook = excepthook

if __name__ == "__main__":
    app = QApplication(sys.argv)
    import qdarkstyle

    app.setStyleSheet(qdarkstyle.load_stylesheet())
    visuales = VisualesUCLV()
    visuales.show()
    app.exec()
