# 시간 제한은 1초이며 수열의 크기는 10만까지 되어 있어서 리스트에 있는 수들의 비교를 빠르게 하는게 관건 일듯

import sys

N = int(sys.stdin.readline())
number_list = list(map(int, sys.stdin.readline().split()))
result = [-1] * N
stack = [0]

for i in range(1, N):
    while stack and number_list[stack[-1]] < number_list[i]:
        result[stack.pop()] = number_list[i]
    stack.append(i)

print(*result)

N = sys.stdin.readline()
list = sys.stdin.readline().split()

for i in range(len(list)):
    max_number = -1
    for j in range(i + 1, len(list)):
        pivot_number = list[i]
        if pivot_number < list[j]:
            max_number = list[j]
            break
    print(max_number, end = ' ')