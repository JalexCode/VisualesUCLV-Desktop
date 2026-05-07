import sys
import asyncio
import traceback
from typing import List, Dict
from PySide6.QtWidgets import (QMainWindow, QApplication, QTreeWidgetItem, QTableWidgetItem,
                             QLineEdit, QToolButton, QToolBar, QMenu, QProgressBar,
                             QMessageBox, QFileDialog, QDialog, QVBoxLayout, QTextEdit, QLabel)
from PySide6.QtCore import Qt, QThread, Signal, Slot, QSize
from PySide6.QtGui import QIcon, QPixmap
from qt_material import apply_stylesheet

from visuales_uclv.presentation.ui.main_ui import Ui_MainWindow
from visuales_uclv.presentation.ui.downloader_ui import Ui_DownloadManager
from visuales_uclv.presentation.about_dialog import AboutDialog
from visuales_uclv.presentation.error_dialog import ErrorDialog
from visuales_uclv.data.repositories.tree_repository import TreeRepository
from visuales_uclv.data.clients.scraper import VisualesScraper
from visuales_uclv.data.clients.downloader import AsyncDownloadManager, DownloadTask
from visuales_uclv.domain.search_engine import SearchEngine
from visuales_uclv.core.config.settings import settings
from visuales_uclv.core.logger.logger import setup_logging, get_logger
from visuales_uclv.domain.models.nodes import FolderNode, FileNode, BaseNode, FileType

# Initialize logger
setup_logging()
logger = get_logger(__name__)

class Worker(QThread):
    finished = Signal(object)
    progress = Signal(int)
    error = Signal(object)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            import inspect
            sig = inspect.signature(self.func)
            if 'progress_callback' in sig.parameters:
                self.kwargs['progress_callback'] = self.progress.emit

            if asyncio.iscoroutinefunction(self.func):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(self.func(*self.args, **self.kwargs))
                loop.close()
            else:
                result = self.func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            logger.error(f"Worker error: {e}\n{traceback.format_exc()}")
            self.error.emit(e)

class PreviewDialog(QDialog):
    def __init__(self, title, content, is_image=False, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(800, 600)
        layout = QVBoxLayout(self)

        if is_image:
            label = QLabel()
            pixmap = QPixmap()
            pixmap.loadFromData(content)
            label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)
        else:
            text_edit = QTextEdit()
            text_edit.setReadOnly(True)
            text_edit.setText(content if isinstance(content, str) else content.decode('utf-8', errors='replace'))
            layout.addWidget(text_edit)

class DownloadManagerWindow(QMainWindow, Ui_DownloadManager):
    progress_updated = Signal(object)

    def __init__(self, manager: AsyncDownloadManager):
        super().__init__()
        self.setupUi(self)
        self.manager = manager
        self.rows: Dict[str, int] = {}
        self.progress_updated.connect(self.on_progress_updated)
        self.manager.add_on_progress_callback(lambda task: self.progress_updated.emit(task))

    @Slot(object)
    def on_progress_updated(self, task: DownloadTask):
        url = task.file.url
        if url not in self.rows:
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(task.file.name))
            self.rows[url] = row

        row = self.rows[url]
        self.tableWidget.setItem(row, 1, QTableWidgetItem(task.status))
        self.tableWidget.setItem(row, 2, QTableWidgetItem(f"{task.progress:.1f}%"))

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Repositories and engines
        self.tree_repo = TreeRepository()
        self.scraper = VisualesScraper()
        self.search_engine = SearchEngine(self.tree_repo)
        self.download_manager = AsyncDownloadManager()
        self.dl_window = DownloadManagerWindow(self.download_manager)

        # Background task for download manager
        self.dl_thread = Worker(self.download_manager.run)
        self.dl_thread.start()

        # UI Elements
        self.setup_custom_ui()
        self.setup_connections()

        # Initial load
        if self.tree_repo.load_from_cache():
            self.populate_tree()
            self.search_engine.refresh()
        else:
            self.statusbar.showMessage("Bienvenido. Sincronice el repositorio para comenzar.")

    def setup_custom_ui(self):
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.setVisible(False)
        self.statusbar.addPermanentWidget(self.progress_bar)

        self.main_toolbar = QToolBar("Principal")
        self.main_toolbar.setIconSize(QSize(32, 32))
        self.main_toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.addToolBar(Qt.TopToolBarArea, self.main_toolbar)

        self.btn_download_repo = QToolButton()
        self.btn_download_repo.setText("Actualizar")
        self.btn_download_repo.setIcon(QIcon(":/icons/images/repo_download.png"))
        self.btn_download_repo.clicked.connect(self.confirm_update_repo)
        self.main_toolbar.addWidget(self.btn_download_repo)

        self.main_toolbar.addSeparator()

        self.btn_search = QToolButton()
        self.btn_search.setText("Buscador")
        self.btn_search.setIcon(QIcon(":/icons/images/search.png"))
        self.btn_search.setCheckable(True)
        self.btn_search.clicked.connect(self.toggle_search)
        self.main_toolbar.addWidget(self.btn_search)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar en todo el repositorio...")
        self.search_input.setMinimumWidth(300)
        self.search_input.setVisible(False)
        self.main_toolbar.addWidget(self.search_input)

        self.btn_downloads = QToolButton()
        self.btn_downloads.setText("Descargas")
        self.btn_downloads.setIcon(QIcon(":/icons/images/download.png"))
        self.btn_downloads.clicked.connect(self.dl_window.show)
        self.main_toolbar.addWidget(self.btn_downloads)

        self.btn_export = QToolButton()
        self.btn_export.setText("Exportar")
        self.btn_export.setIcon(QIcon(":/icons/images/txt.png"))
        self.btn_export.clicked.connect(self.export_to_txt)
        self.main_toolbar.addWidget(self.btn_export)

    def setup_connections(self):
        self.treeWidget.itemExpanded.connect(self.on_item_expanded)
        self.treeWidget.itemClicked.connect(self.on_item_clicked)
        self.search_input.textChanged.connect(self.perform_search)

        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.show_context_menu)
        self.tableWidget.itemDoubleClicked.connect(self.on_table_double_clicked)

        self.download_remote_repo_action.triggered.connect(self.download_repo)
        self.show_download_manager_action.triggered.connect(self.dl_window.show)
        self.about_action.triggered.connect(self.show_about)
        self.quit_action.triggered.connect(self.close)
        self.export_local_repo_as_txt_action.triggered.connect(self.export_to_txt)

    def show_about(self):
        AboutDialog(self).exec()

    def export_to_txt(self):
        if self.tableWidget.rowCount() == 0:
            QMessageBox.warning(self, "Exportar", "No hay elementos en la tabla.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Exportar enlaces", "", "TXT (*.txt)")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    for row in range(self.tableWidget.rowCount()):
                        item = self.tableWidget.item(row, 0)
                        node = item.data(Qt.UserRole)
                        if isinstance(node, BaseNode):
                            f.write(f"{node.url}\n")
                self.statusbar.showMessage(f"Guardado en {file_path}")
            except Exception as e:
                self.on_error(e)

    def show_context_menu(self, pos):
        item = self.tableWidget.itemAt(pos)
        if not item: return

        menu = QMenu()
        row = item.row()
        node = self.tableWidget.item(row, 0).data(Qt.UserRole)

        if isinstance(node, FileNode):
            dl_act = menu.addAction("Descargar")
            dl_act.triggered.connect(lambda: self.download_manager.enqueue(node))

        fav_text = "Quitar Favorito" if node.is_favorite else "Marcar Favorito"
        fav_act = menu.addAction(fav_text)

        def toggle_fav():
            node.is_favorite = not node.is_favorite
            self.refresh_table_icons()

        fav_act.triggered.connect(toggle_fav)
        menu.exec(self.tableWidget.viewport().mapToGlobal(pos))

    def refresh_table_icons(self):
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 0)
            node = item.data(Qt.UserRole)
            if node.is_favorite:
                item.setIcon(QIcon(":/icons/images/favorite.png"))
            else:
                # Reset to default file/folder icon
                item.setIcon(QIcon())

    def on_table_double_clicked(self, item):
        row = item.row()
        node = self.tableWidget.item(row, 0).data(Qt.UserRole)

        if self.search_input.isVisible():
            if isinstance(node, FolderNode):
                self.navigate_to_url(node.url)
            elif isinstance(node, FileNode):
                self.navigate_to_url(node.parent_url)
        else:
            if isinstance(node, FileNode):
                if node.file_type in [FileType.IMAGE, FileType.TEXT]:
                    self.preview_file(node)
                else:
                    import webbrowser
                    webbrowser.open(node.url)

    def preview_file(self, file: FileNode):
        self.statusbar.showMessage(f"Previsualizando {file.name}...")
        async def fetch():
            async with aiohttp.ClientSession() as session:
                async with session.get(file.url) as r:
                    return await r.read()

        worker = Worker(fetch)
        worker.finished.connect(lambda data: PreviewDialog(file.name, data, file.file_type == FileType.IMAGE, self).exec())
        worker.error.connect(self.on_error)
        worker.start()
        self._current_worker = worker

    def navigate_to_url(self, url):
        self.load_folder_contents(url)

    def toggle_search(self, checked):
        self.search_input.setVisible(checked)
        if checked:
            self.search_input.setFocus()
            self.tableWidget.setHorizontalHeaderLabels(["Nombre", "URL", "Score"])
        else:
            self.search_input.clear()
            self.tableWidget.setHorizontalHeaderLabels(["Nombre", "Tamaño", "Fecha"])
        self.tableWidget.setRowCount(0)

    def perform_search(self, text):
        if len(text) < 3: return
        results = self.search_engine.fuzzy_search(text)
        self.tableWidget.setRowCount(len(results))
        for i, (node, score) in enumerate(results):
            item = QTableWidgetItem(node.name)
            item.setData(Qt.UserRole, node)
            self.tableWidget.setItem(i, 0, item)
            self.tableWidget.setItem(i, 1, QTableWidgetItem(node.url))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(f"{score:.1f}"))

    def confirm_update_repo(self):
        self.statusbar.showMessage("Obteniendo tamaño del listado...")
        worker = Worker(self.scraper.get_listado_size)
        worker.finished.connect(self._on_listado_size_received)
        worker.error.connect(self.on_error)
        worker.start()
        self._current_worker = worker

    def _on_listado_size_received(self, size: int):
        size_str = self.format_size(size)
        reply = QMessageBox.question(
            self, "Actualizar Repositorio",
            f"¿Desea descargar el listado de directorios?\n\nTamaño aproximado: {size_str}",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.download_repo()

    def download_repo(self):
        self.statusbar.showMessage("Descargando listado...")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)

        worker = Worker(self.scraper.download_listado)
        worker.progress.connect(self.progress_bar.setValue)
        worker.finished.connect(self.on_listado_downloaded)
        worker.error.connect(self.on_error)
        worker.start()
        self._current_worker = worker

    def on_error(self, error):
        self.progress_bar.setVisible(False)
        details = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        ErrorDialog("Error", "Se produjo un error en la operación", details, self).exec()

    def on_listado_downloaded(self, content):
        self.statusbar.showMessage("Procesando árbol...")
        self.progress_bar.setRange(0, 100)
        worker = Worker(self.tree_repo.build_from_html, content)
        worker.progress.connect(self.progress_bar.setValue)
        worker.finished.connect(self.on_tree_built)
        worker.error.connect(self.on_error)
        worker.start()
        self._current_worker = worker

    def on_tree_built(self, _):
        self.progress_bar.setVisible(False)
        self.populate_tree()
        self.search_engine.refresh()
        self.statusbar.showMessage("Repositorio actualizado.")

    def populate_tree(self):
        self.treeWidget.clear()
        if not self.tree_repo.tree.root: return
        root_node = self.tree_repo.tree.get_node(self.tree_repo.tree.root)
        item = self.create_tree_item(root_node.tag)
        self.treeWidget.addTopLevelItem(item)
        item.setExpanded(True)

    def create_tree_item(self, node: FolderNode):
        item = QTreeWidgetItem([node.name])
        item.setData(0, Qt.UserRole, node.url)
        tree_node = self.tree_repo.tree.get_node(node.url)
        if tree_node and not tree_node.is_leaf():
            item.addChild(QTreeWidgetItem(["Cargando..."]))
        return item

    def on_item_expanded(self, item):
        url = item.data(0, Qt.UserRole)
        if item.childCount() > 0 and item.child(0).text(0) == "Cargando...":
            item.takeChild(0)
            for child in self.tree_repo.get_children(url):
                item.addChild(self.create_tree_item(child))

    def on_item_clicked(self, item):
        self.load_folder_contents(item.data(0, Qt.UserRole))

    def load_folder_contents(self, url):
        self.statusbar.showMessage(f"Cargando {url} ...")
        self.tableWidget.setRowCount(0)
        self.progress_bar.setRange(0, 0) # Indeterminate
        self.progress_bar.setVisible(True)
        QApplication.setOverrideCursor(Qt.WaitCursor)

        worker = Worker(self.scraper.get_folder_contents, url)
        worker.finished.connect(self.on_folder_loaded)
        worker.error.connect(self.on_folder_load_error)
        worker.start()
        self._current_worker = worker

    def on_folder_loaded(self, files):
        QApplication.restoreOverrideCursor()
        self.progress_bar.setVisible(False)
        self.populate_table(files)

    def on_folder_load_error(self, error):
        QApplication.restoreOverrideCursor()
        self.progress_bar.setVisible(False)
        self.on_error(error)

    def get_type_icon(self, file_type: FileType) -> QIcon:
        icon_map = {
            FileType.MOVIE: ":/icons/images/video.png",
            FileType.IMAGE: ":/icons/images/picture.png",
            FileType.AUDIO: ":/icons/images/audio.png",
            FileType.TEXT: ":/icons/images/txt.png",
            FileType.PDF: ":/icons/images/pdf.png",
            FileType.SOFTWARE: ":/icons/images/software.png",
            FileType.COMPRESSED: ":/icons/images/rar.png",
        }
        path = icon_map.get(file_type, ":/icons/images/uknown.png")
        return QIcon(path)

    def populate_table(self, files: List[FileNode]):
        self.tableWidget.setRowCount(len(files))
        for i, file in enumerate(files):
            item = QTableWidgetItem(file.name)
            item.setData(Qt.UserRole, file)

            # Use specific type icon
            icon = self.get_type_icon(file.file_type)
            if file.is_favorite:
                icon = QIcon(":/icons/images/favorite.png")
            item.setIcon(icon)

            # Add checkbox
            item.setCheckState(Qt.Unchecked)

            self.tableWidget.setItem(i, 0, item)
            self.tableWidget.setItem(i, 1, QTableWidgetItem(self.format_size(file.size)))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(file.modification_date.strftime("%d/%m/%Y") if file.modification_date else ""))
        self.statusbar.showMessage("Carpeta cargada.")

    def format_size(self, size):
        if size == 0: return "-"
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024: return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
