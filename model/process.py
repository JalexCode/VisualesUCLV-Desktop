import time
from contextlib import closing
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from util.tree_loader import load_visuales_tree
from util.util import *


class Request:
    """
    This class contains methods that must be called by a QObject to work in async mode
    """

    def __init__(self):
        self.finish_signal = None
        self.error_signal = None
        self.progress_signal = None
        self.info_signal = None

    def signals(self, info_signal, progress_signal, error, finish):
        self.info_signal = info_signal
        self.progress_signal = progress_signal
        self.error_signal = error
        self.finish_signal = finish

    def request_file(self):
        """
        Gets listado.html file 'size' and 'last modification date' attributes
        :return:
        """
        try:
            self.info_signal.emit("Solicitando datos remotos...")
            with closing(requests.get(Paths.VISUALES_UCLV_URL, verify=False, timeout=AppSettings.TIMEOUT)) as response:
                if response.status_code == 200:
                    # parse data
                    bs = BeautifulSoup(response.text, features="lxml")
                    children = bs.find_all("td")[4:]
                    for i in range(0, len(children), 5):
                        try:
                            filename = children[i + 2].get_text().strip()
                        except:
                            filename = ""

                        if filename == "listado.html":
                            # get files metadata
                            size = children[i + 4].get_text().strip()
                            size = get_bytes(size)
                            modificated_date = children[i + 3].get_text().strip()
                            modificated_date = datetime.fromisoformat(modificated_date)
                            # return 'listado.html' file info
                            self.info_signal.emit("Datos remotos obtenidos")
                            self.finish_signal.emit(FileNode(filename=DIRS_FILE_NAME, modification_date=modificated_date, size=size, href=LISTADO_HTML_FILE, type=TEXT)) #response.headers['Last-Modified']
                            return
                    self.error_signal.emit(Exception("No se obtuvieron los datos del listado"))
                else:
                    raise BadResponseException(response.status_code)
        except Exception as error:
            self.error_signal.emit(error)

    def write_content_on_file(self, response: requests.Response, file_to_write: FileNode, mode: str = "wb",
                              destiny: str = Paths.DOWNLOAD_DIR):
        # destiny file
        download_path = os.path.join(destiny, file_to_write.filename)
        #
        self.info_signal.emit(f"Descargando '{file_to_write.filename}'")
        # file size...in bytes
        file_size = file_to_write.size
        print(file_size)
        if not file_size:
            file_size = int(response.headers['content-length'])
        # file data that has been downloaded [in bytes]
        downloaded = 0
        with open(file=download_path, mode=mode) as listado_file:
            t0 = time.time()
            for data in response.iter_content(chunk_size=AppSettings.CHUNK_SIZE):
                # write data on fie
                listado_file.write(data)
                # update state data
                downloaded += len(data)
                # elapsed time
                delay = time.time() - t0
                # calculate percent
                percent = downloaded * 100 // file_size
                # download speed
                speed = int(downloaded // (delay + 1))
                # left time to finish download
                left_time = (file_size - downloaded) / speed if speed > 0 else 1
                # emit progress signal
                self.progress_signal.emit(percent, speed, left_time)
        print("[OK] FILE WAS SAVED")
        # finish
        self.info_signal.emit(f"Archivo guardado en: '{download_path}'")
        self.finish_signal.emit(True)

    def download_file(self, file: FileNode, destiny: str = Paths.DOWNLOAD_DIR):
        """
        Download a file in stream mode
        :return:
        """
        try:
            self.info_signal.emit("Solicitando datos remotos...")
            with closing(requests.get(file.href, verify=False, timeout=AppSettings.TIMEOUT, stream=True)) as response:
                if response.status_code == 200:
                    #
                    self.write_content_on_file(response=response, file_to_write=file, destiny=destiny)
                else:
                    raise BadResponseException(response.status_code)
        except Exception as error:
            self.error_signal.emit(error)

    def get_page(self, url: str, parent: str = ""):
        """
        Get all files metadata in the given page
        :param url:
        :param parent:
        :return:
        """
        self.info_signal.emit("Solicitando datos remotos...")
        files = []
        try:
            with closing(requests.get(url, verify=False, timeout=AppSettings.TIMEOUT)) as response:

                response.raise_for_status()
                if response.status_code == 200:
                    self.info_signal.emit("Leyendo datos...")
                    # paarse data
                    bs = BeautifulSoup(response.text, features="lxml")
                    children = bs.find_all("td")[5:]
                    for i in range(0, len(children), 5):
                        size = children[i + 3].get_text().strip()
                        # if isn't a folder (then is a file, obviusly ;-;)
                        if size != "-":
                            # get files metadata
                            size = get_bytes(size)
                            the_type = get_type(children[i].find("img").attrs['src'])
                            filename = children[i + 1].get_text().strip()
                            modificated_date = datetime.fromisoformat(
                                children[i + 2].get_text().strip()
                            )
                            href = parent + children[i + 1].find("a").attrs['href']
                            # add to list
                            files.append(FileNode(filename, modificated_date, size, href, the_type))
                            # emit progress signal
                            self.progress_signal.emit(i * 100 // len(children) * 5, None, None)
                else:
                    BadResponseException(response.status_code)
            self.finish_signal.emit(files)
        except Exception as error:
            self.error_signal.emit(error)

    def read_html_file(self):
        """
        Parse the html content in '.visuales' file
        :return:
        """
        self.info_signal.emit(f"Leyendo archivo {Paths.DIRS_FILE_NAME}")
        try:
            html_str = get_html_file_content()
            self.info_signal.emit(f"Parseando archivo {Paths.DIRS_FILE_NAME}")
            tree = load_visuales_tree(html_str, self.progress_signal)
            self.finish_signal.emit(tree)
        except Exception as error:
            if isinstance(error, DirsFileDoesntExistException):
                print(f"\tTarea fallida [{Paths.DIRS_FILE_NAME}]")
            print("\t" + str(error.args[0]))
            self.error_signal.emit(error)

    def get_light_weight_file(self, url: str):
        """
        Get a text or image file content
        :param url:
        :return:
        """
        self.info_signal.emit("Solicitando archivo remoto...")
        try:
            with closing(requests.get(url, verify=False)) as response:
                if response.status_code == 200:
                    self.info_signal.emit("Obteniendo datos...")
                    # send data
                    self.finish_signal.emit(response.content)
                    self.info_signal.emit("Datos obtenidos")
                    # emit progress
                    self.progress_signal.emit(100, None, None)
                else:
                    raise BadResponseException(response.status_code)
        except Exception as error:
            if isinstance(error, DirsFileDoesntExistException):
                print(f"\tTarea fallida [{Paths.DIRS_FILE_NAME}]")
            print("\t" + str(error.args[0]))
            self.error_signal.emit(error)
