class Node(object):
    def __init__(self, content=None, left_child=None, right_child=None):
        self.content = content
        self.left_child = left_child
        self.right_child = right_child
 
    # Generic compare function, override in subclasses
    def __cmp__(self, other):
        if self.content < other.content:
            return -1
        if self.content == other.content:
            return 0
        if self.content > other.content:
            return 1
 
    def is_leaf(self):
        return self.left_child is None and self.right_child is None
 
 
class BinarySearchTree(object):
    def __init__(self, root, node_type):
        self.root = root
        self.size = int(root is not None)
        self.node_type = node_type
 
    def add(self, content):
        self.root = self._add(self.root, content)
 
    def _add(self, parent, content):
        if parent is None:
            self.size += 1
            return self.node_type(content)
 
        if content < parent.content:
            parent.left_child = self._add(parent.left_child, content)
        if content > parent.content:
            parent.right_child = self._add(parent.right_child, content)
        return parent
 
 
def main():
    binary_tree = BinarySearchTree(None, Node)
    for a in [21, 11, 31, 10, 15, 29, 33, 6, 14, 26, 32, 40, 3, 9, 13, 27, 41]:
        binary_tree.add(a)
 
    node = binary_tree.root
    while node is not None:
        print node.content
        node = node.right_child
 
 
if __name__ == '__main__':
    main()