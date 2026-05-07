from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict

class FileType(Enum):
    MOVIE = "movie"
    IMAGE = "image"
    AUDIO = "audio"
    TEXT = "text"
    UNKNOWN = "unknown"
    PDF = "pdf"
    SOFTWARE = "software"
    COMPRESSED = "compressed"

@dataclass
class BaseNode:
    name: str
    url: str
    parent_url: Optional[str] = None
    is_favorite: bool = False

@dataclass
class FileNode(BaseNode):
    size: int = 0
    modification_date: Optional[datetime] = None
    file_type: FileType = FileType.UNKNOWN
    is_downloaded: bool = False

@dataclass
class FolderNode(BaseNode):
    is_empty: bool = False
    children_loaded: bool = False
    # In-memory child nodes (can be used for lazy loading)
    files: List[FileNode] = field(default_factory=list)
    subfolders: List['FolderNode'] = field(default_factory=list)
