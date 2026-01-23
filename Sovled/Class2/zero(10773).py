from functools import reduce

N = int(input())
stack = []

def sum(a, b):
    return a + b

for _ in range(N):
    number = int(input())
    if number == 0:
        stack.pop()
    else:
        stack.append(number)


print(reduce(sum, stack, 0))