import sys

N, M = map(int, sys.stdin.readline().rstrip().split())

search_pokemon = {}
search_index = {}
for i in range(1, N+1):
    value = sys.stdin.readline().rstrip()
    search_pokemon[value] = i
    search_index[str(i)] = value

for i in range(M):
    value = sys.stdin.readline().rstrip()
    if value in search_pokemon:
        print(search_pokemon[value])

    if value in search_index:
        print(search_index[value])
