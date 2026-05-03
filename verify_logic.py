import asyncio
from visuales_uclv.data.repositories.tree_repository import TreeRepository
from visuales_uclv.domain.search_engine import SearchEngine
from visuales_uclv.domain.models.nodes import FolderNode

async def test_logic():
    print("Testing TreeRepository...")
    repo = TreeRepository()
    html = '<html><body><a href="http://visuales.uclv.cu/">Visuales</a><a href="http://visuales.uclv.cu/Pelis/">Pelis</a></body></html>'
    repo.build_from_html(html)
    print(f"Tree size: {repo.tree.size()}")

    print("Testing SearchEngine...")
    search = SearchEngine(repo)
    search.refresh()
    results = search.fuzzy_search("Pelis")
    print(f"Search results for 'Pelis': {results}")
    assert len(results) > 0
    assert "Pelis" in results[0][0].name

if __name__ == "__main__":
    asyncio.run(test_logic())
