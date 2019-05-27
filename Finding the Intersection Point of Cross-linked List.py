class ListNode:
    def __init__(self, x, next = None):
        self.value = x
        self.next = next

def node(l1, l2):
    length1, length2 = 0, 0
    #计算链表长度
    l11 = l1
    l22 = l2
    while l11:
        l11 = l11.next#尾节点
        length1 += 1
    while l22:
        l22 = l22.next
        length2 += 1
    print(length1, length2)
        #是否相交
    #长链表先行
    if length1 > length2:
        for _ in range(length1 - length2):
            l1 = l1.next
            print(l1.value)
    else:
        for _ in range(length2 - length1):
            l2 = l2.next
            print(l2.value)
    while l1 and l2:
        if l1.next == l2.next:
            return l1.next
        else:
            l1 = l1.next
            l2 = l2.next


head1 = ListNode(1)
head12 = ListNode(2)
head13 = ListNode(3)
head14 = ListNode(4)
head1.next = head12
head12.next = head13
head13.next = head14

head2 = ListNode(5, head13)

conclusion = node(head1, head2)
print(conclusion, conclusion.value)
