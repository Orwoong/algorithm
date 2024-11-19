import sys
import heapq

N = int(sys.stdin.readline())

for i in range(N):
    K = int(sys.stdin.readline())
    visted = [True] * K
    min_heap = []
    max_heap = []

    for i in range(K):
        in_out, number = sys.stdin.readline().split()
        number = int(number)

        if in_out == 'I':
            heapq.heappush(min_heap, (number,i))
            heapq.heappush(max_heap, (-number, i))
        else:
            if number == -1 and min_heap:
                visted[heapq.heappop(min_heap)[1]] = False
            elif number == 1 and max_heap:
                visted[heapq.heappop(max_heap)[1]] = False

        while min_heap and visted[min_heap[0][1]] == False:
            heapq.heappop(min_heap)
        while max_heap and visted[max_heap[0][1]] == False:
            heapq.heappop(max_heap)

    if min_heap == [] and max_heap == []:
        print("EMPTY")
    else:
        print(-heapq.heappop(max_heap)[0], heapq.heappop(min_heap)[0])

# N = int(sys.stdin.readline())
# deq = deque()
#
# for i in range(N):
#     K = int(sys.stdin.readline())
#
#     for i in range(K):
#         in_out, number = sys.stdin.readline().split()
#         number = int(number)
#
#         if not deq and in_out == 'I':
#             deq.append(number)
#             continue
#
#
#         if in_out == 'I':
#             if deq[-1] < number:
#                 deq.append(number)
#             elif deq[0] > number:
#                 deq.appendleft(number)
#             elif deq[-1] > number and deq[0] < number:
#                 max = deq.pop()
#                 deq.append(number)
#                 deq.append(max)
#             else:
#                 min = deq.popleft()
#                 deq.appendleft(number)
#                 deq.append(min)
#         else:
#             if not deq:
#                 continue
#             if number == 1:
#                 deq.pop()
#             else:
#                 deq.popleft()
#
#     if not deq:
#         print("EMPTY")
#     else:
#         print(deq.pop(), deq.popleft())