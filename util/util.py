import pickle

from model.file_node import FileNode
from model.folder_node import FolderNode
from util.const import *
from model.exceptions import *
from treelib import Node, Tree
try:
    os.mkdir(DATA_FOLDER)
except:
    pass

def get_directories() -> str:
    '''
    Load 'listado.html' file content
    :return:
    '''
    if os.path.exists(DIR_FILE):
        with open(DIR_FILE, "r", encoding="utf-8") as listado_file:
            return listado_file.read()
    raise DirsFileDoesntExistException(f"No se encontró el fichero {DIRS_FILE_NAME}")

def have_children(tree:Tree, node:Node) -> bool:
    '''
    check if a folder has at least one File
    :param tree:
    :param node:
    :return:
    '''
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
                        ,parent='http://visuales.uclv.cu/')
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
    '''
    Load serialized Tree object
    :return: Tree
    '''
    if os.path.exists(TREE_FILE):
        with open(TREE_FILE, "rb") as serialized_data:
            return pickle.load(serialized_data)
    raise TreeFileDoesntExistException(f"No se encontró el fichero {TREE_DATA_FILE_NAME}")
    
def save_all_dirs_n_files_tree(tree:Tree) -> None:
    '''
    Saves Tree in a file with pickle
    :param tree:
    :return:
    '''
    if tree.size(0):
        with open(TREE_FILE, "wb") as serialized_data:
            return pickle.dump(tree, serialized_data)
    
def add_file_nodes_2_tree(tree:Tree, parent:Node, nodes:list) -> None:
    '''
    Adds FileNodes to a FolderNode in Tree
    :param tree:
    :param parent:
    :param nodes:
    :return:
    '''
    for node in nodes:
        tree.create_node(tag=node, identifier=node.href, parent=parent.identifier)
        
def get_total_size(nodes:list) -> int:
    '''
    Returns the sum of all file size in folder
    :param nodes:
    :return:
    '''
    total = 0
    for node in nodes:
        if isinstance(node.tag, FileNode):
            total += node.tag.size
    return total

def get_type(url:str) -> str:
    '''
    Returns a file type
    :param url:
    :return:
    '''
    splitted = url.split("/")
    raw_type = splitted[-1]
    if "movie" in raw_type:
        return MOVIE
    elif "image" in raw_type:
        return PICTURE
    elif "text" in raw_type:
        return TEXT
    elif "layout" in raw_type:
        return LAYOUT
    return UNKNOWN

def search(tree:Tree, text:str) -> list:
    '''
    Search nodes in the Tree that contains the given text
    :param tree:
    :param text:
    :return:
    '''
    result = tree.filter_nodes(lambda node: (text.lower() in str(node.tag).lower()) if isinstance(node.tag, FileNode) else (text.lower() in str(node.tag).lower()))
    return list(result)
def filter_favorites(tree:Tree) -> list:
    '''
    Search nodes in the Tree that are checked as Favorite
    :param tree:
    :return list:
    '''
    def filter(node):
        if isinstance(node.tag, FolderNode) and node.tag.favorite:
            return node
    result = tree.filter_nodes(filter)
    return list(result)
# >---------------------------------------------------------------------------------------------------------------------<
import math

def get_bytes(size_str:str) -> float:
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
    if size_bytes == 0:
        return "0.0 B"
    size_name = ("B", "KB", "MB", "GB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def nd(segundos:'int') -> str:
    horas = int(segundos // 3600)
    segundos -= horas * 3600
    minutos = int(segundos // 60)
    segundos -= minutos * 60
    return "%02d:%02d:%02d" % (horas, minutos, segundos)