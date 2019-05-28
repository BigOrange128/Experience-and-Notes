def QuickSort(lis):
    if len(lis) < 2:
        return lis
    else:
        low = [i for i in lis[1:] if i <= lis[0]]
        high = [i for i in lis[1:] if i > lis[0]]
        finallylist = QuickSort(low) + [lis[0]] + QuickSort(high)
        return finallylist
#匿名函数一句话版
quick_sort = lambda lis : lis if len(lis) < 2 else quick_sort([i for i in lis[1:] if i <= lis[0]]) + [lis[0]] + quick_sort([i for i in lis[1:] if i > lis[0]])

print(QuickSort([2, 8, 3, 1, 4, 6, 5, 1]))
