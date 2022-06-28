import sys
import threading
import traceback
import webbrowser
from datetime import datetime
from io import StringIO

import certifi
import urllib3
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QClipboard
from PyQt5.QtWidgets import QAction, QLabel, QMenu, QProgressBar, QToolButton, QLineEdit, QWidget, \
    QMainWindow, QHBoxLayout, QToolBar, \
    QTreeWidgetItem, QTableWidgetItem, QMessageBox, QApplication, QFileDialog

from model.threads import SubTaskThread
from ui.about_dialog import AboutDialog
from ui.downloader import DownloadManager
from ui.favorites_group_dock import FavoritesGroup
from ui.main import Ui_MainWindow
from ui.preview_dock import PreviewDock
from ui.text import *
from util.const import *
from util.logger import send_to_log
from util.settings import GENERAL_SETTINGS, save_settings
from util.util import *

urllib3.disable_warnings()

LastStateRole = Qt.ItemDataRole.UserRole


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
        # tree widget connections
        self.treeWidget.itemExpanded.connect(self.fill_node)
        self.treeWidget.itemClicked.connect(self.async_get_page)
        # table widget connections
        self.tableWidget.itemClicked.connect(
            self.show_file_details_on_state_bar)
        # self.tableWidget.cellChanged.connect(self.set_node_as_downloaded)
        self.tableWidget.itemDoubleClicked.connect(self.open_in_explorer)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(
            self.show_main_table_context_menu)
        # menu
        self.export_local_repo_as_txt_action.triggered.connect(
            self.export_tree_as_txt)
        #
        self.about_action.triggered.connect(self.show_about)
        #
        self.show_download_manager_action.triggered.connect(lambda: self.activate_download_manager_window(True))

    def activate_download_manager_window(self, show=False):
        if self.download_manager_window is None:
            self.download_manager_window = DownloadManager(self)
        if show:
            self.download_manager_window.show()

    def export_tree_as_txt(self):
        archivo, _ = QFileDialog.getSaveFileName(
            self, "Guardar árbol de repositorio", "", "Archivo de texto (*.txt)")
        if archivo:
            self.tree.save2file(archivo)

    def add_some_elements_to_ui(self):
        #
        self.setWindowTitle(AppInfo.NAME)
        # 
        self.favorites_group_window = None
        self.preview_dock = None
        self.download_manager_window = None
        # progress bar
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setMaximumWidth(100)
        # cancel button
        self.cancel_proccess_button = QToolButton()
        self.cancel_proccess_button.setText("Cancelar")
        # progress bar container
        self.progress_container = QWidget()
        self.progress_container.setMaximumWidth(150)
        self.progress_container.setContentsMargins(0, 0, 0, 0)
        self.progress_container_layout = QHBoxLayout(self.progress_container)
        self.progress_container_layout.setContentsMargins(0, 0, 0, 0)
        self.progress_container_layout.addWidget(self.progress)
        self.progress_container_layout.addWidget(self.cancel_proccess_button)
        self.progress_container.setLayout(self.progress_container_layout)
        self.progress_container.setVisible(False)
        # state label
        self.state_label = QLabel("Visuales UCLV Desktop")
        self.statusbar.addWidget(self.state_label)
        self.statusbar.addPermanentWidget(self.progress_container)
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
        self.download_remote_repo_button = QToolButton()
        self.download_remote_repo_button.setText(
            "Descargar repositorio remoto")
        self.download_remote_repo_button.setToolTip(
            "Descarga los datos de los directorios del repositorio remoto")
        self.download_remote_repo_button.setIcon(
            QIcon(":/icons/images/repo_download.png"))
        self.download_remote_repo_button.clicked.connect(
            lambda: self.request_remote_repo_file())
        self.toolbar.addWidget(self.download_remote_repo_button)
        #
        self.search_button = QToolButton()
        self.search_button.setText("Buscar")
        self.search_button.setToolTip(
            "Buscar archivos y directorios ya conocidos")
        self.search_button.setIcon(QIcon(":/icons/images/search.png"))
        self.search_button.setCheckable(True)
        self.search_button.clicked.connect(self.show_hide_search_widget)
        self.toolbar.addWidget(self.search_button)
        #
        self.favorite_group_button = QToolButton()
        self.favorite_group_button.setCheckable(True)
        self.favorite_group_button.setText("Ver Favoritos")
        self.favorite_group_button.setToolTip(
            "Visualizar todos los directorios marcados como Favoritos")
        self.favorite_group_button.setIcon(
            QIcon(":/icons/images/perm_group_bookmarks.png"))
        self.favorite_group_button.clicked.connect(self.show_all_favorites)
        self.toolbar.addWidget(self.favorite_group_button)
        #
        # self.save_tree_button = QToolButton()
        # self.save_tree_button.setText("Guardar árbol")
        # self.save_tree_button.setToolTip(
        #     "Guarda una copia local de los datos del árbol")
        # self.save_tree_button.setIcon(QIcon(":/icons/images/save.png"))
        # self.save_tree_button.clicked.connect(
        #     lambda: save_all_dirs_n_files_tree(self.tree))
        # self.toolbar.addWidget(self.save_tree_button)
        #
        self.toolbar.addSeparator()
        #
        self.favorite_button = QToolButton()
        self.favorite_button.setText("Agregar a Favoritos")
        self.favorite_button.setToolTip(
            "Agrega a Favoritos el directorio seleccionado en el árbol")
        self.favorite_button.setIcon(QIcon(":/icons/images/favorite.png"))
        self.favorite_button.clicked.connect(self.set_node_as_favorite)
        self.toolbar.addWidget(self.favorite_button)
        #
        # self.set_downloaded_button = QToolButton()
        # self.set_downloaded_button.setText("Marcar como Descargado")
        # self.set_downloaded_button.setToolTip(
        #     "Marca el archivo como 'Descargado'")
        # self.set_downloaded_button.setIcon(QIcon(":/icons/images/success.png"))
        # self.set_downloaded_button.clicked.connect(self.set_node_as_downloaded)
        # self.toolbar.addWidget(self.set_downloaded_button)
        #
        self.download_file_button = QToolButton()
        self.download_file_button.setText("Descargar")
        self.download_file_button.setToolTip(
            "Descargar elemento seleccionado")
        self.download_file_button.setIcon(QIcon(":/icons/images/download.png"))
        self.download_file_button.clicked.connect(self.add_to_download_queue)
        self.toolbar.addWidget(self.download_file_button)
        #
        self.export_as_txt_button = QToolButton()
        self.export_as_txt_button.setText("Exportar como TXT")
        self.export_as_txt_button.setToolTip(
            "Exporta todos los enlaces de la carpeta hacia un archivo de texto plano")
        self.export_as_txt_button.setIcon(QIcon(":/icons/images/txt.png"))
        self.export_as_txt_button.clicked.connect(self.export_as_txt)
        self.toolbar.addWidget(self.export_as_txt_button)
        #
        self.toolbar.setWindowTitle("Barra de herramientas")
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.toolbar)
        #
        self.message_label = QLabel(NO_LOCAL_DATA)
        self.message_label.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.message_label.setVisible(False)
        self.gridLayout.addWidget(self.message_label)

    def export_as_txt(self):
        file, _ = QFileDialog.getSaveFileName(self, "Exportar enlaces como archivo de texto", "",
                                              "Archivo de texto (*.txt)")
        if file:
            txt = "\n".join(self.url_list)
            with open(file, mode="w", encoding="UTF-8") as txt_file:
                txt_file.write(txt)

    def set_node_as_favorite(self):
        '''
        Toggle boolean value in Favorite attribute
        '''

        def update_node(nid: str):
            node: Node = self.tree.get_node(nid)
            # update Favorite attribute in node
            tag = node.tag
            tag.favorite = not tag.favorite
            self.tree.update_node(node.identifier, tag=tag)
            return tag

        if self.treeWidget.hasFocus():
            selected_item: QTreeWidgetItem = self.treeWidget.currentItem()
            if selected_item is not None:
                tag = update_node(selected_item.text(1))
                if tag.favorite:
                    self.treeWidget.currentItem().setIcon(0, QIcon(":/icons/images/favorite.png"))
                else:
                    self.treeWidget.currentItem().setIcon(0, QIcon(""))
        elif self.tableWidget.hasFocus():
            current_row: int = self.tableWidget.currentRow()
            if current_row > -1:
                tag = update_node(self.url_list[current_row])
                if tag.favorite:
                    self.tableWidget.item(current_row, 0).setIcon(QIcon(":/icons/images/favorite.png"))
                else:
                    self.tableWidget.item(current_row, 0).setIcon(QIcon(FileTypes[tag.type]))

    def set_node_as_downloaded(self, row: int, column: int):
        item: QTableWidgetItem = self.tableWidget.item(row, column)
        last_state = item.data(LastStateRole)
        current_state = item.checkState()
        if current_state != last_state:
            checked = current_state == Qt.CheckState.Checked
            print(row)
            print(self.url_list)
            #
            node: Node = self.tree.get_node(self.url_list[row])
            # update Downloaded attribute in node
            tag = node.tag
            tag.downloaded = checked
            self.tree.update_node(node.identifier, tag=tag)
            if tag.downloaded:
                self.tableWidget.item(row, 0).setCheckState(Qt.CheckState.Checked)
                # .setIcon(QIcon(":/icons/images/success.png"))
            else:
                self.tableWidget.item(row, 0).setCheckState(Qt.CheckState.Unchecked)

    def show_all_favorites(self):
        if self.favorite_group_button.isChecked() and self.favorites_group_window is None:
            self.favorites_group_window = FavoritesGroup(self)
            self.addDockWidget(
                Qt.DockWidgetArea.RightDockWidgetArea, self.favorites_group_window)
            self.favorites_group_window.load(self.tree)
        else:
            self.favorites_group_window.close()
            self.removeDockWidget(self.favorites_group_window)
            self.favorites_group_window = None

    def show_hide_search_widget(self):
        if self.tree.size(0):
            self.clear_table()
            is_visible = self.search_container.isVisible()
            search_mode = self.search_button.isChecked()
            # set horizontal header
            if search_mode:
                # search mode
                self.tableWidget.setColumnCount(5)
                self.tableWidget.setHorizontalHeaderLabels(
                    ["", "Nombre", "Ruta", "Tamaño", "Fecha de modificación"])
            else:
                # normal mode
                self.tableWidget.setColumnCount(4)
                self.tableWidget.setHorizontalHeaderLabels(
                    ["", "Nombre", "Tamaño", "Fecha de modificación"])
            self.search_container.setVisible(not is_visible)
            self.dockWidget.setVisible(is_visible)
            if self.favorites_group_window is not None:
                self.favorites_group_window.setVisible(is_visible)
            self.search_input.setFocus()
        else:
            self.search_button.setChecked(False)

    def deep_search(self):
        text = self.search_input.text()
        result = search(self.tree, text)
        self.state_label.setText(f"Resultados: {len(result)}")
        #
        self.clear_table()
        #
        # fill table
        for node in result:
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            if isinstance(node.tag, FileNode):
                icon_item = QTableWidgetItem()
                pixmap = QPixmap(FileTypes[node.tag.type])
                pixmap = pixmap.scaled(AppSettings.ICON_SIZE, AppSettings.ICON_SIZE)
                icon = QIcon(pixmap)
                icon_item.setIcon(icon)
                self.tableWidget.setItem(row, 0, icon_item)
                self.tableWidget.setItem(
                    row, 1, QTableWidgetItem(node.tag.filename))
                self.tableWidget.setItem(
                    row, 2, QTableWidgetItem(node.identifier))
                self.tableWidget.setItem(
                    row, 3, QTableWidgetItem(nz(node.tag.size)))
                self.tableWidget.setItem(row, 4, QTableWidgetItem(
                    node.tag.modification_date.strftime(AppSettings.DATE_FORMAT)))
                # add to urls to list
                self.url_list.append(node.tag.href)
            else:
                icon_item = QTableWidgetItem()
                pixmap = QPixmap(":/icons/images/folder.png")
                pixmap = pixmap.scaled(AppSettings.ICON_SIZE, AppSettings.ICON_SIZE)
                icon = QIcon(pixmap)
                icon_item.setIcon(icon)
                self.tableWidget.setItem(row, 0, icon_item)
                self.tableWidget.setItem(
                    row, 1, QTableWidgetItem(str(node.tag)))
                self.tableWidget.setItem(
                    row, 2, QTableWidgetItem(node.identifier))
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
        self.message_label.setVisible(is_empty)

    def load_local_repo(self):
        # load serialized tree file
        try:
            print(f"Cargando archivo {Paths.TREE_DATA_FILE_NAME}")
            self.tree = load_all_dirs_n_files_tree()
            print("Llenando árbol...")
            self.fill_tree(None, self.tree.get_node(self.tree.root))
            return True
        except TreeFileDoesntExistException as e:
            print(f"\tTarea fallida [{Paths.TREE_DATA_FILE_NAME}]")
            print("\t" + str(e.args[0]))
            #
            self.read_html_file()

    def read_html_file(self):
        if not self.work_in_progress:
            print(f"Leyendo archivo {Paths.DIRS_FILE_NAME}")
            try:
                # change state
                self.set_work_in_progress(True)
                self.show_hide_message(True)
                #
                self.thread = SubTaskThread()
                self.thread.info_signal.connect(
                    lambda text: self.state_label.setText(text))
                self.thread.error_signal.connect(self.error_read_html_fil)
                self.thread.progress_signal.connect(
                    lambda progress, speed, left_time: self.set_progress(progress, None, left_time,
                                                                         text="Tiempo restante"))
                self.thread.finish_signal.connect(self.success_read_html_fil)
                thread = threading.Thread(target=self.thread.read_html_file)
                thread.start()
            except Exception as e:
                print(f"\tTarea fallida [{Paths.DIRS_FILE_NAME}]")
                print("\t" + str(e.args))
                if isinstance(e, DirsFileDoesntExistException):
                    self.state_label.setText(str(e.args))
                    return
                self.message_label.setText(
                    "No hay datos guardados localmente.\nSi está conectado a Internet, presione el botón 'Descargar repositorio remoto' para obtener el fichero de directorios del FTP e iniciar la exploración")
                self.error(
                    f"Leyendo el archivo '{Paths.DIRS_FILE_NAME}'", "Error de funcionamiento", e)
        else:
            self.notificate_work_in_progress()

    def success_read_html_fil(self, tree):
        self.state_label.setText("Datos cargados")
        self.set_work_in_progress(False)
        self.show_hide_message(False)
        #
        self.tree = tree
        #
        self.check_tree_is_empty()
        #
        self.fill_tree(None, self.tree.get_node(self.tree.root))

    def error_read_html_fil(self, error):
        message = NO_LOCAL_DATA
        if isinstance(error, DirsFileDoesntExistException):
            self.state_label.setText(error.args[0])
        else:
            message = FAIL_LOADING_DIR_FILE
            self.error(f"Leyendo el archivo '{Paths.DIRS_FILE_NAME}'",
                       "No se pudo cargar los datos del archivo", error)
        self.set_work_in_progress(False)
        self.show_hide_message(True, message)

    def set_progress(self, percent: int, speed, left_time, text=""):
        self.progress.setValue(percent)
        state_text = text
        if speed is not None:
            state_text += f" {nz(speed)}/s"
        if left_time is not None:
            state_text += f" {nd(left_time)}"
        self.state_label.setText(state_text)

    def set_work_in_progress(self, b):
        self.progress_container.setVisible(b)
        self.progress.setValue(0 if b else 100)
        self.work_in_progress = b

    def show_hide_message(self, b, text=LOADING_DIR_FILE):
        self.message_label.setVisible(b)
        self.message_label.setText(text)
        self.treeWidget.setVisible(not b)
        self.tableWidget.setVisible(not b)

    def notificate_work_in_progress(self):
        QMessageBox.information(self, "Información",
                                "Espere a que termine la tarea actual para proceder a realizar una nueva")

    def download_file(self):
        '''
        [DEPREACATED] Run a download thread
        '''
        i = self.tableWidget.currentRow()
        if i > -1:
            try:
                href = self.url_list[i]
                #
                node: Node = self.tree.get_node(href)
                if node is None:
                    raise FileNotFounded(f"No se encontró '{href}'")
                file: FileNode = node.tag
                #
                print(f"Descargando archivo {file.filename}")
                #
                self.set_work_in_progress(True)
                self.thread = SubTaskThread()
                self.thread.info_signal.connect(
                    lambda text: self.state_label.setText(text))
                self.thread.progress_signal.connect(
                    lambda progress, speed, left_time: self.set_progress(progress, speed, left_time,
                                                                         text="Descargando"))
                self.thread.error_signal.connect(lambda error: self.error(
                    "Descargando el archivo", "La descarga no fue exitosa", error))
                self.thread.finish_signal.connect(
                    lambda foo: self.success_file_download())
                thread = threading.Thread(
                    target=self.thread.download_file, args=(file,))
                thread.start()
            except Exception as e:
                print(f"\tDescarga fallida [{file}]")
                print("\t" + str(e.args))
                self.state_label.setText(ExceptionMessages.CONNECTION_FAIL)

    def add_to_download_queue(self):
        '''
        Add file or folder content to download queue in the Download Manager
        '''
        if self.treeWidget.hasFocus():
            selected_item: QTreeWidgetItem = self.treeWidget.currentItem()
            if selected_item is not None:
                #
                files_list = []
                for url in self.url_list:
                    node: Node = self.tree.get_node(url)
                    if node is not None:
                        file: FileNode = node.tag
                        files_list.append(file)
                #
                self.activate_download_manager_window()
                self.download_manager_window.add_collection_to_queue(files_list)
                self.download_manager_window.show_and_load()
        elif self.tableWidget.hasFocus():
            i: int = self.tableWidget.currentRow()
            if i > -1:
                try:
                    href = self.url_list[i]
                    #
                    node: Node = self.tree.get_node(href)
                    if node is None:
                        raise FileNotFounded(f"No se encontró '{href}'")
                    file: FileNode = node.tag
                    #
                    self.activate_download_manager_window()
                    self.download_manager_window.add_file_to_queue(file)
                    self.download_manager_window.show_and_load()
                except Exception as e:
                    print(f"\tDescarga fallida [{file}]")
                    print("\t" + str(e.args))
                    self.state_label.setText(ExceptionMessages.CONNECTION_FAIL)

    def request_remote_repo_file(self):
        if not self.work_in_progress:
            print(f"Solicitando archivo {Paths.LISTADO_HTML_FILE}")
            try:
                self.set_work_in_progress(True)
                self.thread = SubTaskThread()
                self.thread.info_signal.connect(
                    lambda text: self.state_label.setText(text))
                self.thread.error_signal.connect(
                    lambda error: self.request_remote_repo_file_error(error=error))
                self.thread.finish_signal.connect(
                    lambda response: self.download_remote_repo(response))
                thread = threading.Thread(target=self.thread.request_file)
                thread.start()
            except Exception as e:
                print(f"\tTarea fallida [{Paths.DIRS_FILE_NAME}]")
                print("\t" + str(e.args))
                self.state_label.setText(ExceptionMessages.CONNECTION_FAIL)
        else:
            self.notificate_work_in_progress()

    def request_remote_repo_file_error(self, error):
        self.set_work_in_progress(False)
        self.error("Solicitando archivo remoto", "La petición no se realizó con éxito",
                   error)

    def download_remote_repo(self, file: FileNode):
        # get last modified setting
        last_modified = GENERAL_SETTINGS.value("last_modification_date", type=str)
        # get last modified date from header
        current_last_modified = file.modification_date
        #
        file_size = file.size
        #
        if last_modified:
            last_modified = datetime.fromisoformat(last_modified)
        else:
            last_modified = current_last_modified

        #

        def run_thread():
            print(f"Descargando archivo {Paths.LISTADO_HTML_FILE}")
            try:
                self.set_work_in_progress(True)
                self.thread = SubTaskThread()
                self.thread.info_signal.connect(
                    lambda text: self.state_label.setText(text))
                self.thread.progress_signal.connect(
                    lambda progress, speed, left_time: self.set_progress(progress, speed, left_time,
                                                                         text="Descargando"))
                self.thread.error_signal.connect(lambda error: self.error(
                    "Descargando el archivo", "La descarga no fue exitosa", error))
                self.thread.finish_signal.connect(
                    lambda foo: self.success_listado_file_download(current_last_modified))
                thread = threading.Thread(target=self.thread.download_file, args=(FileNode(
                    filename=Paths.DIRS_FILE_NAME, modification_date=current_last_modified, size=0,
                    href=Paths.LISTADO_HTML_FILE, type=AppEnums.TEXT), Paths.DATA_FOLDER,))
                thread.start()
            except Exception as e:
                print(f"\tTarea fallida [{Paths.DIRS_FILE_NAME}]")
                print("\t" + str(e.args))
                self.state_label.setText(ExceptionMessages.CONNECTION_FAIL)

        # # convert last_modification_date in datetime
        # current_last_modified = datetime.strptime(current_last_modified, DATE_FROM_SERVER_FORMAT)
        # if file has been updated
        if current_last_modified != last_modified:
            q = QMessageBox.question(self, "Información del repositorio",
                                     f"Los datos fueron actualizados el día {current_last_modified}\nTamaño del archivo: {nz(file_size)}\n¿Desea descargar los nuevos datos?",
                                     QMessageBox.Yes | QMessageBox.No)
            if q == QMessageBox.Yes:
                run_thread()
            else:
                self.set_work_in_progress(False)
        else:
            run_thread()

    def success_file_download(self):
        self.set_work_in_progress(False)

    def success_listado_file_download(self, last_modification_date):
        self.set_work_in_progress(False)
        # save last modification date setting
        save_settings("last_modification_date", str(last_modification_date))
        #
        self.read_html_file()
        self.check_tree_is_empty()

    def show_file_details_on_state_bar(self, item: QTableWidgetItem):
        i = item.row()
        is_searching = self.search_button.isChecked()
        size = self.tableWidget.item(i, 3 if is_searching else 2).text()
        modification_date = self.tableWidget.item(
            i, 4 if is_searching else 3).text()
        # set path in statusbar
        self.state_label.setText(
            f"Tamaño:{size}, Fecha de modificación:{modification_date}")  # , Ruta:{self.tableWidget.item(i, 2).text() if is_searching else self.url_list[i]}")

    def open_in_explorer(self):
        i = self.tableWidget.currentRow()
        # get node
        node: Node = self.tree.get_node(self.url_list[i])
        #
        is_searching = self.search_button.isChecked()
        # is file is text or an image
        if node.tag.type == AppEnums.IMAGE or node.tag.type == AppEnums.TEXT:
            # download it
            self.get_light_weight_file(type=node.tag.type, url=node.tag.href)
        else:
            # else, open it in explorer
            webbrowser.open(self.tableWidget.item(i, 2).text() if is_searching else self.url_list[i], new=1,
                            autoraise=False)

    def show_in_tree(self, id):
        # get node
        goal_node: Node = self.tree.get_node(id)
        goal_depth = self.tree.depth(goal_node)
        depth = 0
        while depth != goal_depth:
            parent: Node = self.tree.ancestor(id, depth)
            # item_text = parent.tag.name if not parent.is_root() else "Visuales UCLV"
            print(parent.identifier)
            depth += 1
            # self.treeWidget.ex(parent.tag.name)
        # parent: Node = self.tree.parent(id)
        # print(parent.tag.name)
        # items = self.treeWidget.findItems(parent.tag.name, Qt.MatchContains, 0)
        # print(items)

    def get_light_weight_file(self, type: str, url: str):
        self.set_work_in_progress(True)
        #
        self.thread = SubTaskThread()
        self.thread.info_signal.connect(
            lambda text: self.state_label.setText(text))
        # self.thread.progress_signal.connect(self.set_progress)
        self.thread.error_signal.connect(
            lambda error: self.get_light_weight_file_error(error=error))
        self.thread.finish_signal.connect(
            lambda data: self.show_preview_dock(type=type, data=data))
        thread = threading.Thread(target=self.thread.get_light_weight_file,
                                  args=(url,))
        thread.start()

    def get_light_weight_file_error(self, error):
        self.set_work_in_progress(False)
        self.error("Solicitando archivo remoto", "La petición no concluyó exitosamente", error)

    def show_preview_dock(self, type: str, data):
        self.set_work_in_progress(False)
        if self.preview_dock is None:
            self.preview_dock = PreviewDock(self)
            self.addDockWidget(
                Qt.DockWidgetArea.RightDockWidgetArea, self.preview_dock)
        self.preview_dock.load(type=type, data=data)

    def show_main_table_context_menu(self, position):
        idx = self.tableWidget.currentRow()
        if idx != -1:
            menu = QMenu()
            # copy url to clipboard
            copy_url_action = QAction("Copiar URL", menu)

            def copy_url():
                text = self.tableWidget.item(idx, 2).text() if self.search_button.isChecked() else self.url_list[idx]
                clipboard = QApplication.clipboard()
                clipboard.clear(mode=QClipboard.Clipboard)
                clipboard.setText(text, QClipboard.Clipboard)

            copy_url_action.triggered.connect(copy_url)
            menu.addAction(copy_url_action)
            # search table
            if self.search_button.isChecked():
                show_location_action = QAction("Mostrar ubicación", menu)

                def show_location():
                    # self.locate(self.tableWidget.item(idx, 2).text())
                    pass

                show_location_action.triggered.connect(show_location)
                menu.addAction(show_location_action)  #
            try:
                menu.exec(self.tableWidget.viewport().mapToGlobal(position))
            except Exception as e:
                self.error("Mostrando menú conceptual", "Ver detalles", e)

    def async_get_page(self, selected_item):
        if not self.work_in_progress:
            folder_path = selected_item.text(1) if isinstance(
                selected_item, QTreeWidgetItem) else selected_item.text()
            # get node by column 1 text in QTreeWidgetItem
            node: Node = self.tree.get_node(folder_path)
            #
            if not has_children(self.tree, node):
                try:
                    if not node.tag.is_empty:
                        self.set_work_in_progress(True)
                        self.thread = SubTaskThread()
                        self.thread.info_signal.connect(
                            lambda text: self.state_label.setText(text))
                        self.thread.progress_signal.connect(self.set_progress)
                        self.thread.error_signal.connect(lambda error: self.error(
                            "Solicitando página remota", "La petición no concluyó exitosamente", error))
                        self.thread.finish_signal.connect(
                            lambda children: self.add_children_to_item(children=children, node=node,
                                                                       selected_item=selected_item))
                        thread = threading.Thread(target=self.thread.get_page,
                                                  args=(folder_path, node.identifier,))
                        thread.start()
                except Exception as e:
                    print(e.args)
                    self.state_label.setText(ExceptionMessages.CONNECTION_FAIL)
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
        # save tree
        self.state_label.setText("Guardando datos locales...")
        save_all_dirs_n_files_tree(self.tree)
        self.state_label.setText("Datos locales guardados")
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
        self.tableWidget.setHorizontalHeaderLabels(
            ["", "Nombre", "Tamaño", "Fecha de modificación"])
        # fill table
        for node in children:
            node = node.tag
            if isinstance(node, FileNode):
                row = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row)
                icon_item = QTableWidgetItem()
                icon_item.setCheckState(Qt.CheckState.Checked if node.downloaded else Qt.CheckState.Unchecked)
                if node.favorite:
                    pixmap = QPixmap(":/icons/images/favorite.png")
                else:
                    pixmap = QPixmap(FileTypes[node.type])
                pixmap = pixmap.scaled(AppSettings.ICON_SIZE, AppSettings.ICON_SIZE)
                icon = QIcon(pixmap)
                icon_item.setIcon(icon)
                self.tableWidget.setItem(row, 0, icon_item)
                self.tableWidget.setItem(row, 1, QTableWidgetItem(str(node)))
                self.tableWidget.setItem(
                    row, 2, QTableWidgetItem(nz(node.size)))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(
                    node.modification_date.strftime(AppSettings.DATE_FORMAT)))

                # add to urls to list
                self.url_list.append(node.href)
        self.tableWidget.resizeColumnsToContents()

    def fill_node(self, expanded_item: QTreeWidgetItem):
        self.fill_tree(expanded_item, self.tree.get_node(
            expanded_item.text(1)))

    def error(self, place: str, text: str, exception: Exception = None):
        self.set_work_in_progress(False)
        self.state_label.setText(ExceptionMessages.AN_ERROR_WAS_OCURRED)
        #
        msg = QMessageBox(self)
        msg.setIcon(msg.Icon.Critical)
        msg.setBaseSize(300, 100)
        msg.setWindowTitle("Error")
        msg.setText(f"* {place} *")
        msg.setInformativeText(f"-> {text}")
        if exception is not None:
            msg.setDetailedText(
                f"[{exception.__class__.__name__}] {str(exception.args)}")
        msg.exec_()

    def fill_tree(self, parent: QTreeWidgetItem, node: Node):
        '''
        Add children to QTreeWidget
        '''
        if parent is None:
            self.treeWidget.clear()
            qchild = QTreeWidgetItem(["Visuales UCLV", str(node.tag) + "/"])
            root_item = QTreeWidgetItem(["-", "None"])
            qchild.addChild(root_item)
            self.treeWidget.insertTopLevelItem(0, qchild)
            # expand root node
            self.treeWidget.setCurrentItem(root_item)  # expand(self.treeWidget.indexFromItem(root_item, 0))
            return
        if not node.is_leaf():
            if parent.child(0).text(1) == "None":
                # remove invisible item
                parent.removeChild(parent.child(0))
                for child in self.tree.children(node.identifier):
                    if not isinstance(child.tag, FileNode):
                        qchild = QTreeWidgetItem(
                            [str(child.tag), child.identifier])
                        # set favorite icon
                        if child.tag.favorite:
                            qchild.setIcon(
                                0, QIcon(":/icons/images/favorite.png"))
                        # if child is not empty, add an invisible item
                        if not child.is_leaf():
                            qchild.addChild(QTreeWidgetItem(["-", "None"]))
                        parent.addChild(qchild)

    def closeEvent(self, event) -> None:
        if not self.work_in_progress:
            # save_all_dirs_n_files_tree(self.tree)
            event.accept()
        else:

            q = QMessageBox.question(self, "Información",
                                     "No debe cerrar el programa aún porque hay una tarea activa. Si el programa se cerrase, la integridad de los datos pudiera perderse y consigo su respositorio local.\n¿Está seguro de cerrar el programa?",
                                     QMessageBox.Yes | QMessageBox.No)
            if q == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

    def show_about(self):
        self.about_dialog = AboutDialog()
        self.about_dialog.show()


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

    send_to_log(msg, "ERROR")


sys.excepthook = excepthook

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # ssl cert file
    os.environ["SSL_CERT_FILE"] = certifi.where()
    # app dark style
    import qdarkstyle

    app.setStyleSheet(qdarkstyle.load_stylesheet())
    # start
    visuales = VisualesUCLV()
    visuales.show()
    app.exec()
