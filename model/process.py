from datetime import datetime
from bs4 import BeautifulSoup
import requests
from contextlib import closing

from model.tree_loader import load_visuales_tree
from util.util import *
import time

class Request:
    def __init__(self):
        pass

    def signals(self, info_signal, progress_signal, error, finish):
        self.info_signal = info_signal
        self.progress_signal = progress_signal
        self.error_signal = error
        self.finish_signal = finish

    def request_file(self):
        '''
        Gets listado.html 'Last-Modified' header
        :return:
        '''
        try:
            self.info_signal.emit("Solicitando datos remotos...")
            with closing(requests.get(LISTADO_HTML_FILE, verify=False)) as response:
                if response.status_code == 200:
                    #
                    self.info_signal.emit("Datos remotos obtenidos")
                    self.finish_signal.emit(response.headers['Last-Modified'])
                else:
                    raise BadServerResponseException(response.status_code)
        except Exception as error:
            self.error_signal.emit(error)

    def download_file(self):
        '''
        Download listado.html file in stream mode
        :return:
        '''
        try:
            self.info_signal.emit("Solicitando datos remotos...")
            with closing(requests.get(LISTADO_HTML_FILE, verify=False, timeout=TIMEOUT, stream=True)) as response:
                if response.status_code == 200:
                    self.info_signal.emit(f"Inicializando archivo '{DIRS_FILE_NAME}'...")
                    #
                    with open(DIR_FILE, "w", encoding="utf-8") as listado_file:
                        listado_file.write("")
                    #
                    self.info_signal.emit("Descargando...")
                    # file size...in bytes
                    file_size = len(response.content)
                    # file data that has been downloaded [in bytes]
                    downloaded = 0
                    with open(DIR_FILE, "a", encoding="utf-8") as listado_file:
                        t0 = time.time()
                        for data in response.iter_content(chunk_size=CHUNK_SIZE):
                            # write data on fie
                            listado_file.write(data.decode("utf-8", errors="ignore"))
                            # update state data
                            downloaded += len(data)
                            # elapsed time
                            delay = time.time() - t0
                            # calculate percent
                            percent = downloaded * 100 // file_size
                            # download speed
                            speed = int(downloaded // (delay + 1))
                            # left_time
                            left_time = (file_size - downloaded) / speed if speed > 0 else 1
                            # emit progress signal
                            self.progress_signal.emit(percent, speed, left_time)
                    print("[OK] FILE WAS SAVED")
                    # finish
                    self.info_signal.emit(f"Archivo guardado en '{DIRS_FILE_NAME}'")
                    self.finish_signal.emit(True)
                else:
                    raise BadServerResponseException(response.status_code)
        except Exception as error:
            self.error_signal.emit(error)

    def get_page(self, url: str, parent: str = ""):
        '''
        Get all files metadata in the given page
        :param url:
        :param parent:
        :return:
        '''
        self.info_signal.emit("Solicitando datos remotos...")
        files = []
        try:
            with closing(requests.get(url, verify=False, timeout=TIMEOUT)) as response:
                if response.status_code == 200:
                    self.info_signal.emit("Leyendo datos...")
                    # paarse data
                    bs = BeautifulSoup(response.text)
                    children = bs.find_all("td")[5:]
                    for i in range(0, len(children), 5):
                        size = children[i + 3].get_text().strip()
                        # if isn't a folder (then is a file, obviusly ;-;)
                        if size != "-":
                            # get files metadata
                            size = get_bytes(size)
                            type = get_type(children[i].find("img").attrs['src'])
                            filename = children[i + 1].get_text().strip()
                            modificated_date = children[i + 2].get_text().strip()
                            modificated_date = datetime.fromisoformat(modificated_date)
                            href = parent + children[i + 1].find("a").attrs['href']
                            files.append(FileNode(filename, modificated_date, size, href, type))
                            # emit progress signal
                            self.progress_signal.emit(i * 100 // len(children) * 5, None, None)
            self.finish_signal.emit(files)
        except Exception as error:
            self.error_signal.emit(error)

    def read_html_file(self):
        self.info_signal.emit(f"Leyendo archivo {DIRS_FILE_NAME}")
        try:
            html_str = get_directories()
            self.info_signal.emit(f"Parseando archivo {DIRS_FILE_NAME}")
            tree = load_visuales_tree(html_str, self.progress_signal)
            self.finish_signal.emit(tree)
        except Exception as error:
            if isinstance(error, DirsFileDoesntExistException):
                print(f"\tTarea fallida [{DIRS_FILE_NAME}]")
            print("\t" + str(error.args[0]))
            self.error_signal.emit(error)
