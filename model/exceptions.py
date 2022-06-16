class BadResponseException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class DirsFileDoesntExistException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        
class TreeFileDoesntExistException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        
class FileNotFounded(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)