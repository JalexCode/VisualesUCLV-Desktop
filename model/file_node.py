from datetime import datetime

from util.const import *


class FileNode:
    def __init__(self, filename: str, modification_date: datetime = datetime.now(), size: float = 0,
                 href: str = Paths.LISTADO_HTML_FILE, the_type: str = AppEnums.TEXT, favorite: bool = False,
                 downloaded: bool = False):
        self._filename: str = filename
        self._modification_date: datetime = modification_date
        self._size: float = size
        self._href: str = href
        self._type: str = the_type
        self._favorite = favorite
        self._downloaded = downloaded

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, v):
        self._filename = v

    @property
    def modification_date(self):
        return self._modification_date

    @modification_date.setter
    def modification_date(self, modification_date):
        self._modification_date = modification_date

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size

    @property
    def href(self):
        return self._href

    @href.setter
    def href(self, href):
        self._href = href

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, the_type):
        self._type = the_type

    @property
    def favorite(self):
        return self._favorite

    @favorite.setter
    def favorite(self, value):
        self._favorite = value

    @property
    def downloaded(self):
        return self._downloaded

    @downloaded.setter
    def downloaded(self, value):
        self._downloaded = value

    def __str__(self) -> str:
        return self.filename

    def __repr__(self) -> str:
        return f"<{self.filename}>"

    def __eq__(self, other):
        return self.href == other.href

    def __lt__(self, other):
        return self.filename < other.filename

    def __gt__(self, other):
        return self.filename > other.filename
