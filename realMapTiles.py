import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from absinf import AbsInf
import timeit
import threading

place = "Blacksburg, Virginia, USA"
G = ox.graph_from_place(place, network_type='drive')
G = G.to_undirected()

graph = {}
for u, v, data in G.edges(data=True):
    weight = data.get("length", 1)
    graph.setdefault(u, []).append((v, weight))
    graph.setdefault(v, []).append((u, weight))

orig_coords = (37.22110776412903, -80.42218184640652)
dest_coords = (37.2171688442949, -80.40276057917632)

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

def show_path_async(G, path):
    def plot():
        fig, ax = ox.plot_graph_route(G, path, route_color='r', node_size=0, show=True, close=False)
    threading.Thread(target=plot).start()

# Run and time basic
distance_basic, path_basic = dijkstra_basic(graph, start, end)
print("Basic Distance:", distance_basic)
show_path_async(G, path_basic)

# Run and time AbsInf
distance_abs, path_abs = dijkstra_abs(graph, start, end)
print("AbsInf Distance:", distance_abs)
show_path_async(G, path_abs)
