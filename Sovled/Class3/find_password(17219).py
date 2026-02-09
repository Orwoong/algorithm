import sys

N, M = map(int, sys.stdin.readline().split())

info = {}

for _ in range(N):
    web_site, password = map(str, sys.stdin.readline().rstrip().split())
    info[web_site] = password

for _ in range(M):
    web_site = sys.stdin.readline().rstrip()
    password = info.get(web_site, None)
    if password:
        print(password)