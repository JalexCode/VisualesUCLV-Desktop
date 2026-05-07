from rapidfuzz import process, fuzz
from typing import List, Tuple
from visuales_uclv.domain.models.nodes import BaseNode
from visuales_uclv.data.repositories.tree_repository import TreeRepository
from visuales_uclv.core.logger.logger import get_logger

logger = get_logger(__name__)

class SearchEngine:
    def __init__(self, tree_repo: TreeRepository):
        self.tree_repo = tree_repo
        self._all_nodes: List[BaseNode] = []
        self._node_names: List[str] = []

    def refresh(self):
        logger.info("Refreshing search index...")
        self._all_nodes = [node.tag for node in self.tree_repo.tree.all_nodes()]
        self._node_names = [node.name for node in self._all_nodes]
        logger.info(f"Search index refreshed with {len(self._node_names)} items")

    def fuzzy_search(self, query: str, limit: int = 50) -> List[Tuple[BaseNode, float]]:
        if not query:
            return []

        if not self._node_names:
            self.refresh()

        results = process.extract(
            query,
            self._node_names,
            scorer=fuzz.WRatio,
            limit=limit
        )

        search_results = []
        for name, score, index in results:
            search_results.append((self._all_nodes[index], score))

        return search_results
