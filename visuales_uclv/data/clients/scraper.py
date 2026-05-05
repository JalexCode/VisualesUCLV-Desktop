import aiohttp
import os
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Optional, Callable
from visuales_uclv.domain.models.nodes import FolderNode, FileNode, FileType
from visuales_uclv.core.config.settings import settings
from visuales_uclv.core.logger.logger import get_logger

logger = get_logger(__name__)

class VisualesScraper:
    def __init__(self):
        self.base_url = "http://visuales.uclv.cu"
        self.listado_url = f"{self.base_url}/listado.html"

    async def fetch_html(self, url: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=settings.request_timeout) as response:
                return await response.text()

    def _parse_file_type(self, img_src: str) -> FileType:
        if "video" in img_src: return FileType.MOVIE
        if "image" in img_src: return FileType.IMAGE
        if "audio" in img_src: return FileType.AUDIO
        if "text" in img_src: return FileType.TEXT
        if "pdf" in img_src: return FileType.PDF
        if "software" in img_src: return FileType.SOFTWARE
        if "compressed" in img_src: return FileType.COMPRESSED
        return FileType.UNKNOWN

    def _parse_size(self, size_str: str) -> int:
        size_str = size_str.strip()
        if size_str == "-": return 0

        multipliers = {"K": 1024, "M": 1024*1024, "G": 1024*1024*1024}
        try:
            if size_str[-1] in multipliers:
                return int(float(size_str[:-1]) * multipliers[size_str[-1]])
            return int(size_str)
        except ValueError:
            return 0

    async def get_folder_contents(self, url: str) -> List[FileNode]:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=settings.request_timeout) as response:
                html = await response.text()
                soup = BeautifulSoup(html, "lxml")
                files = []

                rows = soup.find_all("tr")[3:]
                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) < 5: continue

                    img = cols[0].find("img")
                    name_link = cols[1].find("a")
                    if not name_link or not img: continue

                    name = name_link.text.strip()
                    href = name_link.get("href")
                    full_url = url + href if not href.startswith("http") else href

                    size_str = cols[3].text.strip()
                    if size_str == "-": continue

                    mod_date_str = cols[2].text.strip()
                    try:
                        mod_date = datetime.fromisoformat(mod_date_str)
                    except ValueError:
                        mod_date = None

                    file_node = FileNode(
                        name=name,
                        url=full_url,
                        parent_url=url,
                        size=self._parse_size(size_str),
                        modification_date=mod_date,
                        file_type=self._parse_file_type(img.get("src", ""))
                    )
                    files.append(file_node)

                return files

    async def download_listado(self, progress_callback: Optional[Callable[[int], None]] = None) -> bytes:
        logger.info(f"Starting download of {self.listado_url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(self.listado_url, timeout=None) as response:
                if response.status != 200:
                    raise Exception(f"Error del servidor: {response.status}")

                total_size = int(response.headers.get("Content-Length", 0))
                downloaded = 0
                chunks = []

                async for chunk in response.content.iter_chunked(settings.chunk_size):
                    chunks.append(chunk)
                    downloaded += len(chunk)
                    if progress_callback and total_size > 0:
                        progress_callback(int((downloaded / total_size) * 100))

                content = b"".join(chunks)

                cache_path = settings.data_folder / settings.listado_cache_file
                with open(cache_path, "wb") as f:
                    f.write(content)

                logger.info(f"Saved listado.html to {cache_path}")
                return content
