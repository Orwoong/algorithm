import sys

N = int(sys.stdin.readline())
number_list = [0] * 2000001

for _ in range(N):
    number = int(sys.stdin.readline())
    number_list[number + 1000000] = 1

for i in range(2000001):
    if number_list[i] != 0:
        print(i - 1000000)