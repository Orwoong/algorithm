import sys
N = int(input())
count = [0] * 10001

for i in range(N):
    number = int(sys.stdin.readline())
    count[number] += 1

for i in range(10001):
    if count[i] > 0:
        for _ in range(count[i]):
            print(i)

# 메모리 초과
# 플랫 하는 과정에서 메모리가 기하급수적으로 늘어남
# N이 10만인 경우 89095160Byte -> 89 MegaByte

# import sys
# from itertools import chain
#
# N = int(input())
#
# number_list = [[] for _ in range(10001)]
#
# for i in range(N):
#     number = int(sys.stdin.readline())
#     number_list[number].append(number)
#
# number_list = list(chain.from_iterable(number_list))
#
# print(*number_list, sep="\n")