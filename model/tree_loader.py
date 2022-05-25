from treelib import Tree
from bs4 import BeautifulSoup
from bs4.element import Tag


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


def load_visuales_tree(html_string: str) -> Tree:
    soup = BeautifulSoup(html_string)
    link_tags = soup.find_all(name='a')

    tree = Tree()
    # Root------------
    dir_name, dir_identifier = __get_root_name_and_identifier(link_tags)
    tree.create_node(tag=dir_name, identifier=dir_identifier)
    # ----------------

    for html_tag in link_tags[1:]:
        dir_name = __get_name_of_directory(html_tag)
        dir_identifier = __get_identifier_of_directory(html_tag)
        dir_parent = __get_parent(html_tag)
        tree.create_node(tag=dir_name, identifier=dir_identifier, parent=dir_parent)

    return tree
