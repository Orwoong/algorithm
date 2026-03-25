
N = int(input())

dp = [0] * (N+1)

if N < 2:
    print(N)
else:
    dp[1] = 1
    dp[2] = 3
    for i in range(3, N + 1):
        dp[i] = dp[i-1] + 2 * dp[i-2]
    print(dp[N] % 10007)

