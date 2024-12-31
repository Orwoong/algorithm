## 소수란 - 2보다 큰 자연수 중에서 1과 자기 자신을 제외한 자연수로는 떨어지지 않는 자연수
## 소수를 판별하는 방법 - 주어진 수가 x일 경우 제곱근은 x의 루트인데 x를 2부터 x의 제곱근까지 나누어서 나머지가 0이 안나온다면 소수
## 예를 들어 10의 제곱근은 3인데 2부터 3까지 10을 나눌 경우 2로 나눌 경우 나머지가 0이 되므로 소수가 아님
## 13도 제곱근이 3인데 2와 3으로 나눌 수 없어서 소수

import math

N = input()
number_list = list(map(int, input().split()))
count = 0

def is_prime(number):
    if number > 1:
        for j in range(2, int(math.sqrt(number)) + 1):
            if number % j == 0:
                return False
        return True

for i in range(int(N)):
    number = number_list[i]
    if is_prime(number_list[i]):
        count += 1

print(count)


## 에라토스테네스의 체
# import math
#
# n = 1000 # 2부터 1000까지의 모든 수에 대하여 소수 판별
# array = [True for i in range(n + 1)] # 처음엔 모든 수가 소수(True)인 것으로 초기화(0과 1은 제와)
#
# # 에라토스테네스의 체 알고리즘
# for i in range(2, int(math.sqrt(n)) + 1): # 2부터 n의 제곱근까지의 모든 수를 확인하며
#     if array[i] == True: # i가 소수인 경우(남은 수인 경우)
#         # i를 제외한 i의 모든 배수를 지우기
#         j = 2
#         while i * j <= n:
#             array[i * j] = False
#             j += 1
#
# # 모든 소수 출력
# for i in range(2, n + 1):
#     if array[i]:
#         print(i, end=" ")
