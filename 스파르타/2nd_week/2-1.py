def cal_postfix(text):
    number_list = []
    sum = 0

    for char in text:
        if char.isnumeric():
            number_list.insert(0, int(char))
        else :
            if len(number_list) > 1:
                first = number_list.pop()
                last = number_list.pop()
            else:
                first = sum
                last = number_list.pop()

            if char == '+':
                sum = first + last
            elif char == '-':
                sum = first - last
            elif char == '*':
                sum = first * last
            else:
                sum = first // last

    return sum


assert cal_postfix("23+5*") == 25
assert cal_postfix("42/3-2*") == -2
assert cal_postfix("25*3/") == 3
