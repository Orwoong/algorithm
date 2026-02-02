import sys
from collections import deque

N = int(input())
app_inputs = deque(int(sys.stdin.readline()) for _ in range(N))
stack_count = 0
stack = []
result = []

while app_inputs:
    input_first = app_inputs[0]
    stack_last = 0
    if stack:
        stack_last = stack[-1]

    if input_first > stack_last:
        stack_count += 1
        stack.append(stack_count)
        result.append("+")
    elif input_first == stack_last:
        stack.pop()
        app_inputs.popleft()
        result.append("-")
    else:
        break

if not app_inputs:
    print("\n".join(result))
else:
    print("NO")