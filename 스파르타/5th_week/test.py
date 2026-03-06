import sys
from prac import dijkstra, delay_time

with open('dijkstra_testcase.txt') as f:
    sys.stdin = f
    input = sys.stdin.readline
    n, m = map(int, input().split())
    start = int(input())
    graph = [[] for _ in range(n + 1)]

    for _ in range(m):
        a, b, c = map(int, input().split())
        graph[a].append((b, c))

assert dijkstra(graph, start) == [1000000000, 0, 8, 9, 5, 7]


assert delay_time([[2,1,1],[2,3,1],[3,4,1]], 4, 2) == 2
assert delay_time([[1,2,1]], 2, 1) == 1
assert delay_time([[1,2,1]], 2, 2) == -1
