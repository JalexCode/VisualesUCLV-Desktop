from abc import ABC, abstractmethod
from typing import List, Optional
from visuales_uclv.domain.models.nodes import FolderNode, FileNode

class IScraper(ABC):
    @abstractmethod
    async def get_folder_contents(self, url: str) -> List[FileNode]:
        pass

    @abstractmethod
    async def download_listado(self) -> str:
        pass

class ITreeRepository(ABC):
    @abstractmethod
    def build_tree_from_html(self, html_content: str):
        pass

    @abstractmethod
    def search(self, query: str) -> List[BaseNode]:
        pass

class IDownloadManager(ABC):
    @abstractmethod
    def add_to_queue(self, file: FileNode):
        pass

    @abstractmethod
    def start_downloads(self):
        pass

    @abstractmethod
    def pause_downloads(self):
        pass
