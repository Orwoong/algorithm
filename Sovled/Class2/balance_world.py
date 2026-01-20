from collections import deque

while True:
    string = input()

    if string == ".":
        break

    brackets = deque()
    is_balanced = True

    for char in string:
        if char == '[' or char == '(':
            brackets.append(char)
        elif char == ']':
            if not brackets:
                is_balanced = False
                break
            bracket = brackets.pop()
            if bracket != '[':
                is_balanced = False
                break
        elif char == ')':
            if not brackets:
                is_balanced = False
                break
            bracket = brackets.pop()
            if bracket != '(':
                is_balanced = False
                break

    if not brackets and is_balanced:
        print("yes")
    else:
        print("no")

