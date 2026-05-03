from bs4 import BeautifulSoup
from treelib import Tree
import pickle
from typing import List, Optional
from visuales_uclv.domain.models.nodes import FolderNode, BaseNode
from visuales_uclv.core.config.settings import settings
from visuales_uclv.core.logger.logger import get_logger

logger = get_logger(__name__)

class TreeRepository:
    def __init__(self):
        self.tree = Tree()
        self.cache_path = settings.data_folder / settings.tree_cache_file

    def build_from_html(self, html_content: str):
        logger.info("Building tree from HTML...")
        soup = BeautifulSoup(html_content, "lxml")
        links = soup.find_all("a")

        if not links:
            logger.warning("No links found in HTML content")
            return

        # First link is usually the root
        root_tag = links[0]
        root_url = root_tag.get("href") + "/" if not root_tag.get("href").endswith("/") else root_tag.get("href")
        root_name = root_tag.text.strip()

        self.tree = Tree()
        self.tree.create_node(
            tag=FolderNode(name=root_name, url=root_url),
            identifier=root_url
        )

        for link in links[1:]:
            url = link.get("href")
            name = link.text.strip()

            # Parent URL is derived from the URL path
            parent_url = self._get_parent_url(url)

            try:
                self.tree.create_node(
                    tag=FolderNode(name=name, url=url, parent_url=parent_url),
                    identifier=url,
                    parent=parent_url
                )
            except Exception as e:
                # Sometimes parents are missing if the HTML is weird, or duplicates
                pass

        self.save_to_cache()
        logger.info(f"Tree built with {self.tree.size()} nodes")

    def _get_parent_url(self, url: str) -> str:
        # Example: http://visuales.uclv.cu/Pelis/Accion/
        if url.endswith("/"):
            trimmed = url[:-1]
        else:
            trimmed = url

        last_slash = trimmed.rfind("/")
        if last_slash == -1:
            return ""
        return trimmed[:last_slash + 1]

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
