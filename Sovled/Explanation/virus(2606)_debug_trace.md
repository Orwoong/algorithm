# 백준 2606 (바이러스) 디버깅 흐름 문서

이 문서는 [`virus(2606).py`](./virus(2606).py) 코드가 실제로 어떻게 흘러가는지,  
디버깅하듯이 변수 변화와 함수 호출 순서를 따라가며 설명합니다.

---

## 1) 문제를 그래프로 바꾸기

- 컴퓨터 번호: 정점(Vertex)
- 네트워크 연결: 간선(Edge)
- 목표: `1번 컴퓨터`에서 시작해서 방문 가능한 컴퓨터 개수 세기
- 단, `1번 본인`은 제외

---

## 2) 예시 입력으로 추적

백준 예시 입력:

```text
7
6
1 2
2 3
1 5
5 2
5 6
4 7
```

- `num_computers = 7`
- `num_edges = 6`

### 2-1) 그래프(build_graph) 생성 과정

초기 상태(`graph = [[] for _ in range(8)]`):

- `graph[0] = []` (사용 안 함)
- `graph[1] = []`
- `graph[2] = []`
- `graph[3] = []`
- `graph[4] = []`
- `graph[5] = []`
- `graph[6] = []`
- `graph[7] = []`

간선을 한 줄씩 읽어서 양방향으로 추가:

1. 입력 `1 2`
   - `graph[1].append(2)`
   - `graph[2].append(1)`
2. 입력 `2 3`
   - `graph[2].append(3)`
   - `graph[3].append(2)`
3. 입력 `1 5`
   - `graph[1].append(5)`
   - `graph[5].append(1)`
4. 입력 `5 2`
   - `graph[5].append(2)`
   - `graph[2].append(5)`
5. 입력 `5 6`
   - `graph[5].append(6)`
   - `graph[6].append(5)`
6. 입력 `4 7`
   - `graph[4].append(7)`
   - `graph[7].append(4)`

정렬 후 최종 인접 리스트:

- `graph[1] = [2, 5]`
- `graph[2] = [1, 3, 5]`
- `graph[3] = [2]`
- `graph[4] = [7]`
- `graph[5] = [1, 2, 6]`
- `graph[6] = [5]`
- `graph[7] = [4]`

핵심 관찰:
- `1`에서 시작하면 `2, 3, 5, 6`으로 갈 수 있음
- `4, 7`은 다른 컴포넌트라서 못 감

---

## 3) DFS 실행 흐름 (재귀 호출 스택 중심)

초기값:

- `visited = [False, False, False, False, False, False, False, False]`
- `infected_count = 0`
- 호출: `dfs(1)`

아래는 중요한 순간만 압축한 흐름입니다.

| 단계 | 현재 함수 | 주요 동작 | infected_count | visited에서 True인 노드 |
|---|---|---|---:|---|
| 1 | `dfs(1)` 진입 | `visited[1] = True` | 0 | {1} |
| 2 | `dfs(1)` 내부 for | 이웃 `2` 발견(미방문) -> `infected_count += 1`, `dfs(2)` 호출 | 1 | {1} |
| 3 | `dfs(2)` 진입 | `visited[2] = True` | 1 | {1,2} |
| 4 | `dfs(2)` 내부 for | 이웃 `1`은 방문됨 -> `continue` | 1 | {1,2} |
| 5 | `dfs(2)` 내부 for | 이웃 `3` 발견(미방문) -> +1 후 `dfs(3)` | 2 | {1,2} |
| 6 | `dfs(3)` 진입 | `visited[3] = True`, 이웃 `2`는 방문됨 -> 종료/복귀 | 2 | {1,2,3} |
| 7 | `dfs(2)` 내부 for | 다음 이웃 `5` 발견(미방문) -> +1 후 `dfs(5)` | 3 | {1,2,3} |
| 8 | `dfs(5)` 진입 | `visited[5] = True`, 이웃 `1`,`2`는 방문됨 | 3 | {1,2,3,5} |
| 9 | `dfs(5)` 내부 for | 이웃 `6` 발견(미방문) -> +1 후 `dfs(6)` | 4 | {1,2,3,5} |
| 10 | `dfs(6)` 진입 | `visited[6] = True`, 이웃 `5` 방문됨 -> 종료/복귀 | 4 | {1,2,3,5,6} |
| 11 | 복귀 완료 | 더 이상 미방문 이웃 없음 -> 전체 DFS 종료 | 4 | {1,2,3,5,6} |

최종 출력:

```text
4
```

---

## 4) for문이 실제로 하는 일 (DFS 기준)

`for neighbor in graph[node]:`

- 현재 노드와 직접 연결된 컴퓨터를 하나씩 꺼낸다.
- 각 이웃에 대해 아래 순서로 검사한다.
  1. `if visited[neighbor]: continue`
     - 이미 방문한 컴퓨터면 무시
  2. 처음 방문이라면:
     - `infected_count += 1`
     - `dfs(neighbor)` 재귀 호출

즉, for문은 "연결된 후보들을 순회"하고, 재귀는 "그 후보의 하위 연결까지 깊게 탐색"한다.

---

## 5) 재귀 함수 호출/복귀 감각 잡기

`dfs(1)` -> `dfs(2)` -> `dfs(3)`처럼 들어갔다가,  
`dfs(3)`에서 더 갈 곳이 없으면 `dfs(2)`로 복귀한다.

그 다음 `dfs(2)`의 for문이 "중단된 다음 이웃"부터 다시 돈다.  
그래서 `3` 탐색을 끝낸 뒤 `5`를 이어서 처리할 수 있다.

이 과정을 콜스택 느낌으로 쓰면:

1. push `dfs(1)`
2. push `dfs(2)`
3. push `dfs(3)`
4. pop `dfs(3)` (끝)
5. push `dfs(5)`
6. push `dfs(6)`
7. pop `dfs(6)` -> pop `dfs(5)` -> pop `dfs(2)` -> pop `dfs(1)`

---

## 6) BFS로 보면 어떻게 다른가

같은 그래프를 BFS로 탐색하면 큐 변화는 대략 아래처럼 된다.

초기:
- `queue = [1]`, `visited[1] = True`, `infected_count = 0`

흐름:
1. `1` 꺼냄 -> `2,5` 방문 처리 + 큐 삽입 -> `queue=[2,5]`, count=2
2. `2` 꺼냄 -> `3` 새 방문 -> `queue=[5,3]`, count=3
3. `5` 꺼냄 -> `6` 새 방문 -> `queue=[3,6]`, count=4
4. `3` 꺼냄 -> 새 이웃 없음
5. `6` 꺼냄 -> 새 이웃 없음
6. 큐 비어서 종료

결과는 DFS와 동일하게 `4`.

---

## 7) 직접 디버깅 연습 방법

1. `print(node, visited, infected_count)`를 DFS 내부에 잠깐 넣는다.
2. BFS라면 while 루프 안에서 `print(current, list(queue), infected_count)`를 찍는다.
3. 출력이 많으면 작은 입력(노드 4~6개)으로 먼저 검증한다.

이렇게 하면 for문 순회와 재귀/큐 흐름이 눈에 보이기 시작한다.
