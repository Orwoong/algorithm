# 표기식은 알파벳 대문자와 +, -, *, /, (, )

"""
')', '*', '/' 에 따라서 표기식 구분
'*', '/' 뒤에 '(' 표시가 있는지 판단 해야 함.
만약에 '*', '/' 뒤에 '('가 없는 경우에는 쌓아놓은 리스트의 값들을 가지고 조합
"""

from string import ascii_uppercase

DATA = list(input())

alphabet_list = list(ascii_uppercase)
p = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '(': 3
}
stack = []
result = ''

for char in DATA:
    if char.isalpha():
        result += char
        continue

    if not stack:
        stack.append(char)
        continue

    if char == ')':
        while stack and stack[-1] != '(':
            result += stack.pop()
        stack.pop()
        continue

    if char == '(' or p[char] > p[stack[-1]] :
        stack.append(char)
    elif p[char] == p[stack[-1]]:
        result += stack.pop()
        stack.append(char)
    else:
        while stack and stack[-1] != '(':
            result += stack.pop()
        stack.append(char)

while(stack):
    result += stack.pop()

print(result)

"""
반례 모음
# 입력: G*(A-B*(C/D+E)/F) # 내답: GABCD/E+/F*-* # 정답: GABCD/E+*F/-*
"""


# alphabet_list = list(ascii_uppercase)
# bracket_list = ['(', ')']
# operator_list = deque()
# operand_list = deque()
# result = ''
#
# while DATA:
#     char = DATA.popleft()
#
#     if char in alphabet_list:
#         operand_list.append(char)
#     elif char not in bracket_list:
#         operator_list.append(char)
#
#     if char == ')' or not DATA:
#         while operand_list:
#             result += operand_list.popleft()
#         while operator_list:
#             result += operator_list.pop()
#     if (char == '*' or char == '/') and DATA[0] in alphabet_list:
#         operand_list.append(DATA.popleft())
#         if DATA and (DATA[0] == '*' or DATA[0] == '/'):
#             while operand_list:
#                 result += operand_list.popleft()
#             result += operator_list.pop()
#             continue
#
#         while operand_list:
#             result += operand_list.popleft()
#         while operator_list:
#             result += operator_list.pop()
#
# print(result)

# A/B+C*D*E
# AB/CD*E*+
