import timeit
from absinf import AbsInf
import random

# A* Algorithms
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
            return True
        open_list.remove(current)
        for neighbor in neighbors(current):
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + abs(goal[0] - neighbor[0]) + abs(goal[1] - neighbor[1])
                if neighbor not in open_list:
                    open_list.append(neighbor)
    return False

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
            return True
        open_list.remove(current)
        for neighbor in neighbors(current):
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(neighbor, AbsInf()):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + abs(goal[0] - neighbor[0]) + abs(goal[1] - neighbor[1])
                if neighbor not in open_list:
                    open_list.append(neighbor)
    return False

# Grid Generator Functions
def generate_empty_grid(size):
    grid = [[0]*size for _ in range(size)]
    return grid, (0, 0), (size-1, size-1)

def generate_maze_grid(size):
    grid = [[0 if (i+j)%3 != 0 else 1 for j in range(size)] for i in range(size)]
    grid[0][0], grid[size-1][size-1] = 0, 0
    return grid, (0, 0), (size-1, size-1)

def generate_obstacle_heavy(size):
    grid = [[0 if random.random() > 0.3 else 1 for _ in range(size)] for _ in range(size)]
    grid[0][0], grid[size-1][size-1] = 0, 0
    return grid, (0, 0), (size-1, size-1)

def generate_snake_passage(size):
    grid = [[1]*size for _ in range(size)]
    for i in range(size):
        grid[i][i%size] = 0
    grid[0][0], grid[size-1][(size-1)%size] = 0, 0
    return grid, (0, 0), (size-1, (size-1)%size)

def generate_disconnected_grid(size):
    grid = [[1]*size for _ in range(size)]
    for i in range(size//2):
        for j in range(size//2):
            grid[i][j] = 0
    return grid, (0, 0), (size-1, size-1)

def generate_edge_hugging(size):
    grid = [[1]*size for _ in range(size)]
    for i in range(size):
        grid[0][i] = grid[i][0] = grid[size-1][i] = grid[i][size-1] = 0
    return grid, (0, 0), (size-1, size-1)

def generate_random_noise(size):
    random.seed(42)
    grid = [[0 if random.random() > 0.3 else 1 for _ in range(size)] for _ in range(size)]
    grid[0][0], grid[size-1][size-1] = 0, 0
    return grid, (0, 0), (size-1, size-1)

# List of generators
generators = [
    generate_empty_grid,
    generate_maze_grid,
    generate_obstacle_heavy,
    generate_snake_passage,
    generate_disconnected_grid,
    generate_edge_hugging,
    generate_random_noise
]

# Prepare 2 examples from each type
test_cases = []
for gen in generators:
    test_cases.append(gen(10))
    test_cases.append(gen(15))

# Benchmark
for idx, (grid, start, goal) in enumerate(test_cases, 1):
    basic_time = timeit.timeit(lambda: a_star_basic(grid, start, goal), number=1)
    absinf_time = timeit.timeit(lambda: a_star_absinf(grid, start, goal), number=1)
    print(f"Grid {idx}: Basic={basic_time:.6f}s | AbsInf={absinf_time:.6f}s")
