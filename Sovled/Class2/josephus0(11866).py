class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class CircleLinkedList:
    def __init__(self):
        self.head = None

    def append(self, val):
        if not self.head:
            self.head = ListNode(val, None)
            return

        node = self.head
        while node.next:
            node = node.next

        node.next = ListNode(val, None)

    def connect_last_node_to_header(self):
        node = self.head

        while node.next:
            node = node.next

        node.next = self.head

    def pop(self, jump_val):
        node = self.head
        pre_node = node

        for _ in range(jump_val - 1):
            pre_node = node
            node = node.next

        if not node.val:
            self.head = node
            return self.head.val
        else:
            self.head = node.next
            pre_node.next = self.head
            return node.val

def josephus(n, k):
    linked_list = CircleLinkedList()
    result = []

    for i in range(1, n+1):
        linked_list.append(i)

    linked_list.connect_last_node_to_header()

    for _ in range(n):
        result.append(linked_list.pop(k))

    return result

n, k = map(int, input().split())

result = josephus(n, k)
print("<" + ", ".join(map(str, result)) + ">")