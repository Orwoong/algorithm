import sys

N = int(sys.stdin.readline())
result = set()

for _ in range(N):
    parts = sys.stdin.readline().split()

    if len(parts) > 1:
        order, value = parts[0], int(parts[1])
        if order == "add":
            result.add(value)
        elif order == "remove":
            result.discard(value)
        elif order == "check":
            print(1 if value in result else 0)
        elif order == "toggle":
            if value in result:
                result.discard(value)
            else:
                result.add(value)
    else:
        if parts[0] == "all":
            result = set([i for i in range(1, 21)])
        else:
            result = set()