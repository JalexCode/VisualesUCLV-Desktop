import asyncio
from visuales_uclv.data.repositories.tree_repository import TreeRepository
from visuales_uclv.domain.search_engine import SearchEngine
from visuales_uclv.domain.models.nodes import FolderNode

async def test_logic():
    print("Testing TreeRepository...")
    repo = TreeRepository()
    # Mock HTML with multiple links to test hierarchy
    html = '<html><body>' \
           '<a href="http://visuales.uclv.cu/">Visuales</a>' \
           '<a href="http://visuales.uclv.cu/Series/">Series</a>' \
           '<a href="http://visuales.uclv.cu/Series/NETFLIX/">NETFLIX</a>' \
           '</body></html>'
    repo.build_from_html(html)
    print(f"Tree size: {repo.tree.size()}")

    print("Testing SearchEngine...")
    search = SearchEngine(repo)
    search.refresh()
    results = search.fuzzy_search("Series")
    print(f"Search results for 'Series': {results}")
    assert len(results) > 0
    assert "Series" in results[0][0].name

if __name__ == "__main__":
    asyncio.run(test_logic())
