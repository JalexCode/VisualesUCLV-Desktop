from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path
import os

class Settings(BaseSettings):
    app_name: str = "Visuales UCLV Explorer"
    download_dir: Path = Field(default=Path.home() / "Downloads" / "VisualesUCLV")
    max_concurrent_downloads: int = 5
    cache_expire_days: int = 7
    request_timeout: int = 30
    chunk_size: int = 1024 * 64  # 64KB

    data_folder: Path = Path("data")
    tree_cache_file: str = "data.tree"
    listado_cache_file: str = "directories.visuales"

    model_config = SettingsConfigDict(env_prefix="VISUALES_", env_file=".env")

    def ensure_dirs(self):
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.data_folder.mkdir(parents=True, exist_ok=True)

settings = Settings()
settings.ensure_dirs()
