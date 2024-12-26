while True:
    a, b, c = map(int, input().split())
    if a == 0 and b == 0 and c == 0:
        break
    a_square_in_two = a * a
    b_square_in_two = b * b
    c_square_in_two = c * c
    if a_square_in_two + b_square_in_two == c_square_in_two:
        print("right")
    elif a_square_in_two + c_square_in_two == b_square_in_two:
        print("right")
    elif c_square_in_two + b_square_in_two == a_square_in_two:
        print("right")
    else:
        print("wrong")