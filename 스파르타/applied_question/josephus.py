## [7,3이 주어진다면]
## [1,2,3,4,5,6,7]에서 세번째를 제거 해야 하므로 3이 먼저 제거 되고 4가 첫번째가 되므로 세번째는 4,5,6의 순서로 인하여 6이 제거 되어야 함
## 링크드 리스트를 사용해보자 -> 마지막 노드가 헤드를 가르키게 하여 순환 구조로 만들어 보자

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

        if node.val is None:
            self.head = self.head.next
            return self.head.val
        else:
            self.head = node.next
            pre_node.next = self.head
            return node.val

def josephus(n, k):
    linked_list = CircleLinkedList()
    result = []

    for i in range(1, n + 1):
        linked_list.append(i)

    linked_list.connect_last_node_to_header()

    for _ in range(0, n):
        result.append(linked_list.pop(k))

    return result

n, k = map(int, input().split())


print(josephus(n, k))
