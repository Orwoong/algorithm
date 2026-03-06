import sys

N = int(sys.stdin.readline())
range_list = {int(x): True for x in sys.stdin.readline().split()}

M = int(sys.stdin.readline())
check_number_list = list(map(int, sys.stdin.readline().split()))

for check_number in check_number_list:
    try:
        if range_list[check_number]:
            print(1)
    except KeyError:
        print(0)
