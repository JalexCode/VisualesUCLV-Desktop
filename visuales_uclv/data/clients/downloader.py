import aiohttp
import asyncio
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Callable
from visuales_uclv.domain.models.nodes import FileNode
from visuales_uclv.core.config.settings import settings
from visuales_uclv.core.logger.logger import get_logger

logger = get_logger(__name__)

@dataclass
class DownloadTask:
    file: FileNode
    status: str = "pending" # pending, downloading, paused, completed, error
    progress: float = 0.0
    downloaded_bytes: int = 0
    total_bytes: int = 0
    error_message: Optional[str] = None
    task: Optional[asyncio.Task] = None

class AsyncDownloadManager:
    def __init__(self):
        self.tasks: Dict[str, DownloadTask] = {}
        self.queue = asyncio.Queue()
        self.semaphore = asyncio.Semaphore(settings.max_concurrent_downloads)
        self._on_progress_callbacks: List[Callable[[DownloadTask], None]] = []

    def add_on_progress_callback(self, callback: Callable[[DownloadTask], None]):
        self._on_progress_callbacks.append(callback)

    def enqueue(self, file: FileNode):
        if file.url in self.tasks:
            logger.info(f"File {file.name} already in download queue")
            return

        task = DownloadTask(file=file, total_bytes=file.size)
        self.tasks[file.url] = task
        self.queue.put_nowait(task)
        logger.info(f"Enqueued: {file.name}")

    async def _download_worker(self, task: DownloadTask):
        async with self.semaphore:
            task.status = "downloading"
            dest_path = settings.download_dir / task.file.name

            # Resume support
            start_pos = 0
            mode = "wb"
            if dest_path.exists():
                start_pos = dest_path.stat().st_size
                if start_pos < task.file.size:
                    mode = "ab"
                    task.downloaded_bytes = start_pos
                elif start_pos == task.file.size:
                    task.status = "completed"
                    task.progress = 100.0
                    return

            headers = {}
            if start_pos > 0:
                headers["Range"] = f"bytes={start_pos}-"

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(task.file.url, headers=headers, timeout=None) as response:
                        if response.status not in (200, 206):
                            raise Exception(f"HTTP Error {response.status}")

                        if task.total_bytes == 0:
                            task.total_bytes = int(response.headers.get("Content-Length", 0)) + start_pos

                        with open(dest_path, mode) as f:
                            async for chunk in response.content.iter_chunked(settings.chunk_size):
                                if task.status == "paused":
                                    # Handle pause logic if needed
                                    break

                                f.write(chunk)
                                task.downloaded_bytes += len(chunk)
                                if task.total_bytes > 0:
                                    task.progress = (task.downloaded_bytes / task.total_bytes) * 100

                                for cb in self._on_progress_callbacks:
                                    cb(task)

                        if task.downloaded_bytes >= task.total_bytes:
                            task.status = "completed"
                            logger.info(f"Finished: {task.file.name}")

            except Exception as e:
                task.status = "error"
                task.error_message = str(e)
                logger.error(f"Error downloading {task.file.name}: {e}")

    async def run(self):
        while True:
            task = await self.queue.get()
            asyncio.create_task(self._download_worker(task))
            self.queue.task_done()
