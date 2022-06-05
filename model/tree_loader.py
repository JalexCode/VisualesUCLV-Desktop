from treelib import Tree
from bs4 import BeautifulSoup
from bs4.element import Tag
import time
from model.folder_node import FolderNode
#import pdb

def __get_parent(element: Tag) -> str:
    href = element.attrs['href']
    last_slash_index = href[:-1].rfind('/')
    return href[:last_slash_index + 1]


def __get_name_of_directory(element:Tag) -> str:
    return element.text


def __get_identifier_of_directory(element: Tag) -> str:
    return element.attrs['href']


def __get_root_name_and_identifier(link_tags: list) -> tuple:
    visuales_root_tag = link_tags[0]
    dir_name = __get_name_of_directory(visuales_root_tag)
    dir_identifier = __get_identifier_of_directory(visuales_root_tag) + '/'
    return dir_name, dir_identifier


def load_visuales_tree(html_string: str, progress_signal=None) -> Tree:
    #pdb.set_trace()
    soup = BeautifulSoup(markup=html_string, features="lxml")
    link_tags = soup.find_all(name='a')
    #
    tree = Tree()
    # Root------------
    dir_name, dir_identifier = __get_root_name_and_identifier(link_tags)
    tree.create_node(tag=FolderNode(dir_name, False, False), identifier=dir_identifier)
    # ----------------
    t0 = time.time()
    tags = link_tags[1:]
    for i in range(len(tags)):
        html_tag = tags[i]
        dir_name = __get_name_of_directory(html_tag)
        dir_identifier = __get_identifier_of_directory(html_tag)
        dir_parent = __get_parent(html_tag)
        tree.create_node(tag=FolderNode(dir_name, False, False), identifier=dir_identifier, parent=dir_parent)
        #
        if progress_signal is not None:
            i += 1
            delay = time.time() - t0
            # calculate percent
            percent = i * 100 // len(tags) + 1
            # speed
            speed = int(i // (delay + 1))
            # left_time
            left_time = ((len(tags) + 1) - i) / speed if speed > 0 else 1
            # emit
            progress_signal.emit(percent, speed, left_time)
    return tree
