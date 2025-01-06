N = input()

for _ in range(int(N)):
    floor = int(input())
    room = int(input())

    floors = [[0] * room for _ in range(floor + 1)]

    for i in range(0, room):
        floors[0][i] = i + 1

    for j in range(1, floor + 1):
        for k in range(room):
            floors[j][k] = sum(floors[j-1][:k+1])

    print(floors[floor][room-1])
