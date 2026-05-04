from bs4 import BeautifulSoup
from treelib import Tree
import pickle
import os
from typing import List, Optional
from visuales_uclv.domain.models.nodes import FolderNode, BaseNode
from visuales_uclv.core.config.settings import settings
from visuales_uclv.core.logger.logger import get_logger

logger = get_logger(__name__)

class TreeRepository:
    def __init__(self):
        self.tree = Tree()
        self.cache_path = settings.data_folder / settings.tree_cache_file

    def build_from_html(self, html_content: str, progress_callback=None):
        logger.info("Building tree from HTML...")
        soup = BeautifulSoup(html_content, "lxml")
        links = soup.find_all("a")

        if not links:
            logger.warning("No links found in HTML content")
            return

        # Normalized root URL
        root_tag = links[0]
        root_url = root_tag.get("href")
        if not root_url.endswith("/"):
            root_url += "/"

        root_name = root_tag.text.strip()
        if not root_name:
            root_name = "Visuales UCLV"

        self.tree = Tree()
        self.tree.create_node(
            tag=FolderNode(name=root_name, url=root_url),
            identifier=root_url
        )

        total_links = len(links) - 1
        for i, link in enumerate(links[1:]):
            url = link.get("href")
            if not url: continue

            name = link.text.strip()
            if not name:
                name = os.path.basename(url.rstrip("/"))

            parent_url = self._get_parent_url(url)

            # Normalize url
            if not url.endswith("/") and parent_url:
                 # it should be a directory if it is in listado.html
                 url += "/"

            try:
                if self.tree.contains(parent_url):
                    self.tree.create_node(
                        tag=FolderNode(name=name, url=url, parent_url=parent_url),
                        identifier=url,
                        parent=parent_url
                    )
                else:
                    # If parent doesn't exist, we might have a gap.
                    # For listado.html this shouldn't happen often as it is usually ordered.
                    # But if it does, we attach to root as fallback or try to build path.
                    self.tree.create_node(
                        tag=FolderNode(name=name, url=url, parent_url=self.tree.root),
                        identifier=url,
                        parent=self.tree.root
                    )
            except Exception as e:
                # logger.debug(f"Skip node {url}: {e}")
                pass

            if progress_callback and i % 100 == 0:
                progress_callback(int((i / total_links) * 100))

        self.save_to_cache()
        logger.info(f"Tree built with {self.tree.size()} nodes")

    def _get_parent_url(self, url: str) -> str:
        # url: http://visuales.uclv.cu//Cursos/
        # url: http://visuales.uclv.cu//Cursos/Adobe/

        trimmed = url.rstrip("/")
        last_slash = trimmed.rfind("/")
        if last_slash == -1:
            return ""

        parent = trimmed[:last_slash + 1]

        # Handle cases like http://visuales.uclv.cu//Cursos/ -> parent is http://visuales.uclv.cu//
        # But root is http://visuales.uclv.cu/
        # We need to be careful with double slashes
        return parent

    def save_to_cache(self):
        with open(self.cache_path, "wb") as f:
            pickle.dump(self.tree, f)

    def load_from_cache(self) -> bool:
        if self.cache_path.exists():
            try:
                with open(self.cache_path, "rb") as f:
                    self.tree = pickle.load(f)
                return True
            except Exception as e:
                logger.error(f"Failed to load tree cache: {e}")
        return False

    def get_children(self, url: str) -> List[FolderNode]:
        if not self.tree.contains(url):
            return []
        return [node.tag for node in self.tree.children(url) if isinstance(node.tag, FolderNode)]
