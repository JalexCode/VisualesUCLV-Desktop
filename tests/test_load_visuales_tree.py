import unittest
from treelib import Tree

from model.tree_loader import load_visuales_tree


class TestLoadVisualesTree(unittest.TestCase):
    HTML_TEXT = '''
    
    <a href="http://visuales.uclv.cu/">http://visuales.uclv.cu/</a><br>
        <a href="http://visuales.uclv.cu//Cursos/">Cursos</a><br>
            <a href="http://visuales.uclv.cu//Cursos/Libros/">Libros</a><br>
                <a href="http://visuales.uclv.cu//Cursos/Libros/Java/">Java</a><br>
                <a href="http://visuales.uclv.cu//Cursos/Libros/Python/">Python</a><br>
        <a href="http://visuales.uclv.cu//Pelis/">Pelis</a><br>
            <a href="http://visuales.uclv.cu//Pelis/La vida es bella/">La vida es bella</a><br>
            <a href="http://visuales.uclv.cu//Pelis/Gravity/">Gravity</a><br>
    
    '''

    def get_testing_tree(self):
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

    def test_load_is_done_correctly(self):
        print('EXPECTED TREE')
        print(self.get_testing_tree())

        print('\n\n\nRETRIEVED TREE')
        print(load_visuales_tree(self.HTML_TEXT))


if __name__ == '__name__':
    unittest.main()
