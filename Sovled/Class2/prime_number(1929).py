import math

number_list = list(map(int, input().split()))
result_list = []

def is_prime(number):
    if number > 1:
        for j in range(2, int(math.sqrt(number)) + 1):
            if number % j == 0:
                return False
        return True

for i in range(number_list[0], number_list[1] + 1):
    if is_prime(i):
        result_list.append(i)


print("\n".join(map(str, result_list)))