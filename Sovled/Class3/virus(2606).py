import sys

def build_graph_practice(num_computers: int, num_edges: int) -> list[list[int]]:
    graph = [[] for _ in range(num_computers + 1)]

    for _ in range(num_edges):
        a, b = map(int, sys.stdin.readline().rstrip().split())

        graph[a].append(b)
        graph[b].append(a)

    for node in range(1, num_computers + 1):
        graph[node].sort()

    return graph

def count_infected_by_dfs_practice(graph: list[list[int]], start: int = 1) -> int:
    visited = [False] * len(graph)
    count = 0

    def dfs(node: int) -> None:
        nonlocal count

        visited[node] = True

        for neighbor in graph[node]:
            if visited[neighbor]:
                continue

            count += 1
            dfs(neighbor)

    dfs(start)
    return count

computers = int(sys.stdin.readline().rstrip())
edges = int(sys.stdin.readline().rstrip())

graph = build_graph_practice(num_computers=computers, num_edges=edges)
print(count_infected_by_dfs_practice(graph))