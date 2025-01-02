## 나의 풀이
## 시간 120ms(평균)
from string import ascii_lowercase

N = int(input())
S = input()
R = 31
MOD = 1234567891

a_list = list(ascii_lowercase)
a_hash = {a_list[i] : i+1 for i in range(0, len(a_list))}

result = 0

for i in range(N):
    result += a_hash.get(S[i]) * (R ** i)

print(result % 1234567891)

## 아스키 코드를 이용한 풀이
## 시간 40ms(평균)

N = int(input())
S = input()
R = 31
MOD = 1234567891
result = 0

for i in range(N):
    result += (ord(S[i]) - 96) * (R ** i)

print(result % 1234567891)