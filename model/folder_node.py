class FolderNode:
    def __init__(self, name:str, visited:str, favorite:str):
        self._name:str = name
        self._visited:str = visited
        self._favorite:str = favorite

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, v):
        self._name = v

    @property
    def visited(self):
        return self._visited

    @visited.setter
    def visited(self, visited):
        self._visited = visited

    @property
    def favorite(self):
        return self._favorite

    @favorite.setter
    def favorite(self, favorite):
        self._favorite = favorite