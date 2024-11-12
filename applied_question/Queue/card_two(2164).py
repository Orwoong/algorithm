from collections import deque

N = int(input())
deq = deque(range(1, N+1))

while len(deq) > 1:
    deq.popleft()
    deq.append(deq.popleft())

print(deq.popleft())