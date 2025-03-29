import osmnx as ox
import timeit
import networkx as nx
import matplotlib.pyplot as plt
from absinf import AbsInf
import threading
import sys
import Emailer
import re

sys.stdout = open("benchmarks\\real_maps_tests_1.txt","w")
test_routes = {
    "McComas Hall(895 Washington St SW, Blacksburg, VA 24060) To Kroger South(1322 S Main St, Blacksburg, VA 24060)":[(37.22077736791238, -80.42247000488936),4000,(37.21689030678678, -80.40265650118901)],
    "McComas Hall(895 Washington St SW, Blacksburg, VA 24060) To Kroger North(903 University City Blvd, Blacksburg, VA 24060)":[(37.22077736791238, -80.42247000488936),4000,(37.23552264245645, -80.43524403205011)],
    "The Inn(901 Prices Fork Rd, Blacksburg, VA 24061) to Pamplin Hall(880 W Campus Dr, Blacksburg, VA 24061)":[(37.23001825689157, -80.43000178079231),2500,(37.228762507887176, -80.42473392243994)],
    "Fairfield by Marriott Bengaluru(Marathahalli - Sarjapur Outer Ring Rd, Bellandur, Bengaluru, Karnataka 560103, India) to Decathlon Sports Sarjapura(Survey 96/1, After Wipro Corporate Office - Railway Crossing, Sarjapur Main Rd, Bengaluru, Karnataka 560035, India)":[(12.928164368027304, 77.68253489278254),9000,(12.902935714851331, 77.70700861321126)],
    "St Johns Hospital BMTC Bus Stand(WJH8+R9H, Sarjapur - Marathahalli Rd, Santhosapuram, Koramangala Industrial Layout, Koramangala, Bengaluru, Karnataka 560034, India) to The Rameshwaram Cafe(847/1(Old No. 847/A), Binnamangala 1st Stage, 100 Feet Rd, Bengaluru, Karnataka 560038, India)":[(12.929317600267492, 77.61759068476289),9000,(12.983308622269272, 77.64085481287738)],
    "M.A. Chidambaram Stadium(1, Wallahjah Rd, Chepauk, Triplicane, Chennai, Tamil Nadu 600002, India) to Chennai Lighthouse(Marina Beach Road, Marina Beach, Mylapore, Chennai, Tamil Nadu 600004, India)":[(13.063095632837598, 80.27942274907355),4000,(13.040466160210698, 80.27929182736985)],
    "Dr. MGR Block(X594+J88, Vellore, Tamil Nadu 632014, India) to Katpadi Railway Station(Katpadi Jct, KRS Nagar, Katpadi, Vellore, Tamil Nadu 632007, India)":[(12.969217680093521, 79.15580660978962),4000,(12.972139845854452, 79.13782641820697)],
    "Lambert High School(805 Nichols Rd, Suwanee, GA 30024) to Riverwatch Middle School(610 James Burgess Rd #1135, Suwanee, GA 30024)":[(34.10641389262153, -84.13890857432139),7000,(34.12447446253152, -84.10939258191553)]
}

setup_code = '''
from __main__ import (
    dijkstra_basic, graph,
    start, end, ox, G, dijkstra_abs
)
'''

emailIngString = "The Results for this run of Dijkstra's Algorithm:\n"

def sanitize_filename(name, max_length=80):
    # Replace any character that is not a letter, number, or underscore
    name = re.sub(r'[^a-zA-Z0-9]', '_', name)
    return name[:max_length]  # Trim long names for safety

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

i=1

for key in test_routes:
    orig_coords = test_routes[key][0]
    G = ox.graph_from_point(orig_coords, dist=test_routes[key][1], network_type='drive')
    G = G.to_undirected()
    graph = {}
    for u, v, data in G.edges(data=True):
        weight = data.get("length", 1)
        graph.setdefault(u, []).append((v, weight))
        graph.setdefault(v, []).append((u, weight))  
    dest_coords = test_routes[key][2]
    start = ox.distance.nearest_nodes(G, X=orig_coords[1], Y=orig_coords[0])
    end = ox.distance.nearest_nodes(G, X=dest_coords[1], Y=dest_coords[0])

    Map_test_basic = ''' 
distance, path = dijkstra_basic(graph, start, end)
'''

    Map_test_abs = ''' 
distance, path = dijkstra_abs(graph, start, end)
'''
    
    emailIngString+="----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"+"\n"
    emailIngString+="The time it took for the algorithm with float('inf') to compute the route from "+key+" is "+str(timeit.timeit(stmt=Map_test_basic,setup=setup_code, number=1))+"\n"
    emailIngString+="The time it took for the algorithm with AbsInf to compute the route from "+key+" is "+str(timeit.timeit(stmt=Map_test_abs,setup=setup_code, number=1))+"\n"
    emailIngString+="----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"+"\n"

    distance, path = dijkstra_abs(graph=graph,start=start,end=end)
    fig, ax = ox.plot_graph_route(G, path, show=False, close=False)
    filename = f"maps/{i}.png"
    i+=1
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close(fig)

email = Emailer.Emailer()
email.createEmail("anjanbellamkonda@vt.edu",emailIngString)