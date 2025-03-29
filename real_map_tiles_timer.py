import osmnx as ox
import timeit
import networkx as nx
import matplotlib.pyplot as plt
from absinf import AbsInf
import threading

# place = "Bengaluru , Karnataka, India"
orig_coords = (12.928187365833969, 77.68248261476438)
G = ox.graph_from_point(orig_coords, dist=7500, network_type='drive')
G = G.to_undirected()


# Build a simple graph representation
graph = {}
for u, v, data in G.edges(data=True):
    weight = data.get("length", 1)  # distance in meters
    graph.setdefault(u, []).append((v, weight))
    graph.setdefault(v, []).append((u, weight))  # if it's undirected

# Get coordinates directly (e.g., using Google Maps)
dest_coords = (12.901033525487962, 77.70721338095277)

start = ox.distance.nearest_nodes(G, X=orig_coords[1], Y=orig_coords[0])
end = ox.distance.nearest_nodes(G, X=dest_coords[1], Y=dest_coords[0])

def dijkstra_basic(graph, start, end):
    unvisited = list(graph.keys())
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {}

    while unvisited:
        current = min((node for node in unvisited), key=lambda node: distances[node])
        for neighbor, weight in graph[current]:
            new_distance = distances[current] + weight
            if distances[neighbor] > new_distance:
                distances[neighbor] = new_distance
                previous[neighbor] = current
        unvisited.remove(current)

    # Reconstruct the path
    path = []
    current = end
    while current != start:
        path.append(current)
        current = previous.get(current, start)
    path.append(start)
    path.reverse()
    return distances[end], path

def dijkstra_abs(graph, start, end):
    unvisited = list(graph.keys())
    distances = {node: AbsInf() for node in graph}
    distances[start] = 0
    previous = {}

    while unvisited:
        current = min((node for node in unvisited), key=lambda node: distances[node])
        for neighbor, weight in graph[current]:
            new_distance = distances[current] + weight
            if distances[neighbor] > new_distance:
                distances[neighbor] = new_distance
                previous[neighbor] = current
        unvisited.remove(current)

    path = []
    current = end
    while current != start:
        path.append(current)
        current = previous.get(current, start)
    path.append(start)
    path.reverse()
    return distances[end], path


setup_code = '''
from __main__ import (
    dijkstra_basic, graph,
    start, end, ox, G, dijkstra_abs
)
'''

Map_test_basic1 = ''' 
distance, path = dijkstra_basic(graph, start, end)
'''

Map_test_abs1 = ''' 
distance, path = dijkstra_abs(graph, start, end)
'''

print(timeit.timeit(stmt=Map_test_basic1,setup=setup_code, number=1))
print(timeit.timeit(stmt=Map_test_abs1,setup=setup_code, number=1))

distance_basic, path_basic = dijkstra_abs(graph, start, end)
ox.plot_graph_route(G, path_basic, route_color='r', node_size=0, show=True, close=False)