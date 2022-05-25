class TreeNode:
    def __init__(self, value, modification_date, size):
        self._value = value
        self._modification_date = modification_date
        self._size = size

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v

    @property
    def modification_date(self):
        return self._modification_date

    @modification_date.setter
    def modification_date(self, value):
        self._modification_date = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    def __eq__(self, other):
        return self.value == other.value and self.modification_date == self.modification_date and self.size == other.size
