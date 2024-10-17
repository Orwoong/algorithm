import sys
import heapq

input = sys.stdin.readline
city_count = int(input())
way_count = int(input())

graph = [[] for _ in range(city_count + 1)]

for _ in range(way_count):
    start, end, cost = map(int, input().split())
    graph[start].append((end, cost))

starting, destination = map(int, input().split())

def destinationLeastCost(graph, starting, destination):
    INF = 1e9
    distance = [INF] * len(graph)

    q = []

    heapq.heappush(q, (0, starting))
    distance[starting] = 0

    while q:
        cost, end = heapq.heappop(q)

        if distance[end] < cost:
            continue

        for graph_end_node, graph_cost in graph[end]:
            cost_sum = graph_cost + cost
            if cost_sum < distance[graph_end_node]:
                distance[graph_end_node] = cost_sum
                heapq.heappush(q, (cost_sum, graph_end_node))

    return distance[destination]

print(destinationLeastCost(graph, starting, destination))