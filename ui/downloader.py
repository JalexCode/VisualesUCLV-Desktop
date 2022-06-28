import subprocess
import threading
from datetime import datetime
from typing import List

import psutil
from PyQt5.QtCore import QTimer, QTime, QUrl
from PyQt5.QtGui import QIcon, QPixmap, QCloseEvent
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QProgressBar, QToolButton, QLineEdit, QWidget, QHBoxLayout, \
    QLabel, QFileDialog, QMessageBox
from pySmartDL import SmartDL

from model.threads import DownloadThread
from ui.downloader_ui import Ui_MainWindow
from util.downloader_settings import DOWNLOADER_SETTINGS, save_settings
from util.flags import *
from util.util import *
import urllib.parse


class DownloadManager(Ui_MainWindow, QMainWindow):
    """
    A download manager
    """

    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.setupUi(self)
        #
        self._parent = parent
        #
        self._files: List[FileNode] = []
        self._downloaded_files: List[FileNode] = []
        #
        self.total_size = 0
        self.__state = ""
        #
        self.timer = QTimer()
        self.timer.timeout.connect(self.set_download_time)
        self.time = QTime(0, 0, 0)
        #
        self.player = QMediaPlayer(self)
        #
        self.load_preferences()
        self.init()
        self.connections()

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value: str):
        self.__state = value

    def show_and_load(self):
        self.show()
        self.fill_table()
        self.get_free_space()

    def add_file_to_queue(self, url: FileNode):
        if url not in self._files:
            self._files.append(url)

    def add_collection_to_queue(self, urls: List[FileNode]):
        while len(urls):
            url = urls.pop(0)
            if url not in self._files:
                self._files.append(url)

    def init(self):
        #
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(
            ["", "Nombre", "Estado", "Progreso", "Velocidad", "Tamaño", "Tiempo restante", "Agregada"])
        #
        self.setWindowTitle(AppInfo.NAME + " Download Manager")
        self.toolBar.setWindowTitle("Barra de herramientas")
        # state label
        self.state_label = QLabel("")
        self.statusbar.addWidget(self.state_label)
        #
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nombre")
        self.search_input.setClearButtonEnabled(True)
        #
        self.search_action_button = QToolButton()
        self.search_action_button.setText("Buscar")
        # self.search_action_button.clicked.connect()
        #
        self.search_container = QWidget()
        self.layout = QHBoxLayout(self.search_container)
        self.layout.addWidget(self.search_input)
        self.layout.addWidget(self.search_action_button)
        self.search_container.setLayout(self.layout)
        self.search_container.setVisible(False)
        self.statusbar.addPermanentWidget(self.search_container)
        #
        self.start_all_tasks_button = QToolButton()
        self.start_all_tasks_button.setText(
            "Iniciar/Reanudar")
        self.start_all_tasks_button.setToolTip(
            "Inicia o reanuda todas las descargas")
        self.start_all_tasks_button.setIcon(
            QIcon(":/icons/images/play.png"))
        self.start_all_tasks_button.clicked.connect(
            lambda: self.start_all_tasks())
        self.toolBar.addWidget(self.start_all_tasks_button)
        #
        self.pause_button = QToolButton()
        self.pause_button.setText("Pausar")
        self.pause_button.setToolTip(
            "Pausa todas las tareas")
        self.pause_button.setIcon(
            QIcon(":/icons/images/pause.png"))

        def set_pause():
            self.__state = PAUSE

        self.pause_button.clicked.connect(lambda: set_pause())
        self.toolBar.addWidget(self.pause_button)
        #
        self.stop_button = QToolButton()
        self.stop_button.setText("Detener todas")
        self.stop_button.setToolTip(
            "Detiene todas las tareas")
        self.stop_button.setIcon(QIcon(":/icons/images/stop.png"))

        def set_stop():
            self.__state = STOP

        self.stop_button.clicked.connect(
            lambda: set_stop())
        self.toolBar.addWidget(self.stop_button)
        #
        self.toolBar.addSeparator()
        #
        self.delete_from_list_button = QToolButton()
        self.delete_from_list_button.setText("Eliminar elementos seleccionados de la lista")
        self.delete_from_list_button.setToolTip(
            "Elimina de la cola de descarga los elementos seleccionados")
        self.delete_from_list_button.setIcon(QIcon(":/icons/images/delete.png"))
        self.delete_from_list_button.clicked.connect(self.delete_from_list)
        self.toolBar.addWidget(self.delete_from_list_button)
        #
        self.toolBar.addSeparator()
        #
        self.search_button = QToolButton()
        self.search_button.setText("Buscar")
        self.search_button.setToolTip(
            "Buscar elementos en la cola de descarga")
        self.search_button.setIcon(QIcon(":/icons/images/search.png"))
        self.search_button.setCheckable(True)
        # self.search_button.clicked.connect(self.show_hide_search_widget)
        self.toolBar.addWidget(self.search_button)
        #
        self.load_txt_button = QToolButton()
        self.load_txt_button.setText("Cargar archivo TXT")
        self.load_txt_button.setToolTip(
            "Buscar y cargar enlaces de archivos remotos")
        self.load_txt_button.setIcon(QIcon(":/icons/images/link.png"))
        self.load_txt_button.clicked.connect(self.load_txt)
        self.toolBar.addWidget(self.load_txt_button)
        #
        self.export_as_txt_button = QToolButton()
        self.export_as_txt_button.setText("Exportar como TXT")
        self.export_as_txt_button.setToolTip(
            "Exporta todos los enlaces de la carpeta hacia un archivo de texto plano")
        self.export_as_txt_button.setIcon(QIcon(":/icons/images/txt.png"))
        self.export_as_txt_button.clicked.connect(self.export_as_txt)
        self.toolBar.addWidget(self.export_as_txt_button)
        #
        self.open_destiny_button = QToolButton()
        self.open_destiny_button.setText("Abrir carpeta destino")
        self.open_destiny_button.setToolTip(
            "Abre la carpeta destino")
        self.open_destiny_button.setIcon(QIcon(":/icons/images/folder.png"))
        self.open_destiny_button.clicked.connect(
            lambda: self.open_destiny(DOWNLOADER_SETTINGS.value("destiny_folder", type=str), True, False))
        self.toolBar.addWidget(self.open_destiny_button)
        #

    def delete_from_list(self):
        # selected indexes
        table_items = self.tableWidget.selectedIndexes()  # selectedItems()
        #
        if not table_items: return
        # sort
        table_items.sort(key=lambda item: item.row(), reverse=True)
        a = QMessageBox.warning(self, "Eliminar elementos seleccionados",
                                "¿Realmente desea eliminar los elementos seleccionados de la lista?",
                                QMessageBox.Ok | QMessageBox.Cancel)
        if a == QMessageBox.Ok:
            # delete from self._file
            selected_size = 0
            for i in table_items:
                selected_size += self._files[i.row()].size
            for i in table_items:
                self._files.pop(i.row())
            # update total size flag
            self.total_size -= selected_size
            # update total size label
            self.total_size_queue_label.setText(f"Tamaño total: {nz(self.total_size)}")
            # delete from tableWidget
            for item in table_items:
                row = item.row()
                self.tableWidget.removeRow(row)

    def export_as_txt(self):
        """
        Open a Save File Dialog to export file links into a txt file
        :return:
        """
        if self._files:
            file, _ = QFileDialog.getSaveFileName(self, "Exportar enlaces como archivo de texto", "",
                                                  "Archivo de texto (*.txt)")
            if file:
                txt = "\n".join([filenode.href for filenode in self._files])
                with open(file, mode="w", encoding="UTF-8") as txt_file:
                    txt_file.write(txt)

    def load_preferences(self):
        # ---------------------------------------------------------#
        destiny_folder = DOWNLOADER_SETTINGS.value("destiny_folder", type=str)
        self.destiny_folder_input.setText(destiny_folder)
        # ---------------------------------------------------------#
        max_threads = DOWNLOADER_SETTINGS.value("max_threads", type=int)
        self.max_threads_threads.setValue(max_threads)
        # ---------------------------------------------------------#
        attemps_limit = DOWNLOADER_SETTINGS.value("attemps_limit", type=int)
        self.attemps_limit_spin.setValue(attemps_limit)
        # ---------------------------------------------------------#
        alert_on_finish = DOWNLOADER_SETTINGS.value("alert_on_finish", type=bool)
        self.alert_when_finish_checkb.setChecked(alert_on_finish)
        # ---------------------------------------------------------#
        alert_sound = DOWNLOADER_SETTINGS.value("alert_sound", type=str)
        self.sound_path_input.setText(alert_sound)
        # ---------------------------------------------------------#
        if_file_exists = DOWNLOADER_SETTINGS.value("if_file_exists", type=int)
        self.if_file_already_exists_combo.setCurrentIndex(if_file_exists)
        # ---------------------------------------------------------#
        on_stop = DOWNLOADER_SETTINGS.value("on_stop", type=int)
        self.when_downloads_stops_combo.setCurrentIndex(on_stop)
        # ---------------------------------------------------------#

    def connections(self):
        self.change_destiny_button.clicked.connect(self.change_dest_folder)
        self.change_song_button.clicked.connect(self.change_alert_sound)
        # settings
        self.max_threads_threads.valueChanged.connect(
            lambda value: save_settings("max_threads", value))
        #
        self.attemps_limit_spin.valueChanged.connect(lambda value: save_settings("attemps_limit", value))
        #
        self.if_file_already_exists_combo.currentIndexChanged.connect(
            lambda index: save_settings("if_file_exists", index))
        #
        self.when_downloads_stops_combo.currentIndexChanged.connect(
            lambda index: save_settings("on_stop", index))

        #
        def open_file():
            i = self.history_table.currentRow()
            self.open_destiny(file_path=self.history_table.item(i, 2).text(), folder=False, highlight=True)
        self.history_table.itemDoubleClicked.connect(lambda: open_file())

    def set_download_time(self):
        """
        Increase timer's time
        :return:
        """
        self.time = self.time.addSecs(1)
        self.download_time_label.setText(f"Tiempo transcurrido: {self.time.toString('hh:mm:ss')}")

    def get_free_space(self):
        # get destiny path
        path = DOWNLOADER_SETTINGS.value("destiny_folder", type=str)
        # get drive letter
        drive = os.path.splitdrive(path)[0]
        # print(drive)
        disk_usage = psutil.disk_usage(drive)
        # print("Espacio total: {:.2f} GB.".format(to_gb(disk_usage.total)))
        # print("Espacio libre: {:.2f} GB.".format(to_gb(disk_usage.free)))
        # print("Espacio usado: {:.2f} GB.".format(to_gb(disk_usage.used)))
        # print("Porcentaje de espacio usado: {}%.".format(disk_usage.percent))
        free = disk_usage.free
        self.free_space.setText(f"Espacio disponible: {nz(free)}")
        self.free_space.setStyleSheet("color:lightgreen;")
        if self.total_size >= free:
            self.free_space.setStyleSheet("color:red;")

    def fill_table(self):
        self.clear_table()
        for file in self._files:
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            # set file type image
            self.set_table_widget_item_pixmap(row, file.type if file.type else AppEnums.UNKNOWN)
            #
            self.tableWidget.setItem(row, 1, QTableWidgetItem(file.filename))
            self.tableWidget.setItem(row, 2, QTableWidgetItem("-"))
            # progress
            self.tableWidget.setCellWidget(row, 3, QProgressBar())
            self.tableWidget.cellWidget(row, 3).setFormat("Esperando...")
            #
            self.tableWidget.setItem(row, 4, QTableWidgetItem("-"))
            self.on_file_size_deteted(row, file.size)
            self.tableWidget.setItem(row, 6, QTableWidgetItem("-"))
            self.tableWidget.setItem(row, 7, QTableWidgetItem(datetime.now().strftime(AppSettings.DATE_FORMAT)))
        #
        self.tableWidget.resizeColumnsToContents()
        pass

    def add_2_table(self, file: FileNode):
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        #
        self.set_table_widget_item_pixmap(row, file.type if file.type else AppEnums.UNKNOWN)
        self.tableWidget.setItem(row, 1, QTableWidgetItem(file.filename))
        self.tableWidget.setItem(row, 2, QTableWidgetItem("-"))
        # progress
        self.tableWidget.setCellWidget(row, 3, QProgressBar())
        self.tableWidget.cellWidget(row, 3).setFormat("Esperando...")
        #
        self.tableWidget.setItem(row, 4, QTableWidgetItem("-"))
        self.tableWidget.setItem(row, 5, QTableWidgetItem(nz(file.size)))
        self.tableWidget.setItem(row, 6, QTableWidgetItem("-"))
        self.tableWidget.setItem(row, 7, QTableWidgetItem(datetime.now().strftime(AppSettings.DATE_FORMAT)))
        #
        self.tableWidget.resizeColumnsToContents()

    def clear_table(self):
        # clear table
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)

    def start_task(self):
        pass

    def start_all_tasks(self):
        if self.__state == PAUSE:
            self.__state = REANUDE
        else:
            #
            thread = DownloadThread(self)
            thread.error_signal.connect(self.on_error)
            thread.progress_signal.connect(self.on_download_progress_changed)
            thread.file_size_signal.connect(self.on_file_size_deteted)
            thread.file_type_signal.connect(self.on_file_type_detected)
            thread.finish_one_task_signal.connect(self.on_finish_one)
            thread.finish_all_signal.connect(self.on_finish_all)
            #
            # with ThreadPoolExecutor(max_workers=DOWNLOADER_SETTINGS.value("max_workers", type=int)) as executor:
            #     for i in range(len(self._files)):
            #         #
            #         executor.submit(fn=thread.download_async, args=(i,self._files[i], DOWNLOAD_DIR,))
            #         print("ASD")
            thread = threading.Thread(target=thread.download,
                                      args=(self._files, DOWNLOADER_SETTINGS.value("destiny_folder", type=str),))
            thread.start()
            #
            self.timer.start(1000)

    def on_download_progress_changed(self, idx: int, state: str, dl_size: str, progress: int, speed: str,
                                     estimated_time: str):
        # update item data on table
        self.tableWidget.setItem(idx, 2, QTableWidgetItem(state))
        self.tableWidget.cellWidget(idx, 3).setFormat(f"{dl_size} (%p%)")
        self.tableWidget.cellWidget(idx, 3).setValue(progress)
        self.tableWidget.setItem(idx, 4, QTableWidgetItem(speed))
        self.tableWidget.setItem(idx, 6, QTableWidgetItem(estimated_time))
        # check free space on disk
        self.get_free_space()

    def on_error(self, file: FileNode, error: Exception):
        row = self.errors_table.rowCount()
        self.errors_table.insertRow(row)
        self.errors_table.setItem(row, 0, QTableWidgetItem(datetime.now().strftime(AppSettings.DATE_FORMAT)))
        self.errors_table.setItem(row, 1, QTableWidgetItem(file.filename))
        self.errors_table.setItem(row, 2, QTableWidgetItem(f"[{error.__class__.__name__}] {str(error.args)}"))
        #
        self.tableWidget.resizeColumnsToContents()
        #
        self.tableWidget.removeRow(0)
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        # set file type image
        self.set_table_widget_item_pixmap(row, file.type if file.type else AppEnums.UNKNOWN)
        #
        self.tableWidget.setItem(row, 1, QTableWidgetItem(file.filename))
        self.tableWidget.setItem(row, 2, QTableWidgetItem("-"))
        # progress
        self.tableWidget.setCellWidget(row, 3, QProgressBar())
        self.tableWidget.cellWidget(row, 3).setFormat("Esperando...")
        #
        self.tableWidget.setItem(row, 4, QTableWidgetItem("-"))
        self.on_file_size_deteted(row, file.size)
        self.tableWidget.setItem(row, 6, QTableWidgetItem("-"))
        self.tableWidget.setItem(row, 7, QTableWidgetItem(datetime.now().strftime(AppSettings.DATE_FORMAT)))

    def on_finish_one(self, idx: int, state: str, file: FileNode, download_data: SmartDL):
        """
        Receives data from finish_one_task_signal
        :param filename:
        :param download_data:
        :return:
        """
        #
        self.timer.stop()
        self.time = QTime(0, 0, 0)
        #
        self._downloaded_files.append(file)
        #
        self.tableWidget.setItem(idx, 2, QTableWidgetItem(state))
        self.tableWidget.removeRow(idx)
        #
        row: int = self.history_table.rowCount()
        self.history_table.insertRow(row)
        self.history_table.setItem(row, 0, QTableWidgetItem(file.filename))
        self.history_table.setItem(row, 1, QTableWidgetItem(download_data.get_dl_time(human=True)))
        self.history_table.setItem(row, 2, QTableWidgetItem(download_data.get_dest()))
        #
        self.history_table.resizeColumnsToContents()
        #

    def on_finish_all(self):
        """
        Receives data from finish_all_signal
        :return:
        """
        #
        self.timer.stop()
        self.time = QTime(0, 0, 0)
        #
        self.alert()

    def on_file_size_deteted(self, row: int, size: int) -> None:
        """
        Receives data from file_size_signal and update file size in self._files and QTableWidgetItem
        :param row:
        :param size:
        :return:
        """
        # update table item
        self.tableWidget.setItem(row, 5, QTableWidgetItem(nz(size)))
        #
        self.total_size += size
        self.total_size_queue_label.setText(f"Tamaño total: {nz(self.total_size)}")

    def on_file_type_detected(self, row: int, type: str):
        """
        Receives data from file_type_signal [ACTUALLY USELESS]
        :param row:
        :param type:
        :return:
        """
        try:
            if type in FileExtensions["AUDIO"]:
                self._files[row].type = FileTypes.AUDIO
            elif type in FileExtensions["TEXT"]:
                self._files[row].type = FileTypes.TEXT
            elif type in FileExtensions["IMAGE"]:
                self._files[row].type = FileTypes.IMAGE
            elif type in FileExtensions["VND"]:
                self._files[row].type = FileTypes.LAYOUT
            elif type in FileExtensions["APPLICATION"]:
                self._files[row].type = FileTypes.EXEC
            else:
                self._files[row].type = AppEnums.UNKNOWN
            #
            self.set_table_widget_item_pixmap(row, self._files[row].type)
        except Exception as e:
            print(e.args)

    def set_table_widget_item_pixmap(self, row: int, type: str) -> None:
        """
        Sets item icon in download's queue QTableWidget
        :param row:
        :param type:
        :return:
        """
        icon_item = QTableWidgetItem()
        # create pixmap
        pixmap = QPixmap(FileTypes[type])
        # scale pixmap
        pixmap = pixmap.scaled(AppSettings.ICON_SIZE, AppSettings.ICON_SIZE)
        # set icon
        icon = QIcon(pixmap)
        icon_item.setIcon(icon)
        # set item
        self.tableWidget.setItem(row, 0, icon_item)

    def load_txt(self) -> None:
        """
        Open a File Dialog to open a txt file to fill Download Queue
        :return:
        """
        # open file dialog
        location, _ = QFileDialog.getOpenFileName(self, "Seleccione archivos de texto",
                                                  Paths.USER_PATH, "TXT (*.txt)")
        if location:
            with open(location, "r", encoding="UTF-8") as txt:
                content = txt.readlines()
                for url in content:
                    url = url.strip("\n")
                    # parse url to get file name
                    filename = urllib.parse.unquote(os.path.basename(urllib.parse.urlparse(url).path))
                    # build File Node object
                    file_node = FileNode(filename, href=url, type="")
                    # set file type
                    get_file_type(file_node)
                    # add to self._file and self.tableWidget
                    self.add_file_to_queue(file_node)
                    self.add_2_table(file_node)

    def change_dest_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Seleccione una carpeta para almacenar las Descargas")
        if path:
            self.destiny_folder_input.setText(path)
            save_settings("destiny_folder", path)

    def change_alert_sound(self):
        path, _ = QFileDialog.getOpenFileName(self, "Seleccionar un audio", Paths.USER_PATH, "Audio (*.mp3; *.wav; *.ogg)")
        if path:
            self.sound_path_input.setText(path)
            save_settings("alert_sound", path)

    def alert(self):
        alert_on_finish = DOWNLOADER_SETTINGS.value("alert_on_finish", type=bool)
        if alert_on_finish:
            sound = DOWNLOADER_SETTINGS.value("alert_sound", type=str)
            if os.path.exists(sound):
                self.player.setMedia(QMediaContent(QUrl.fromLocalFile(sound)))
                self.player.play()

    def closeEvent(self, event: QCloseEvent) -> None:
        event.ignore()
        self.hide()

    def open_destiny(self, file_path:str, folder=False, highlight=False):
        file_path = file_path.replace("/", "\\")
        print(file_path)
        try:
            CREATE_NO_WINDOW = 0x08000000
            if folder:
                subprocess.Popen(['explorer.exe', file_path],
                                 stderr=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stdin=subprocess.PIPE,
                                 shell=False,
                                 creationflags=CREATE_NO_WINDOW)
            else:
                if highlight:
                    subprocess.Popen(['explorer.exe', '/select,', file_path],
                                     stderr=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stdin=subprocess.PIPE,
                                     shell=False,
                                     creationflags=CREATE_NO_WINDOW)

                else:
                    subprocess.Popen(['cmd', '/C', 'start', file_path, file_path],
                                     stderr=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stdin=subprocess.PIPE,
                                     shell=False,
                                     creationflags=CREATE_NO_WINDOW)
        except Exception as e:
            print(e.args)
            # self.error("Abriendo archivo descargado", e.args)

    def error(self, place: str, text: str, exception: Exception = None):
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
