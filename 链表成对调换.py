'''
将1->2->3->4转换成2->1->4->3
'''
class ListNode:
    def __init__(self, x, n = None):
        self.value = x
        self.next = n

#递归
# class Solution:
#     def swapPairs(self, head):
#         if head != None and head.next != None:
#             next = head.next
#             head.next = self.swapPairs(next.next)
#             next.next = head
#             return next
#         return head
#双指针交换值
class Solution:
    def swapPairs(self, head):
        try:
            prev = head
            tail = prev.next
            while True:
                prev.value, tail.value = tail.value, prev.value
                prev = tail.next
                tail = prev.next
        finally:
            return head
#测试       
head1 = ListNode(1, ListNode(2, ListNode(3, ListNode(4))))
print(head1.value, head1.next.value, head1.next.next.value, head1.next.next.next.value, head1.next.next.next.next)
solu = Solution()
head2 = solu.swapPairs(head1)
print(head2.value, head2.next.value, head2.next.next.value, head2.next.next.next.value, head2.next.next.next.next)
