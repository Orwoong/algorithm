import sys
from collections import deque

N = int(input())
dequeue = deque()
result = []

for _ in range(N):
    data = list(map(str, sys.stdin.readline().split()))
    if len(data) > 1:
        value = data.pop()
        dequeue.append(value)
    else:
        value = data.pop()
        if value == "pop":
            if dequeue:
                result.append(dequeue.popleft())
            else:
                result.append(-1)
        elif value == "size":
            result.append(len(dequeue))
        elif value == "empty":
            result.append(0 if dequeue else 1)
        elif value == "front":
            if dequeue:
                result.append(dequeue[0])
            else:
                result.append(-1)
        else:
            if dequeue:
                result.append(dequeue[len(dequeue) - 1])
            else:
                result.append(-1)

print("\n".join(map(str, result)))