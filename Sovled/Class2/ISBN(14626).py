## ISBN은 다음과 같은 패턴이 있다
## 13자리의 숫자로 되어 있으며 12자리까지 홀수 자리수는 1을 곱하고 짝수 자리수는 3을 곱한다
## 마지막 자리수인 13자리의 숫자는 각각 자리수를 곱한 것을 가지고 10으로 나눈 나머지가 된다.

N = input()

sum = 0
damage_index = -1

for i in range(0, len(N)-1):
    if N[i] == '*':
        damage_index = i
    elif i % 2 == 0:
        sum += int(N[i])
    else:
        sum += int(N[i])*3

if damage_index % 2 == 0:
    multiplier = 1
else:
    multiplier = 3

last = int(N[-1])

for i in range(0, 10):
    result = (10 - ((sum + (i * multiplier)) % 10)) % 10
    if result == last:
        print(i)
        break