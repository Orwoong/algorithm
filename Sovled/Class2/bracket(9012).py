N = int(input())

for _ in range(N):
    s = input().strip()
    stack = 0
    print_flag = True

    for char in s:
        if char == '(':
            stack += 1
        else:
            if stack == 0:
                print_flag = False
            else:
                stack -= 1

    if stack != 0:
        print_flag = False

    print("YES" if print_flag else "NO")