# L	커서를 왼쪽으로 한 칸 옮김 (커서가 문장의 맨 앞이면 무시됨)
# D	커서를 오른쪽으로 한 칸 옮김 (커서가 문장의 맨 뒤이면 무시됨)
# B	커서 왼쪽에 있는 문자를 삭제함 (커서가 문장의 맨 앞이면 무시됨)
# 삭제로 인해 커서는 한 칸 왼쪽으로 이동한 것처럼 나타나지만, 실제로 커서의 오른쪽에 있던 문자는 그대로임
# P $	$라는 문자를 커서 왼쪽에 추가함

# 위에 주어진 방향을 토대로 커서를 통해서 문자를 끼워 넣음.

import sys

left = list(input())
right = []

for _ in range(int(input())):
    command = list(sys.stdin.readline().split())
    if command[0] == 'L' and left:
        right.append(left.pop())
    elif command[0] == 'D' and right:
        left.append(right.pop())
    elif command[0] == 'B' and left:
        left.pop()
    elif command[0] == 'P':
        left.append(command[1])

result = left + right[::-1]
print(''.join(result))

# 시간 초과 나는 풀이
# text = list(input())
# N = int(input())
# cursor = len(text)
#
# for i in range(int(input())):
#     command = sys.stdin.readline().split()
#     move = command[0]
#     if move == 'L' and cursor > 0:
#         cursor -= 1
#     elif move == 'D' and cursor < len(move):
#         cursor += 1
#     elif move == 'B' and 0 < cursor < len(move):
#         text.remove(cursor - 1)
#         cursor -= 1
#     elif move == 'P':
#         text.insert(cursor, command[1])
#         cursor += 1
#
# print(''.join(text))