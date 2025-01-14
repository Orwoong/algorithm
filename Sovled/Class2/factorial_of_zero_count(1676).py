from math import factorial

N = int(input())

number = factorial(N)
str_number = str(number)
count = 0

for i in range(len(str_number)-1, -1, -1):
    if str_number[i] == '0':
        count += 1

    else:
        break

print(count)