import heapq

heap = []
heapq.heappush(heap, (8, 1))
heapq.heappush(heap, (50, 2))
heapq.heappush(heap, (10, 1))


print(heap)
print(heap.pop(0))

