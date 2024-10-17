# 정수를 저장하는 큐를 구현한 다음, 입력으로 주어지는 명령을 처리하는 프로그램을 작성하시오.
#
# 명령은 총 여섯 가지이다.
#
# push X: 정수 X를 큐에 넣는 연산이다.
# pop: 큐에서 가장 앞에 있는 정수를 빼고, 그 수를 출력한다. 만약 큐에 들어있는 정수가 없는 경우에는 -1을 출력한다.
# size: 큐에 들어있는 정수의 개수를 출력한다.
# empty: 큐가 비어있으면 1, 아니면 0을 출력한다.
# front: 큐의 가장 앞에 있는 정수를 출력한다. 만약 큐에 들어있는 정수가 없는 경우에는 -1을 출력한다.
# back: 큐의 가장 뒤에 있는 정수를 출력한다. 만약 큐에 들어있는 정수가 없는 경우에는 -1을 출력한다.

import sys
from collections import deque

input_count = int(sys.stdin.readline())

deq = deque()

def printQueue(input_count):
    for i in range(input_count):
        command, value = (sys.stdin.readline().split() + [None])[:2]
        result = None
        if command == 'push':
            deq.append(value)
        elif command == 'pop':
            result = deq.popleft() if deq else -1
        elif command == 'size':
            result = len(deq)
        elif command == 'empty':
            result = 0 if deq else 1
        elif command == 'front':
            result = deq[0] if deq else -1
        elif command == 'back':
            result = deq[-1] if deq else -1

        if result != None:
            print(result)

printQueue(input_count)