import time
import timeit
from absinf import AbsInf

def dijkstra_basic(graph, start):
    # Step 1: Set initial distances to infinity, except for the start node
    unvisited = list(graph.keys())
    # distances = {node: absinf.absinf() for node in graph}
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    # Step 2: Loop until all nodes are visited
    while unvisited:
        # Step 3: Pick the unvisited node with the smallest distance
        current = min((node for node in unvisited), key=lambda node: distances[node])

        # Step 4: Update distances of neighbors
        for neighbor, weight in graph[current].items():
            new_distance = distances[current] + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance

        # Step 5: Mark current node as visited
        unvisited.remove(current)

    return distances

def dijkstra_abs(graph,start):
    # Step 1: Set initial distances to infinity, except for the start node
    unvisited = list(graph.keys())
    # distances = {node: absinf.absinf() for node in graph}
    distances = {node: AbsInf() for node in graph}
    distances[start] = 0

    # Step 2: Loop until all nodes are visited
    while unvisited:
        # Step 3: Pick the unvisited node with the smallest distance
        current = min((node for node in unvisited), key=lambda node: distances[node])

        # Step 4: Update distances of neighbors
        for neighbor, weight in graph[current].items():
            new_distance = distances[current] + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance

        # Step 5: Mark current node as visited
        unvisited.remove(current)

    return distances

# graph = {
#     'A': {'B': 2, 'C': 1},
#     'B': {'D': 3},
#     'C': {'D': 1},
#     'D': {}
# }
graph = {
    'A': {'B': 10, 'C': 3},
    'B': {'D': 2},
    'C': {'B': 4, 'D': 8},
    'D': {}
}


print(dijkstra_basic(graph, 'A'))
print(dijkstra_abs(graph, 'A'))


setup_code = '''
from __main__ import dijkstra_basic, graph, dijkstra_abs
'''

test_code1 = '''
dijkstra_basic(graph, 'A')
'''

test_code2 = '''
dijkstra_abs(graph, 'A')
'''

print(timeit.timeit(stmt=test_code1, setup=setup_code, number=500000))
print(timeit.timeit(stmt=test_code2, setup=setup_code, number=500000))