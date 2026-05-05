from bs4 import BeautifulSoup
from treelib import Tree
import pickle
import os
import re
from typing import List, Optional
from visuales_uclv.domain.models.nodes import FolderNode, BaseNode
from visuales_uclv.core.config.settings import settings
from visuales_uclv.core.logger.logger import get_logger

logger = get_logger(__name__)

class TreeRepository:
    def __init__(self):
        self.tree = Tree()
        self.cache_path = settings.data_folder / settings.tree_cache_file

    def _normalize_url(self, url: str) -> str:
        if not url: return ""
        # Collapse multiple slashes after protocol
        url = re.sub(r'([^:])//+', r'\1/', url)
        return url

    def build_from_html(self, html_content: bytes, progress_callback=None):
        logger.info("Building tree from HTML...")
        # BeautifulSoup handles decoding from bytes automatically
        soup = BeautifulSoup(html_content, "lxml")
        links = soup.find_all("a")

        if not links:
            logger.warning("No links found in HTML content")
            return

        # Normalized root URL
        root_tag = links[0]
        root_url = self._normalize_url(root_tag.get("href"))
        if not root_url.endswith("/"):
            root_url += "/"

        root_name = root_tag.text.strip() or "Visuales UCLV"

        self.tree = Tree()
        self.tree.create_node(
            tag=FolderNode(name=root_name, url=root_url),
            identifier=root_url
        )

        total_links = len(links) - 1
        for i, link in enumerate(links[1:]):
            url = self._normalize_url(link.get("href"))
            if not url: continue

            name = link.text.strip() or os.path.basename(url.rstrip("/"))
            parent_url = self._get_parent_url(url)

            # Normalize folder url if it is directory in listado.html
            if not url.endswith("/") and parent_url:
                 url += "/"

            try:
                # Always use normalized URLs for lookup and insertion
                if self.tree.contains(parent_url):
                    self.tree.create_node(
                        tag=FolderNode(name=name, url=url, parent_url=parent_url),
                        identifier=url,
                        parent=parent_url
                    )
                else:
                    self.tree.create_node(
                        tag=FolderNode(name=name, url=url, parent_url=self.tree.root),
                        identifier=url,
                        parent=self.tree.root
                    )
            except Exception:
                pass

            if progress_callback and i % 500 == 0:
                progress_callback(int((i / total_links) * 100))

        self.save_to_cache()
        logger.info(f"Tree built with {self.tree.size()} nodes")

    def _get_parent_url(self, url: str) -> str:
        trimmed = url.rstrip("/")
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
        url = self._normalize_url(url)
        if not self.tree.contains(url):
            return []
        return [node.tag for node in self.tree.children(url) if isinstance(node.tag, FolderNode)]
