from django.http import HttpResponseForbidden
from treelib import Tree, Node
from bs4 import BeautifulSoup, Tag
import requests
from model.exceptions import BadServerResponseException
from model.file_node import FileNode
from contextlib import closing
from util.const import *
from util.util import *

def get_page(url:str, parent:str=""):
    files = []
    with closing(requests.get(url, verify=False)) as req:
        if req.status_code == 200:
        #with open("Index of _Cursos_Adobe.Photoshop.CC.from.A-Z.Begginner.to.Master_1. Introduction.html", "r") as f:#Index of _Cursos_Adobe.Photoshop.CC.from.A-Z.Begginner.to.Master_1. Introduction #Index of _Infantiles
            bs = BeautifulSoup(req.content)
            children = bs.find_all("td")[5:]
            for i in range(0, len(children), 5):
                size = children[i + 3].get_text().strip()
                # if isnt a folder
                if size != "-":
                    # get multimedia files data
                    size = get_bytes(size)
                    type = get_type(children[i].find("img").attrs['src'])
                    filename = children[i + 1].get_text().strip()
                    modificated_date = children[i + 2].get_text().strip()
                    href = parent + children[i + 1].find("a").attrs['href']
                    print(href)
                    files.append(FileNode(filename, modificated_date, size, href, type))
    return files

def download_listado_file():
    with closing(requests.get(LISTADO_HTML_FILE, verify=False)) as req:
        if req.status_code == 200:
            with open(DIR_FILE, "w", encoding="utf-8") as listado_file:
                listado_file.write(req.text)
                print("[OK] FILE WAS SAVED")
        else:
            raise BadServerResponseException(req.status_code)