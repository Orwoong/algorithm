N = int(input())
info_list = []
result = [1] * N

for _ in range(N):
    x, y = map(int, input().split())
    info_list.append([x, y])

for i in range(N):
    for j in range(N):
        if info_list[i][0] < info_list[j][0] and info_list[i][1] < info_list[j][1]:
            result[i] += 1

print(*result)