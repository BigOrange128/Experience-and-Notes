#二叉树节点
class Node(object):
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
tree = Node(1, Node(3, Node(7, Node(0)), Node(6)), Node(2, Node(5), Node(4)))

#层次遍历
def lookup(root):
    row = [root]
    while row:
        print(row)
        for i in row:
            print(i.data, end='')
        row = [kid for item in row for kid in (item.left, item.right) if kid]
lookup(tree)
#深度遍历
def deep(root):
    if not root:
        return
    print(root.data)
    deep(root.left)
    deep(root.right)
deep(tree)
#前序
def pre_travelsal(root):
    print(root.value)
    if root.left is not None:
        pre_travelsal(root.left)
    if root.right is not None:
        pre_travelsal(root.right)
#中序
def mid_travelsal(root):
    if root.left is not None:
        mid_travelsal(root.left)
    print(root.value)
    if root.right is not None:
        mid_travelsal(root.right)
#后序
def post_travelsal(root):
    if root.left is not None:
        post_travelsal(root.left)
    if root.right is not None:
        post_travelsal(root.right)
    print(root.value)
