class FileNode:
    def __init__(self, filename:str, modification_date:str, size:str, href:str, type:str):
        self._filename:str = filename
        self._modification_date:str = modification_date
        self._size:str = size
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

    def __eq__(self, other):
        return self.filename == other.filename and self.modification_date == self.modification_date and self.size == other.size