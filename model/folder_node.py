class FolderNode:
    def __init__(self, name: str, is_empty: str, favorite: str):
        self._name: str = name
        self._is_empty: str = is_empty
        self._favorite: str = favorite

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, v):
        self._name = v

    @property
    def is_empty(self):
        return self._is_empty

    @is_empty.setter
    def is_empty(self, value):
        self._is_empty = value

    @property
    def favorite(self):
        return self._favorite

    @favorite.setter
    def favorite(self, favorite):
        self._favorite = favorite

    def __str__(self) -> str:
        return self.name
