#二分查找--递归
def search(sequence, number, lower=0, upper=None):
    if upper is None:
        upper = len(sequence)-1
    if lower == upper:
        assert number == sequence[upper]
        return upper
    else:
        middle = (lower + upper) // 2
        if number > sequence[middle]:
            return search(sequence, number, middle + 1, upper)
        else:
            return search(sequence, number, lower, middle)
#二分查找--普通
def search2(sequence, number, lower=0, upper=None):
    if upper is None:
        upper = len(sequence)-1
    while 1:
        if lower == upper:
            assert number == sequence[upper]
            return upper
            break
        middle = (lower + upper) // 2
        if number > sequence[middle]:
            lower = middle + 1
        else:
            upper = middle

print(search([1, 5, 8, 10, 15, 19], 0))
print(search2([1, 5, 8, 10, 15, 19], 0))
