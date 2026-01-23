N = int(input())

stack = []
for _ in range(N):
    data = list(map(str, input().split()))
    if len(data) > 1:
        value = data.pop()
        stack.append(value)
    else:
        value = data.pop()
        if value == "pop":
            if stack:
                print(stack.pop())
            else:
                print(-1)
        elif value == "size":
            print(len(stack))
        elif value == "empty":
            print(0 if stack else 1)
        elif value == "top":
            if stack:
                print(stack[len(stack) - 1])
            else:
                print(-1)

