import sys

N, M = map(int, sys.stdin.readline().rstrip().split())

unknown_heard = {}
unknown_saw = {}

result = []

for i in range(0, N):
    value = sys.stdin.readline().rstrip()
    unknown_heard[value] = 1

for i in range(M):
    value = sys.stdin.readline().rstrip()
    heard = unknown_heard.get(value, -1)
    if heard == 1:
        result.append(value)

result = sorted(result)
print(len(result))
print("\n".join(result))