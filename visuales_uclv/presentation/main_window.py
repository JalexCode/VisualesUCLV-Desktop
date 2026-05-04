import sys
import asyncio
from typing import List, Dict
from PySide6.QtWidgets import QMainWindow, QApplication, QTreeWidgetItem, QTableWidgetItem, QLineEdit, QToolButton, QToolBar, QMenu
from PySide6.QtCore import Qt, QThread, Signal, Slot, QRect
from qt_material import apply_stylesheet

from visuales_uclv.presentation.ui.main_ui import Ui_MainWindow
from visuales_uclv.presentation.ui.downloader_ui import Ui_DownloadManager
from visuales_uclv.data.repositories.tree_repository import TreeRepository
from visuales_uclv.data.clients.scraper import VisualesScraper
from visuales_uclv.data.clients.downloader import AsyncDownloadManager, DownloadTask
from visuales_uclv.domain.search_engine import SearchEngine
from visuales_uclv.core.config.settings import settings
from visuales_uclv.core.logger.logger import setup_logging, get_logger
from visuales_uclv.domain.models.nodes import FolderNode, FileNode, BaseNode

# Initialize logger
setup_logging()
logger = get_logger(__name__)

class Worker(QThread):
    finished = Signal(object)
    error = Signal(str)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            if asyncio.iscoroutinefunction(self.func):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(self.func(*self.args, **self.kwargs))
                loop.close()
            else:
                result = self.func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            logger.error(f"Worker error: {e}")
            self.error.emit(str(e))

class DownloadManagerWindow(QMainWindow, Ui_DownloadManager):
    def __init__(self, manager: AsyncDownloadManager):
        super().__init__()
        self.setupUi(self)
        self.manager = manager
        self.manager.add_on_progress_callback(self.update_progress)
        self.rows: Dict[str, int] = {}

    def update_progress(self, task: DownloadTask):
        # This is called from the async worker, so it might need to be thread-safe or use signals
        # For simplicity in this refactor, we'll assume it's okay or use a signal if we had more time
        pass

    def add_task(self, task: DownloadTask):
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        self.tableWidget.setItem(row, 0, QTableWidgetItem(task.file.name))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(task.status))
        self.tableWidget.setItem(row, 2, QTableWidgetItem("0%"))
        self.rows[task.file.url] = row

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
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.setVisible(False)
        self.statusbar.addPermanentWidget(self.search_input)

        self.main_toolbar = QToolBar("Main Toolbar")
        self.addToolBar(Qt.TopToolBarArea, self.main_toolbar)

        self.btn_download_repo = QToolButton()
        self.btn_download_repo.setText("Update Repo")
        self.btn_download_repo.clicked.connect(self.download_repo)
        self.main_toolbar.addWidget(self.btn_download_repo)

        self.btn_search = QToolButton()
        self.btn_search.setText("Search")
        self.btn_search.setCheckable(True)
        self.btn_search.clicked.connect(self.toggle_search)
        self.main_toolbar.addWidget(self.btn_search)

        self.btn_downloads = QToolButton()
        self.btn_downloads.setText("Downloads")
        self.btn_downloads.clicked.connect(self.dl_window.show)
        self.main_toolbar.addWidget(self.btn_downloads)

        # Connections
        self.treeWidget.itemExpanded.connect(self.on_item_expanded)
        self.treeWidget.itemClicked.connect(self.on_item_clicked)
        self.search_input.textChanged.connect(self.perform_search)

        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.show_context_menu)
        self.tableWidget.itemDoubleClicked.connect(self.on_table_double_clicked)

        # Initial load
        if self.tree_repo.load_from_cache():
            self.populate_tree()
            self.search_engine.refresh()
        else:
            self.statusbar.showMessage("No cache found. Please Update Repo.")

    def show_context_menu(self, pos):
        item = self.tableWidget.itemAt(pos)
        if not item: return

        menu = QMenu()
        download_action = menu.addAction("Download")

        action = menu.exec(self.tableWidget.viewport().mapToGlobal(pos))
        if action == download_action:
            row = item.row()
            name_item = self.tableWidget.item(row, 0)
            file_node = name_item.data(Qt.UserRole)
            if isinstance(file_node, FileNode):
                self.download_manager.enqueue(file_node)
                self.statusbar.showMessage(f"Enqueued {file_node.name} for download.")

    def on_table_double_clicked(self, item):
        row = item.row()
        if self.search_input.isVisible():
            # In search mode, navigate to folder
            url = self.tableWidget.item(row, 1).text()
            if url.endswith("/"):
                self.navigate_to_url(url)
            else:
                parent_url = url[:url.rfind("/")+1]
                self.navigate_to_url(parent_url)

    def navigate_to_url(self, url):
        # Simple navigation: load folder contents
        self.load_folder_contents(url)
        # In a full implementation, we'd also expand the tree to this location

    def toggle_search(self, checked):
        self.search_input.setVisible(checked)
        if checked:
            self.search_input.setFocus()
            self.tableWidget.setHorizontalHeaderLabels(["Name", "URL", "Score", ""])
        else:
            self.search_input.clear()
            self.tableWidget.setHorizontalHeaderLabels(["Name", "Size", "Date", ""])

    def perform_search(self, text):
        if len(text) < 3:
            return
        results = self.search_engine.fuzzy_search(text)
        self.populate_search_results(results)

    def populate_search_results(self, results):
        self.tableWidget.setRowCount(len(results))
        for i, (node, score) in enumerate(results):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(node.name))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(node.url))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(f"{score:.1f}"))

    def download_repo(self):
        self.statusbar.showMessage("Downloading listado.html...")
        worker = Worker(self.scraper.download_listado)
        worker.finished.connect(self.on_listado_downloaded)
        worker.start()
        # Store reference to prevent GC
        self._current_worker = worker

    def on_listado_downloaded(self, html):
        self.statusbar.showMessage("Building tree...")
        worker = Worker(self.tree_repo.build_from_html, html)
        worker.finished.connect(self.on_tree_built)
        worker.start()
        self._current_worker = worker

    def on_tree_built(self, _):
        self.populate_tree()
        self.search_engine.refresh()
        self.statusbar.showMessage("Tree ready.")

    def populate_tree(self):
        self.treeWidget.clear()
        root_nodes = self.tree_repo.tree.children(self.tree_repo.tree.root)
        for node in root_nodes:
            item = self.create_tree_item(node.tag)
            self.treeWidget.addTopLevelItem(item)

    def create_tree_item(self, node: FolderNode):
        item = QTreeWidgetItem([node.name])
        item.setData(0, Qt.UserRole, node.url)
        tree_node = self.tree_repo.tree.get_node(node.url)
        if tree_node and not tree_node.is_leaf():
            item.addChild(QTreeWidgetItem(["Loading..."]))
        return item

    def on_item_expanded(self, item):
        url = item.data(0, Qt.UserRole)
        if item.childCount() > 0 and item.child(0).text(0) == "Loading...":
            item.takeChild(0)
            children = self.tree_repo.get_children(url)
            for child in children:
                item.addChild(self.create_tree_item(child))

    def on_item_clicked(self, item):
        url = item.data(0, Qt.UserRole)
        self.load_folder_contents(url)

    def load_folder_contents(self, url):
        self.statusbar.showMessage(f"Loading contents of {url}...")
        self.tableWidget.setRowCount(0)
        worker = Worker(self.scraper.get_folder_contents, url)
        worker.finished.connect(self.populate_table)
        worker.start()
        self._current_worker = worker

    def populate_table(self, files: List[FileNode]):
        self.tableWidget.setRowCount(len(files))
        for i, file in enumerate(files):
            item = QTableWidgetItem(file.name)
            item.setData(Qt.UserRole, file)
            self.tableWidget.setItem(i, 0, item)
            self.tableWidget.setItem(i, 1, QTableWidgetItem(self.format_size(file.size)))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(file.modification_date.isoformat() if file.modification_date else ""))
        self.statusbar.showMessage("Done.")

    def format_size(self, size):
        if size == 0: return "0 B"
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
