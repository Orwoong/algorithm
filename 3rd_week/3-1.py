###
import collections
import sys
from collections import deque

s = sys.stdin.readlines()
maze = [list(map(int,list(i.strip()))) for i in s]

def bfs_maze(maze):
    rows = len(maze)
    cols = len(maze[0])
    visited = {(0, 0)}

    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    queue = deque()
    queue.append((0, 0))

    while queue:
        x, y = queue.popleft()

        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]

            if nx < 0 or ny < 0 or nx >= rows or ny >= cols or maze[nx][ny] == 0 or (nx, ny) in visited:
                continue

            if maze[nx][ny] == 1:
                maze[nx][ny] = maze[x][y] + 1
                queue.append((nx, ny))
                visited.add((nx, ny))

    return maze[rows-1][cols-1]

print(bfs_maze(maze))