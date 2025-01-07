# 이항 계수에 대해서 잘 몰랐기 때문에 관련 정보를 검색한 후 기억하기 위해 남겨둠
# 참고 사이트 - https://velog.io/@newdana01/알고리즘-이항계수란-알고리즘-구현
import math

N, K = map(int, input().split())
def bino_coef_factorial(n, k):
	return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))

print(bino_coef_factorial(N, K))