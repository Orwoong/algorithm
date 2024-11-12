"""
입력값
3
1 0
5
4 2
1 2 3 4
6 0
1 1 9 1 1 1
"""

# 예를 들어 Queue에 4개의 문서(A B C D)가 있고, 중요도가 2 1 4 3 라면 C를 인쇄하고, 다음으로 D를 인쇄하고 A, B를 인쇄하게 된다.
import sys
from collections import deque

N = int(sys.stdin.readline())

for _ in range(N):
    doc_count, print_index = map(int, sys.stdin.readline().split())
    priority_list = list(map(int, sys.stdin.readline().split()))
    doc_list = deque(enumerate(priority_list))
    priority = dict(enumerate(priority_list))

    if doc_count == 1:
        print(1)
        continue

    while doc_list:
        max_key = max(priority, key=priority.get)
        max_value = priority[max_key]

        left = doc_list.popleft()
        if left[1] == max_value:
            priority.pop(max_key)
            if left[0] == print_index:
                print_order = doc_count-len(doc_list)
                print(print_order)
                break
        else:
            doc_list.append(left)


## 나의 정답

t = int(input())

for _ in range(t):
    n, m = map(int, input().split())
    data = list(map(int, input().split()))

    result = 1
    while data:
        if data[0] < max(data):
            data.append(data.pop(0))

        else:
            if m == 0: break

            data.pop(0)
            result += 1

        m = m - 1 if m > 0 else len(data) - 1

    print(result)

## 다른 풀이 정답
## 출처 : https://thisismi.tistory.com/entry/%EB%B0%B1%EC%A4%80-1966%EB%B2%88-%ED%94%84%EB%A6%B0%ED%84%B0-%ED%81%90-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EC%A0%95%EB%8B%B5-%EC%BD%94%EB%93%9C
