### 1차 제출 시간 초과로 실패 -> 원인 분석 필요
### 2차 제출 통과 -> input()과 readline()의 속도 차이가 있음
import sys

N = int(input())

stack = []
for _ in range(N):
    data = list(map(str, sys.stdin.readline().split()))
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

