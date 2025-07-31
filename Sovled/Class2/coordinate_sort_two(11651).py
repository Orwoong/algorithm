N = int(input())
list = [[] for _ in range(200001)]

for i in range(N):
    x, y = map(int, input().split())
    list[y + 100000].append(x)

for i in range(len(list)):
    if list[i]:
        list[i] = sorted(list[i])
        for j in range(len(list[i])):
            print(list[i][j], i - 100000)