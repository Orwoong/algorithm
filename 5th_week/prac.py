import heapq


def dijkstra(graph, start):
    N = len(graph)
    INF = 1e9
    dist = [INF] * N

    q = []
    # 튜플일 경우 0번째 요소 기준으로 최소 힙 구조.
    # 첫 번째 방문 누적 비용은 0이다.
    heapq.heappush(q, (0, start))
    dist[start] = 0

    while q:
        # 누적 비용이 가장 작은 녀석을 꺼낸다.
        acc, node = heapq.heappop(q)

        # 이미 답이 될 가망이 없다.
        if dist[node] < acc:
            continue

        # 인접 노드를 차례대로 살펴보며 거리를 업데이트한다.
        for adj, d in graph[node]:
            cost = acc + d
            if cost < dist[adj]:
                dist[adj] = cost
                heapq.heappush(q, (cost, adj))

    return dist

def delay_time(list, node_count, start_node):
    graph = {}

    for start, end, time in list:
        if start not in graph:
            graph[start] = []
        graph[start].append((end, time))

    q = [(0, start_node)]
    result = {}

    while q:
        acc, cur = heapq.heappop(q)
        if cur not in result:
            result[cur] = acc
            if cur in graph:
                for adj, time in graph[cur]:
                    heapq.heappush(q, (acc + time, adj))
    if len(result) == node_count:
        return max(result.values())

    return -1