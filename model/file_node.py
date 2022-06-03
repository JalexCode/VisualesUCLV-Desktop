from datetime import datetime


class FileNode:
    def __init__(self, filename:str, modification_date:datetime, size:float, href:str, type:str):
        self._filename:str = filename
        self._modification_date:datetime = modification_date
        self._size:float = size
        self._href:str = href
        self._type:str = type

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
    def type(self, type):
        self._type = type
        
    def __str__(self) -> str:
        return self.filename

    def __eq__(self, other):
        return self.filename == other.filename and self.modification_date == other.modification_date and self.size == other.size
