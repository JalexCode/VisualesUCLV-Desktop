import os

# paths and files
VISUALES_UCLV_URL = "http://visuales.uclv.cu"
LISTADO_HTML_FILE = "http://visuales.uclv.cu/listado.html"
DATA_FOLDER = os.path.join(os.getcwd(), "data")
DIRS_FILE_NAME = "directories.visuales"
DIR_FILE = os.path.join(DATA_FOLDER, DIRS_FILE_NAME)
TREE_DATA_FILE_NAME = "data.tree"
TREE_FILE = os.path.join(DATA_FOLDER, TREE_DATA_FILE_NAME)
# settings
RETRY = 5
TIMEOUT = 5
ICON_SIZE = 64
# enums
MOVIE = "MOVIE"
PICTURE = "PICTURE"
AUDIO = "AUDIO"
TEXT = "TEXT"
UNKNOWN = "UNKNOWN"
LAYOUT = "LAYOUT"
# visual
FILE_TYPES = {MOVIE: ":/types/images/video.png", PICTURE: ":/types/images/picture.png", AUDIO: ":/types/images/audio.png",
              TEXT: ":/types/images/doc.png", UNKNOWN: ":/types/images/uknown.png", LAYOUT: ":/types/images/pdf.png"}
# exceptions
CONNECTION_FAIL = "Error de conexión"