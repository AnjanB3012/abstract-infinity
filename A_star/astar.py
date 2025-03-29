import timeit
from absinf import AbsInf

def a_star_basic(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_list = [start]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: abs(goal[0] - start[0]) + abs(goal[1] - start[1])}

    def neighbors(node):
        r, c = node
        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                yield (nr, nc)

    while open_list:
        current = min(open_list, key=lambda x: f_score.get(x, float('inf')))
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        open_list.remove(current)

        for neighbor in neighbors(current):
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + abs(goal[0] - neighbor[0]) + abs(goal[1] - neighbor[1])
                if neighbor not in open_list:
                    open_list.append(neighbor)

    return []

def a_star_absinf(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_list = [start]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: abs(goal[0] - start[0]) + abs(goal[1] - start[1])}

    def neighbors(node):
        r, c = node
        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                yield (nr, nc)

    while open_list:
        current = min(open_list, key=lambda x: f_score.get(x, AbsInf()))
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        open_list.remove(current)

        for neighbor in neighbors(current):
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(neighbor, AbsInf()):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + abs(goal[0] - neighbor[0]) + abs(goal[1] - neighbor[1])
                if neighbor not in open_list:
                    open_list.append(neighbor)

    return []

# Define grids and start/goal points
grids = [
    ([  # Grid 1
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 0, 1, 0]
    ], (0, 0), (4, 4)),

    ([  # Grid 2
        [0, 1, 0],
        [0, 1, 0],
        [0, 0, 0]
    ], (0, 0), (2, 2)),

    ([  # Grid 3
        [0, 1],
        [1, 0]
    ], (0, 0), (1, 1))
]

for idx, (grid, start, goal) in enumerate(grids, 1):
    basic_time = timeit.timeit(lambda: a_star_basic(grid, start, goal), number=50000)
    absinf_time = timeit.timeit(lambda: a_star_absinf(grid, start, goal), number=50000)
    print(f"Grid {idx} - a_star_basic: {basic_time:.6f}s, a_star_absinf: {absinf_time:.6f}s")
