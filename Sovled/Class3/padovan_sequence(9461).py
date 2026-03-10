N = int(input())

dp = [0] * 102

dp[1] = 1
dp[2] = 1
dp[3] = 1

for i in range(4, 102):
    dp[i] = dp[i-2] + dp[i-3]

for i in range(0, N):
    value = int(input())
    print(dp[value])