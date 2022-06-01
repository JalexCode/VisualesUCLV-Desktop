from util.net import *
from model.tree_loader import *
from treelib import Tree, Node
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from util.util import get_directories


#dictio:Tree = load_visuales_tree(get_directories())
dictio = {"http://visuales.uclv.cu/":{"children":[{'upload': {'children': ['Upload.S02.']}}, 'vampires', 'work.in.progress', {'NETFLIX': {'children': ['Anne with an E', 'Another Life', 'Behind Her Eyes', 'Billions', 'Cable Girls', 'Cathedral of the Sea', 'Clickbait', 'Colony', 'Cursed', 'Dark', 'Greys.Anatomy', 'High Seas', 'House.of.Cards', 'Into.The.Night', 'Invisible.City', 'Jane The Virgin', 'La Casa de Papel', 'Locke and Key', 'Lucifer', 'Maid', 'Messiah', {'Peaky Blinders': {'children': ['Peaky.Blinders.x6']}}, 'Post Mortem No One Dies in Skarnes', 'Ragnarok', 'Squid Game', 'Stranger.Things', 'The Billion Dolar Code', 'The Bonfire of Destiny', 'The Chair', 'The Cook of Castamar', 'The Crown', 'The Defeated', 'The Five Juanas', 'The.One', {'The.Time.Travelers.Wife.': {'children': ['Screens']}}, 'V.Wars', 'Valeria', 'Versailles', 'Watership.Down']}}]}}
items = ["http://visuales.uclv.cu/"]

a = "2.2"
print(int(a))