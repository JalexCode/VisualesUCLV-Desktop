import pickle

from model.file_node import FileNode
from util.const import *
from model.exceptions import *
from treelib import Node, Tree

try:
    os.mkdir(Paths.DATA_FOLDER)
except:
    pass


def get_html_file_content() -> str:
    """
    Load 'listado.html' file content
    :return:
    """
    if os.path.exists(Paths.DIR_FILE):
        with open(Paths.DIR_FILE, "r", encoding="utf-8", errors="ignore") as listado_file:
            return listado_file.read()
    raise DirsFileDoesntExistException(f"No se encontró el fichero {Paths.DIRS_FILE_NAME}")


def has_children(tree: Tree, node: Node) -> bool:
    """
    Check if a folder has at least one File
    :param tree:
    :param node:
    :return:
    """
    children = tree.children(node.identifier)
    for child in children:
        if isinstance(child.tag, FileNode):
            return True
    return False


def get_test_tree():
    tree = Tree()
    tree.create_node(tag='http://visuales.uclv.cu/',
                     identifier='http://visuales.uclv.cu/')
    tree.create_node(tag='Cursos',
                     identifier='http://visuales.uclv.cu//Cursos/'
                     , parent='http://visuales.uclv.cu/')
    tree.create_node(tag='Libros',
                     identifier='http://visuales.uclv.cu//Cursos/Libros/',
                     parent='http://visuales.uclv.cu//Cursos/')
    tree.create_node(tag='Java',
                     identifier='http://visuales.uclv.cu//Cursos/Libros/Java/',
                     parent='http://visuales.uclv.cu//Cursos/Libros/')
    tree.create_node(tag='Python',
                     identifier='http://visuales.uclv.cu//Cursos/Libros/Python/',
                     parent='http://visuales.uclv.cu//Cursos/Libros/')
    tree.create_node(tag='Pelis',
                     identifier='http://visuales.uclv.cu//Pelis/',
                     parent='http://visuales.uclv.cu/')
    tree.create_node(tag='La vida es bella',
                     identifier='http://visuales.uclv.cu//Pelis/La vida es bella/',
                     parent='http://visuales.uclv.cu//Pelis/')
    tree.create_node(tag='Gravity',
                     identifier='http://visuales.uclv.cu//Pelis/Gravity/',
                     parent='http://visuales.uclv.cu//Pelis/')
    return tree


def load_all_dirs_n_files_tree() -> Tree:
    """
    Load serialized Tree object
    :return: Tree
    """
    if os.path.exists(Paths.TREE_FILE):
        with open(Paths.TREE_FILE, "rb") as serialized_data:
            return pickle.load(serialized_data)
    raise TreeFileDoesntExistException(f"No se encontró el fichero {Paths.TREE_DATA_FILE_NAME}")


def save_all_dirs_n_files_tree(tree: Tree) -> None:
    """
    Saves Tree in a file with pickle
    :param tree:
    :return:
    """
    if tree.size(0):
        with open(Paths.TREE_FILE, "wb") as serialized_data:
            return pickle.dump(tree, serialized_data)


def add_file_nodes_2_tree(tree: Tree, parent: Node, nodes: list) -> None:
    """
    Adds FileNodes to a FolderNode in Tree
    :param tree:
    :param parent:
    :param nodes:
    :return:
    """
    for node in nodes:
        tree.create_node(tag=node, identifier=node.href, parent=parent.identifier)


def get_total_size(nodes: list) -> int:
    """
    Returns the sum of all file size in folder
    :param nodes:
    :return:
    """
    total = 0
    for node in nodes:
        if isinstance(node.tag, FileNode):
            total += node.tag.size
    return total


def get_type(url: str) -> str:
    """
    Returns a file type
    :param url:
    :return:
    """
    splitted = url.split("/")
    raw_type = splitted[-1]
    if AppEnums.MOVIE in raw_type:
        return AppEnums.MOVIE
    elif AppEnums.IMAGE in raw_type:
        return AppEnums.IMAGE
    elif AppEnums.TEXT in raw_type:
        return AppEnums.TEXT
    elif AppEnums.LAYOUT in raw_type:
        return AppEnums.LAYOUT
    return AppEnums.UNKNOWN


def search(tree: Tree, text: str) -> list:
    """
    Search nodes in the Tree that contains the given text
    :param tree:
    :param text:
    :return:
    """
    result = tree.filter_nodes(
        lambda node: (text.lower() in str(node.tag).lower()) if isinstance(node.tag, FileNode) else (
                text.lower() in str(node.tag).lower()))
    return list(result)


def filter_favorites(tree: Tree) -> list:
    """
    Search nodes in the Tree that are checked as Favorite
    :param tree:
    :return list:
    """

    def filter(node):
        if node.tag.favorite:
            print(node.tag)
            return node

    result = tree.filter_nodes(filter)
    return list(result)


# >---------------------------------------------------------------------------------------------------------------------<
import math


def get_bytes(size_str: str) -> float:
    if size_str.isnumeric():
        total_bytes = float(size_str)
    else:
        total_bytes = float(size_str[:-1])
        if "K" in size_str:
            total_bytes *= 1000
        elif "M" in size_str:
            total_bytes *= 1000000
        elif "G" in size_str:
            total_bytes *= 1000000000
    return total_bytes


def nz(size_bytes) -> str:
    """
    Humanize data meassure
    :param size_bytes:
    :return:
    """
    if size_bytes == 0:
        return "0.0 B"
    size_name = ("B", "KB", "MB", "GB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def nd(segundos: 'int') -> str:
    """
    Humanize time
    :param segundos:
    :return:
    """
    horas = int(segundos // 3600)
    segundos -= horas * 3600
    minutos = int(segundos // 60)
    segundos -= minutos * 60
    return "%02d:%02d:%02d" % (horas, minutos, segundos)


def get_file_type(file: FileNode) -> None:
    ext = os.path.splitext(file.filename)
    ext = ext[1].replace(".", "")
    ext = ext.lower()

    if ext in FileExtensions["AUDIO"]:
        file.type = AppEnums.AUDIO
    elif ext in FileExtensions["COMPRESSED"]:
        file.type = AppEnums.COMPRESSED
    elif ext in FileExtensions["DOCS"]:
        file.type = AppEnums.TEXT
    elif ext in FileExtensions["EXEC"]:
        file.type = AppEnums.EXEC
    elif ext in FileExtensions["IMG"]:
        file.type = AppEnums.IMAGE
    elif ext in FileExtensions["VIDEO"]:
        file.type = AppEnums.MOVIE
    else:
        file.type = AppEnums.UNKNOWN
