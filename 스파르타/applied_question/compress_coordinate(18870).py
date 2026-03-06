import sys

N = int(sys.stdin.readline())
coords = list(map(int, sys.stdin.readline().split()))

sorted_coords = sorted(set(coords))

dic = {sorted_coords[i] : i for i in range(len(sorted_coords))}

for coord in coords:
    print(dic[coord], end=' ')