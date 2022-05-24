from bs4 import BeautifulSoup
import requests

from model.tree import GeneralTree
from util.const import VISUALES_UCLV_URL, LISTADO_HTML_FILE


def get_page(url:str):
    # req = requests.get(url, verify=False)
    # if req.status_code == 200:
    #     print(req.text)
    with open("Index of _Infantiles.html", "r") as f:
        bs = BeautifulSoup(f.read())
        childrens = bs.find_all("tr")
        print(childrens[2:])


#get_page(VISUALES_UCLV_URL)
# TODO:
#  - test this method
def get_listado_file():
    req = requests.get(LISTADO_HTML_FILE, verify=False)
    print(req.text)
    if req.status_code == 200:
        with open("temp/directories.visuales", "w") as listado_file:
            listado_file.write(req.text)
            print("[OK] FILE WAS SAVED")
#get_listado_file()

def get_all_directories_tree():
    tree = GeneralTree(VISUALES_UCLV_URL)
    with open("temp/directories.visuales", "r", encoding="utf-8") as listado_file:
        bs = BeautifulSoup(listado_file.read())
        directories = bs.find_all("a")
        #
        last_directory = VISUALES_UCLV_URL
        parents = [VISUALES_UCLV_URL]
        current_level = 0
        for i in range(1, 10):
            directory = directories[i]
            next_directory = directories[i + 1].get("href") if i < 10 else ""
            directory_href = directory.get("href")
            print("LAST:", last_directory)
            directory_name = directory_href.replace(last_directory, "")
            print("CURRENT:", directory_name)
            # tree.add_child(last_directory, href)
            if directory_href in next_directory:
                if last_directory not in directory_href:
                    print("IT'S HAPPENING")
                    current_level -= 1
                    last_directory = parents[current_level]
                    parents = parents[:current_level]
                    continue
                last_directory = directory_href
                parents.append(directory_href)
                current_level += 1
        # for i in tree.preorder():
        #     print(i)


get_all_directories_tree()