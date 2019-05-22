'''
要求：
    在一个m行n列二维数组中，每一行都按照从左到右递增的顺序排序，每一列按照从上到下递增的顺序排序。
    完成一个函数输入这样一个二维数组和一个整数，判断数组中是否含有该整数。
Step-wise线性搜索原理:
    从右上角开始，每次将搜索值与右上角的值比较，如果大于右上角的值，则直接去除，否则去掉一列。
'''


def get_value(l, r, c):
    return l[r][c]

def find(l, x):
    m = len(l) - 1#最后一行
    n = len(l[0]) - 1#最后一列
    r = 0
    c = n
    while c >= 0 and r <= m:
        value = get_value(l, r, c)
        if value == x:
            return True
        elif value < x:
            r+=1
        elif value > x:
            c-=1
    return False

nums = [[1,4,7,11,15], [2,5,8,12,19], [3,6,9,16,22], [10,13,14,17,24], [18,21,23,26,30]]
print(find(nums, 50))
