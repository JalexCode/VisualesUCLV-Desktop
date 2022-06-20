from util.response_codes import RESPONSE_CODES


class BadResponseException(Exception):
    def __init__(self, message: object) -> None:
        message = f"[{message}] {RESPONSE_CODES[message]}"
        super().__init__(message)

class DirsFileDoesntExistException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        
class TreeFileDoesntExistException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        
class FileNotFounded(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)