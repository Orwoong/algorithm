import sys
from decimal import Decimal, ROUND_HALF_UP

N = int(input())
level_count = 30
dict = {}

for i in range(level_count):
    dict.update({i+1:0})

for _ in range(N):
    level = sys.stdin.readline()
    value = dict.get(int(level)) + 1
    dict[int(level)] = value

exception_count = Decimal(0.15 * N).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
low_exception_count = exception_count
high_exception_count = exception_count

for i in range(1, level_count + 1):
    value = dict.get(i)
    if low_exception_count > value:
        dict[i] = 0
        low_exception_count = low_exception_count - value
        if low_exception_count == 0:
            break
    else:
        dict[i] = value - low_exception_count
        break

for i in range(level_count, 1, -1):
    value = dict.get(i)
    if high_exception_count > value:
        dict[i] = 0
        high_exception_count = high_exception_count - value
        if high_exception_count == 0:
            break
    else:
        dict[i] = value - high_exception_count
        break

sum = 0
sum_count = 0
for i in range(1, level_count + 1):
    value = dict.get(i)
    if value > 0:
        sum_count += value
    sum += i * value

if sum_count == 0:
    print(0)
else:
    print(Decimal(sum/sum_count).quantize(Decimal('1'), rounding=ROUND_HALF_UP))


# 속도 개선 버전

N = int(input())
level_count = 30
level_list = [0] * 31

app_inputs = [int(sys.stdin.readline()) for _ in range(N)]

for level in app_inputs:
    level_list[level] += 1

exception_count = Decimal(0.15 * N).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
low_exception_count = exception_count
high_exception_count = exception_count

for i in range(1, level_count + 1):
    value = level_list[i]
    if low_exception_count > value:
        level_list[i] = 0
        low_exception_count = low_exception_count - value
        if low_exception_count == 0:
            break
    else:
        level_list[i] = value - low_exception_count
        break

for i in range(level_count, 1, -1):
    value = level_list[i]
    if high_exception_count > value:
        level_list[i] = 0
        high_exception_count = high_exception_count - value
        if high_exception_count == 0:
            break
    else:
        level_list[i] = value - high_exception_count
        break

sum = 0
sum_count = 0
for i in range(1, level_count + 1):
    value = level_list[i]
    if value > 0:
        sum_count += value
    sum += i * value

if sum_count == 0:
    print(0)
else:
    print(Decimal(sum/sum_count).quantize(Decimal('1'), rounding=ROUND_HALF_UP))