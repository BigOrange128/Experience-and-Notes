#树节点
class Node(object):
    def __init__(self, value, left = None, right = None):
        self.value = value
        self.left = left
        self.right = right
tree = Node(1, Node(3, Node(7, Node(0)), Node(6)), Node(2, Node(5), Node(4)))
tree2 = Node(1, Node(3, Node(7, Node(0)), Node(6)), Node(2, Node(5), Node(8)))
#求最大树深
def MaxDepth(root):
    if not root:
        return 0
    return max(MaxDepth(root.right), MaxDepth(root.left)) + 1

print(MaxDepth(tree))
#求两棵树是否相同
def IsSameTree(p, q):
    if p == None and q == None:
        return True
    elif p and q:
        return p.value == q.value and IsSameTree(p.left, q.left) and IsSameTree(p.right, q.right)
    else:
        return False
print(IsSameTree(tree, tree2))
#前序中序求后序
pre= "ABDGCEFH"
mid = "DGBAECHF"
def rebuild(pre, mid):
    if not pre:
        return
    cur = Node(pre[0])
    index = mid.index(pre[0])
    cur.left = rebuild(pre[1:index + 1], mid[:index])
    cur.right = rebuild(pre[index + 1:], mid[index + 1:])
    return cur
tree3 = rebuild(pre, mid)
