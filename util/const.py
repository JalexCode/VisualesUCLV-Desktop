import os
# paths and files
VISUALES_UCLV_URL = "http://visuales.uclv.cu"
LISTADO_HTML_FILE = "http://visuales.uclv.cu/listado.html"
DATA_FOLDER = os.path.join(os.getcwd(), "data")
DIRS_FILE_NAME = "directories.visuales"
DIR_FILE = os.path.join(DATA_FOLDER, DIRS_FILE_NAME)
TREE_DATA_FILE_NAME = "data.tree"
TREE_FILE = os.path.join(DATA_FOLDER, TREE_DATA_FILE_NAME)
# app
APP_NAME = "Visuales UCLV Explorer"
APP_ID = "_".join(APP_NAME.split()).lower()
VERSION = "0.1"
COLABORATORS = "Rolando Juan Rio Garaboa [@R0land013]"
ABOUT = f"""{APP_NAME} funciona como explorador local del FTP {VISUALES_UCLV_URL}, el cual tiene mucha demanda por los internautas cubanos quienes acceden diariamente en busca de las series que siguen, las películas en estreno, y en general, el sin fin de materiales audiovisuales que en ese repositorio se encuentran. Este programa tiene como fin facilitar la exploración del contenido de este repositorio remoto.
Características:
* Acceso rápido y bajo demanda a todos los directorios del repositorio
* Búsqueda de directorios y archivos
* Sistema de caché para almacenar la información solicitada al repositorio remoto (metadatos de los archivos y directorios)

Importante:
{APP_NAME} recibe los directorios del fichero {LISTADO_HTML_FILE}, por lo que le brinda la opción de Descarga manual para adquirir este archivo.
A priori, esta aplicación no contendrá los datos de todos los archivos existentes en el repositorio. Solo almacenará los que usted haya visitado.
Esta aplicación no descarga los ficheros directamente, solo les muestra su información. La descarga la puede realizar desde el navegador.
"""
# settings
RETRY = 5
TIMEOUT = 10
CHUNK_SIZE = 1024
ICON_SIZE = 64
DATE_FORMAT = "%d/%m/%Y %I:%M %p"
DATE_FROM_SERVER_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"
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
AN_ERROR_WAS_OCURRED = "Ha ocurrido un error :-("
