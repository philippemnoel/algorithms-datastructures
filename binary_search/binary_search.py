"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Philippe M. Noël
Binary Search Tree Class & Binary Search Implementations -- Python 3
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class Node:
    def __init__(self, k):
        self.val = k
        self.leftchild = None
        self.rightchild = None

    def get(self):
        return self.val
        
    def set(self, k):
        self.val = k

    def getChildren(self):
        children = []
        if self.left != None:
            children.append(self.leftchild)
        if self.right != None:
            children.append(self.rightchild)
        return children


class BST:
    def __init__(self):
        self.root = None

    def setRoot(self, k):
        self.root = Node(k)

    def insertNode(self, curr_node, k):
        """ Recursive insertion preserving the invariant """
        if k <= curr_node.val:
            if curr_node.leftchild:
                self.insertNode(curr_node.leftchild, k)
            else:
                curr_node.leftchild = Node(k)
        elif k > curr_node.val:
            if curr_node.rightchild:
                self.insertNode(curr_node.rightchild, k)
            else:
                curr_node.rightchild = Node(k)

    def insert(self, k):
        if self.root is None:
            self.setRoot(k)
        else:
            self.insertNode(self.root, k)

    def findNode(self, curr_node, k):
        """ Recursive binary search """
        if curr_node is None:
            return False # no such node
        elif k == curr_node.val:
            return True # node found
        elif k < curr_node.val:
            return self.findNode(curr_node.leftchild, k)
        else:
            return self.findNode(curr_node.rightchild, k)

    def find(self, k):
        return self.findNode(self.root, k)
