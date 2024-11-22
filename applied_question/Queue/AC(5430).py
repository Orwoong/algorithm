import sys
from collections import deque

N = int(sys.stdin.readline())

for _ in range(N):
    string_list = list(sys.stdin.readline().rstrip())
    C = int(sys.stdin.readline())
    input_list = sys.stdin.readline().rstrip('\n')[1:-1].split(",")

    if input_list == ['']:
        input_list = deque()
    else:
        input_list = deque(input_list)

    reverse_count = 0
    flag = 0 # 만약에 입력값이 D와 빈 리스트가 들어올 경우 flag가 없을 경우에 error를 print후 빈 리스트를 출력 하게 됨
    for i in range(len(string_list)):
        if string_list[i] == 'R':
            reverse_count += 1
        else:
            if len(input_list) == 0:
                print("error")
                flag = 1
                break # error가 나올 경우 더이상 진행하지 않아도 되기 때문에 break 필요
            else:
                # 배열이 뒤집게 되면 index 0 <-> 리스트 마지막 index만 바뀌면 되기 때문에 나머지 연산자를 통해 reverse를 계속 하지 않아도 됨
                if reverse_count % 2 == 0:
                    input_list.popleft()
                else:
                    input_list.pop()
    if flag == 0:
        if reverse_count % 2 == 0:
            print('[' + ','.join(input_list) + ']')
        else:
            input_list.reverse()
            print('[' + ','.join(input_list) + ']')