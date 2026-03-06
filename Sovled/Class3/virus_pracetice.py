"""
백준 2606번 - 바이러스

핵심 아이디어:
1. 컴퓨터들을 "정점", 네트워크 연결을 "간선"으로 보는 그래프 문제다.
2. 1번 컴퓨터에서 시작해서, 연결된 모든 컴퓨터를 탐색하면 감염되는 컴퓨터 수를 알 수 있다.
3. 시작점(1번) 자체는 문제에서 제외하므로, "새로 방문한 컴퓨터 수"만 세면 된다.

아래 코드는 학습용으로 DFS와 BFS를 모두 구현했다.
실제 출력은 DFS 결과를 사용하며, BFS로 바꾸고 싶다면 main()의 한 줄만 바꾸면 된다.
"""

import sys
from collections import deque

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

        for neighbor in graph[node]:
            if visited[neighbor]:
                continue

            visited[neighbor] = True
            count += 1
            dfs(neighbor)

    dfs(start)
    return count

computers = sys.stdin.readline().rstrip()
edges = sys.stdin.readline().rstrip()

graph = build_graph_practice(num_computers=computers, num_edges=edges)
print(count_infected_by_dfs_practice(graph))

def build_graph(num_computers: int, num_edges: int) -> list[list[int]]:
    """
    입력으로 주어진 연결 정보를 바탕으로 인접 리스트 그래프를 만든다.

    예:
    컴퓨터가 7대면 인덱스를 1~7까지 쓰기 위해 길이 8짜리 리스트를 만든다.
    graph[1]에는 1번과 직접 연결된 컴퓨터 목록이 들어간다.
    """
    # 0번 인덱스는 사용하지 않고, 1번부터 num_computers번까지 사용한다.
    graph = [[] for _ in range(num_computers + 1)]

    # 간선(연결) 정보를 num_edges줄 읽는다.
    for _ in range(num_edges):
        a, b = map(int, input().split())

        # 양방향 연결:
        # a와 b가 연결되면 a에서도 b로 갈 수 있고, b에서도 a로 갈 수 있다.
        graph[a].append(b)
        graph[b].append(a)

    # 탐색 순서를 일정하게 맞추기 위해 정렬한다.
    # 정렬은 정답 필수 조건은 아니지만, 디버깅/학습 시 흐름을 보기 쉬워진다.
    for node in range(1, num_computers + 1):
        graph[node].sort()

    return graph


def count_infected_by_dfs(graph: list[list[int]], start: int = 1) -> int:
    """
    DFS(깊이 우선 탐색)로 start에서 도달 가능한 컴퓨터 수를 센다.
    단, start 본인은 감염 수에서 제외한다.
    """
    visited = [False] * len(graph)
    infected_count = 0  # 1번을 제외한 실제 감염 컴퓨터 수

    def dfs(node: int) -> None:
        nonlocal infected_count

        # 1) 현재 노드 방문 처리
        visited[node] = True

        # 2) 현재 노드와 인접한 모든 노드를 확인
        for neighbor in graph[node]:
            # 이미 방문했다면 다시 가지 않는다.
            if visited[neighbor]:
                continue

            # 아직 방문하지 않은 컴퓨터를 "처음 발견"한 순간 감염 수 +1
            infected_count += 1

            # 더 깊은 연결로 재귀 호출
            dfs(neighbor)

    # DFS 시작
    dfs(start)
    return infected_count


def count_infected_by_bfs(graph: list[list[int]], start: int = 1) -> int:
    """
    BFS(너비 우선 탐색)로 start에서 도달 가능한 컴퓨터 수를 센다.
    단, start 본인은 감염 수에서 제외한다.
    """
    visited = [False] * len(graph)
    queue = deque([start])  # 시작점을 큐에 넣고 시작
    visited[start] = True
    infected_count = 0

    # 큐가 빌 때까지 반복
    while queue:
        current = queue.popleft()

        # current와 연결된 이웃들을 확인
        for neighbor in graph[current]:
            if visited[neighbor]:
                continue

            # 처음 방문하는 순간 감염 처리
            visited[neighbor] = True
            infected_count += 1
            queue.append(neighbor)

    return infected_count


def main() -> None:
    # 입력 형식:
    # 1줄: 컴퓨터 수 N
    # 2줄: 연결 수 M
    # 3줄~: 연결 정보 M줄
    num_computers = int(input().strip())
    num_edges = int(input().strip())

    graph = build_graph(num_computers, num_edges)

    # 최종 출력: 1번 컴퓨터로 인해 감염되는 컴퓨터 수
    answer = count_infected_by_dfs(graph, start=1)
    # answer = count_infected_by_bfs(graph, start=1)  # BFS 버전 사용 시 이 줄로 교체
    print(answer)


if __name__ == "__main__":
    main()
