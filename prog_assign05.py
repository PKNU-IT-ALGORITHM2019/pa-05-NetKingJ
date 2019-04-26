class Node(object):
    def __init__(self, word, pos, mean):
        self.word = word
        self.pos = pos
        self.mean = mean
        self.left = self.right = None

class BST(object):
    def __init__(self):
        self.root = None

    def insert(self, word, pos, mean):
        self.root = self._insert_value(self.root, word, pos, mean)
        return self.root is not None

    def _insert_value(self, node, word, pos, mean):
        if node is None:
            node = Node(word, pos, mean)
        else:
            if word <= node.word:
                node.left = self._insert_value(node.left, word, pos, mean)
            else:
                node.right = self._insert_value(node.right, word, pos, mean)
        return node

    def find(self, key):
        return self._find_value(self.root, key)

    def _find_value(self, root, key):
        if root is None:
            return False
        if root.word == key:
            return root

        elif key < root.word:
            return self._find_value(root.left, key)
        else:
            return self._find_value(root.right, key)

    def delete(self, key):
        self.root, deleted = self._delete_value(self.root, key)
        return deleted

    def _delete_value(self, node, key):
        if node is None:
            return node, False
        deleted = False
        if key == node.word:
            deleted = True
            if node.left and node.right:
                parent, child = node, node.right
                while child.left is not None:
                    parent, child = child, child.left
                child.left = node.left
                if parent != node:
                    parent.left = child.right
                    child.right = node.right
                node = child
            elif node.left or node.right:
                node = node.left or node.right
            else:
                node = None
        elif key < node.word:
            node.left, deleted = self._delete_value(node.left, key)
        else:
            node.right, deleted = self._delete_value(node.right, key)
        return node, deleted

    def node_count(self,node):
        if node == None:
            return 0
        return 1 + self.node_count(node.right) + self.node_count(node.left)

fp = open("shuffled_dict.txt","r",encoding="utf-8")
BST = BST()
while True:
    word = fp.readline().split("\n")[0]
    if not word:
        break
    wpm = word.split()
    word = wpm[0]
    pos = wpm[1]
    mean = ''
    for i in wpm[2:]:
        mean += i + ' '
    BST.insert(word, pos, mean)
fp.close()

while True:
    cmd1 = cmd = ''
    cmd = input("$ ")
    tmp = cmd.split()
    cmd1 = cmd2 = ''
    if len(tmp) > 1:
        cmd2 = tmp[1]
    cmd1 = tmp[0]
    
    if cmd1 == "size":
        print(BST.node_count(BST.root))

    if cmd1 == "find":
        key = cmd2
        result = BST.find(key)
        if result != False:
            print(result.word + ' ' + result.pos + ' ' + result.mean)
        else:
            print("Not Found.")

    if cmd1 == "add":
        word,pos,mean = input("word: "),input("class:  "),input("meaning: ")
        pos = "(" + pos + ".)"
        BST.insert(word, pos, mean)

    if cmd1 == "delete":
        key = cmd2
        if BST.delete(key):
            print("Deleted successfully.")
        else:
            print("Not found.")

    if cmd1 == "deleteall":
        filename=cmd2
        fp = open(filename,"r",encoding="utf-8")
        af = BST.node_count(BST.root)
        while True:
            del_word = fp.readline().split("\n")[0]
            if not del_word:
                break
            BST.delete(del_word)
        bf = BST.node_count(BST.root)
        fp.close()
        print("%d words were deleted successfully." % int(af-bf))
