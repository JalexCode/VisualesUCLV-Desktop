from collections import deque


class GeneralTree:

    def __init__(self, root=None):
        self._root = root
        self._sub_trees = []

    @property
    def root(self):
        return self._root

    @property
    def sub_trees(self):
        return self._sub_trees

    def add_child(self, parent, child):
        added = False
        tmp = GeneralTree(child)
        if parent == None:
            self._root = child
            added = True
        if parent == self._root:
            self._sub_trees.append(tmp)
            added = True
        else:
            for tree in self._sub_trees:
                added = tree.add_child(parent, child)
                if added: return True
        return added

    def search(self, element):
        found = False
        if element == self._root:
            found = True
        else:
            for tree in self._sub_trees:
                found = tree.search(element)
                if found:
                    return True
        return found

    def is_empty(self):
        return self._root is None

    def is_leaf(self):
        return len(self._sub_trees) == 0

    def preorder(self):
        pre_order = [self._root]
        for general_tree in self._sub_trees:
            pre_order.append(general_tree.preorder())
        return pre_order

    def postorder(self, post_order):
        post_order = []
        for general_tree in self._sub_trees:
            post_order.append(general_tree.postorder(post_order))
        post_order.append(self._root)
        return post_order

    def inorder(self, in_order):
        if self.is_leaf():
            in_order.append(self._root)
        else:
            self._sub_trees[0].inorder(in_order)
            in_order.append(self._root)
            if len(self._sub_trees) > 1:
                for tree in self._sub_trees[1:]:
                    tree.inorder(in_order)
        return in_order

    def bfs(self):
        wide = []
        queue = deque()
        queue.append(self)
        while len(queue) > 0:
            wide.append(queue[0].root)
            for tree in queue.popleft().sub_trees:
                queue.append(tree)
        return wide

    def __str__(self):
        print(self._root)