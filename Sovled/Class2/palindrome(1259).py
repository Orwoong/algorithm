while True:
    s = input()
    if s == '0':
        break

    is_palindrome = s == s[::-1]
    print("yes" if is_palindrome else "no")
