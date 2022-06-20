'''
This module contains constants variables
'''
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
__version_major__ = 0
__version_minor__ = 4
__version_micro__ = 0
__version__ = "{}.{}.{}".format(__version_major__, __version_minor__, __version_micro__)
COLABORATORS = "Rolando Juan Rio Garaboa [@R0land013]"
ABOUT = f"""{APP_NAME} funciona como explorador local del FTP {VISUALES_UCLV_URL}, el cual tiene mucha demanda por los internautas cubanos quienes acceden diariamente en busca de las series que siguen, las películas en estreno y, en general, el sin fin de materiales audiovisuales que en ese repositorio se encuentran. Este programa tiene como fin facilitar la exploración del contenido de este repositorio remoto.
Características:
* Acceso rápido y bajo demanda a todos los directorios del repositorio
* Búsqueda de directorios y archivos
* Sistema de caché para almacenar la información solicitada al repositorio remoto (metadatos de los archivos y directorios)
* Previsualización del contenido de archivos de texto e imágenes
* Marcadores para archivos
* Descarga de archivos (contiene fallos, pues queda aún por desarrollar)
"""
# settings
RETRY = 10
TIMEOUT = 10
WAIT = 0.1
WORKERS = 5
THREADS = 5
CHUNK_SIZE = 1024
ICON_SIZE = 64
PREVIEW_SIZE = 256
DATE_FORMAT = "%d/%m/%Y %I:%M %p"
DATE_FROM_SERVER_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"
USER_PATH = os.path.expanduser('~')
DOWNLOAD_DIR = os.path.join(USER_PATH, 'downloads/')
# enums
MOVIE = "movie"
IMAGE = "image"
AUDIO = "audio"
TEXT = "text"
UNKNOWN = "unknown"
LAYOUT = "layout"
EXEC = "exec"
COMPRESSED = "compressed"
# visual
FILE_TYPES = {MOVIE: ":/types/images/video.png", IMAGE: ":/types/images/picture.png", AUDIO: ":/types/images/audio.png",
              TEXT: ":/types/images/doc.png", UNKNOWN: ":/types/images/uknown.png", LAYOUT: ":/types/images/pdf.png",
              EXEC: ":/types/images/software.png", COMPRESSED: ":/types/images/rar.png"}
# exceptions
CONNECTION_FAIL = "Error de conexión"
AN_ERROR_WAS_OCURRED = "Ha ocurrido un error :-("
# file extensions
AUDIO_EXT = ['aac', 'ac3', 'aif', 'aifc', 'aiff', 'au', 'cda', 'dts', 'fla', 'flac', 'it', 'm1a', 'm2a', 'm3u', 'm4a',
             'mid', 'midi', 'mka', 'mod', 'mp2', 'mp3', 'mpa', 'ogg', 'ra', 'rmi', 'spc', 'rmi', 'snd', 'umx', 'voc',
             'wav', 'wma', 'xm']
COMPRESSED_EXT = ['7z', 'ace', 'arj', 'bz2', 'cab', 'gz', 'gzip', 'jar', 'r00', 'r01', 'r02', 'r03', 'r04', 'r05',
                  'r06', 'r07', 'r08', 'r09', 'r10', 'r11', 'r12', 'r13', 'r14', 'r15', 'r16', 'r17', 'r18', 'r19',
                  'r20', 'r21', 'r22', 'r23', 'r24', 'r25', 'r26', 'r27', 'r28', 'r29', 'rar', 'tar', 'tgz', 'z', 'zip']
DOCS_EXT = ['c', 'chm', 'cpp', 'csv', 'cxx', 'doc', 'docm', 'docx', 'dot', 'dotm', 'dotx', 'h', 'hpp', 'htm', 'html',
            'hxx', 'ini', 'java', 'lua', 'mht', 'mhtml', 'odt', 'pdf', 'potx', 'potm', 'ppam', 'ppsm', 'ppsx', 'pps',
            'ppt', 'pptm', 'pptx', 'rtf', 'sldm', 'sldx', 'thmx', 'txt', 'vsd', 'wpd', 'wps', 'wri', 'xlam', 'xls',
            'xlsb', 'xlsm', 'xlsx', 'xltm', 'xltx', 'xml']
EXEC_EXT = ['bat', 'cmd', 'exe', 'msi', 'msp', 'scr']
IMG_EXT = ['ani', 'bmp', 'gif', 'ico', 'jpe', 'jpeg', 'jpg', 'pcx', 'png', 'psd', 'tga', 'tif', 'tiff', 'wmf']
VIDEO_EXT = ['3g2', '3gp', '3gp2', '3gpp', 'amr', 'amv', 'asf', 'avi', 'bdmv', 'bik', 'd2v', 'divx', 'drc', 'dsa',
             'dsm', 'dss', 'dsv', 'evo', 'f4v', 'flc', 'fli', 'flic', 'flv', 'hdmov', 'ifo', 'ivf', 'm1v', 'm2p', 'm2t',
             'm2ts', 'm2v', 'm4b', 'm4p', 'm4v', 'mkv', 'mp2v', 'mp4', 'mp4v', 'mpe', 'mpeg', 'mpg', 'mpls', 'mpv2',
             'mpv4', 'mov', 'mts', 'ogm', 'ogv', 'pss', 'pva', 'qt', 'ram', 'ratdvd', 'rm', 'rmm', 'rmvb', 'roq', 'rpm',
             'smil', 'smk', 'swf', 'tp', 'tpr', 'ts', 'vob', 'vp6', 'webm', 'wm', 'wmp', 'wmv']
APK_EXT = ['apk', 'xapk']
# content type
APPLICATION_TYPE = (
"application/EDI-X12", "application/EDIFACT", "application/javascript", "application/octet-stream", "application/ogg",
"application/pdf", "application/xhtml+xml", "application/x-shockwave-flash", "application/json", "application/ld+json",
"application/xml", "application/zip", "application/x-www-form-urlencoded")
AUDIO_TYPE = ("audio/mpeg", "audio/x-ms-wma", "audio/vnd.rn-realaudio", "audio/x-wav")
IMAGE_TYPE = (
"image/gif", "image/jpeg", "image/png", "image/tiff", "image/vnd.microsoft.icon", "image/x-icon", "image/vnd.djvu",
"image/svg+xml")
MULTIPART_TYPE = (
"multipart/mixed", "multipart/alternative", "multipart/related (using by MHTML (HTML mail).)", "multipart/form-data")
TEXT_TYPE = ("text/css", "text/csv", "text/html", "text/javascript (obsolete)", "text/plain", "text/xml")
VND_TYPE = ("application/vnd.oasis.opendocument.text", "application/vnd.oasis.opendocument.spreadsheet",
            "application/vnd.oasis.opendocument.presentation", "application/vnd.oasis.opendocument.graphics",
            "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.ms-powerpoint",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation", "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.mozilla.xul+xml")
