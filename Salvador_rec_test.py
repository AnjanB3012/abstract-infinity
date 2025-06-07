import time
import timeit
from absinf import AbsInf

def dijkstra_basic(graph, start):
    dist = {start: 0}
    pred = {}
    fixed = set()
    eligible = {start}

    while eligible:
        d, u = min((dist[v], v) for v in eligible)
        eligible.remove(u)
        fixed.add(u)
        for v, weight in graph[u].items():
            if v not in fixed:
                if v not in dist:
                    pred[v] = u
                    dist[v] = dist[u] + weight
                    eligible.add(v)
                elif dist[v] > dist[u] + weight:
                    pred[v] = u
                    dist[v] = dist[u] + weight

    # For compatibility: mark unreachable nodes with None or omit them
    # Since you're expecting all nodes with distances, fill in explicitly:
    for node in graph:
        if node not in dist:
            # Represent unreachable nodes by a large constant instead of infinity
            # or leave them out if you prefer strict no-infinity logic
            dist[node] = None  # Or use something like `9999999`

    return dist

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
            if distances[neighbor] > new_distance:
                distances[neighbor] = new_distance

        # Step 5: Mar current node as visited
        unvisited.remove(current)

    return distances

#Test Cases
graph = {
    'A': {'B': 10, 'C': 3},
    'B': {'D': 2},
    'C': {'B': 4, 'D': 8},
    'D': {}
}

# 1. Linear / Chain
Linear_Chain_1 = {"A": {"B": 2}, "B": {"C": 3}, "C": {"D": 1}, "D": {}}
Linear_Chain_2 = {"1": {"2": 5}, "2": {"3": 4}, "3": {"4": 6}, "4": {"5": 2}, "5": {}}

# 2. Sparse Tree
Sparse_Tree_1 = {"A": {"B": 1, "C": 2}, "B": {"D": 4}, "C": {"E": 3}, "D": {}, "E": {}}
Sparse_Tree_2 = {"1": {"2": 7}, "2": {"3": 5}, "3": {"4": 1, "5": 3}, "4": {}, "5": {}}

# 3. Dense Graph
Dense_Graph_1 = {
    "A": {"B": 2, "C": 5, "D": 1},
    "B": {"A": 2, "C": 3, "D": 2},
    "C": {"A": 5, "B": 3, "D": 1},
    "D": {"A": 1, "B": 2, "C": 1},
}
Dense_Graph_2 = {
    "1": {"2": 1, "3": 2, "4": 3},
    "2": {"1": 1, "3": 1, "4": 2},
    "3": {"1": 2, "2": 1, "4": 1},
    "4": {"1": 3, "2": 2, "3": 1},
}

# 4. Star Graph
Star_Graph_1 = {"A": {"B": 2, "C": 3, "D": 1}, "B": {}, "C": {}, "D": {}}
Star_Graph_2 = {"0": {"1": 5, "2": 4, "3": 6, "4": 7}, "1": {}, "2": {}, "3": {}, "4": {}}

# 5. Disconnected Graph
Disconnected_Graph_1 = {"A": {"B": 3}, "B": {"C": 4}, "C": {}, "X": {"Y": 1}, "Y": {}}
Disconnected_Graph_2 = {"1": {"2": 1}, "2": {}, "3": {"4": 2}, "4": {}, "5": {}}

# 6. Cycle Graph
Cycle_Graph_1 = {"A": {"B": 1}, "B": {"C": 2}, "C": {"A": 3}}
Cycle_Graph_2 = {"1": {"2": 1}, "2": {"3": 1}, "3": {"4": 1}, "4": {"1": 1}}

# 7. Equal Weights
Equal_Weights_1 = {"A": {"B": 1}, "B": {"C": 1}, "C": {"D": 1}, "D": {}}
Equal_Weights_2 = {"1": {"2": 1, "3": 1}, "2": {"4": 1}, "3": {"4": 1}, "4": {}}

# 8. Large Uniform Graph (e.g., 3x3 grid)
Large_Uniform_Graph_1 = {
    "A": {"B": 1, "D": 1},
    "B": {"A": 1, "C": 1, "E": 1},
    "C": {"B": 1, "F": 1},
    "D": {"A": 1, "E": 1, "G": 1},
    "E": {"B": 1, "D": 1, "F": 1, "H": 1},
    "F": {"C": 1, "E": 1, "I": 1},
    "G": {"D": 1, "H": 1},
    "H": {"E": 1, "G": 1, "I": 1},
    "I": {"F": 1, "H": 1},
}
Large_Uniform_Graph_2 = {
    "1": {"2": 1, "4": 1},
    "2": {"1": 1, "3": 1, "5": 1},
    "3": {"2": 1, "6": 1},
    "4": {"1": 1, "5": 1, "7": 1},
    "5": {"2": 1, "4": 1, "6": 1, "8": 1},
    "6": {"3": 1, "5": 1, "9": 1},
    "7": {"4": 1, "8": 1},
    "8": {"5": 1, "7": 1, "9": 1},
    "9": {"6": 1, "8": 1},
}

# 9. Worst-case Tie Graph (same cost via all paths)
Worst_Case_Tie_1 = {
    "A": {"B": 1, "C": 1},
    "B": {"D": 1},
    "C": {"D": 1},
    "D": {},
}
Worst_Case_Tie_2 = {
    "1": {"2": 2, "3": 2},
    "2": {"4": 2},
    "3": {"4": 2},
    "4": {},
}

# 10. Real-world-like Graph (road network style)
Real_World_Like_1 = {
    "Home": {"Gas_Station": 2, "Supermarket": 5},
    "Gas_Station": {"Work": 6},
    "Supermarket": {"Work": 2},
    "Work": {},
}
Real_World_Like_2 = {
    "Apt": {"Grocery": 3, "School": 6},
    "Grocery": {"Mall": 4},
    "School": {"Mall": 2},
    "Mall": {"Office": 5},
    "Office": {},
}

setup_code = '''
from __main__ import (
    dijkstra_basic, dijkstra_abs,
    Linear_Chain_1, Linear_Chain_2,
    Sparse_Tree_1, Sparse_Tree_2,
    Dense_Graph_1, Dense_Graph_2,
    Star_Graph_1, Star_Graph_2,
    Disconnected_Graph_1, Disconnected_Graph_2,
    Cycle_Graph_1, Cycle_Graph_2,
    Equal_Weights_1, Equal_Weights_2,
    Large_Uniform_Graph_1, Large_Uniform_Graph_2,
    Worst_Case_Tie_1, Worst_Case_Tie_2,
    Real_World_Like_1, Real_World_Like_2
)
'''

print(dijkstra_basic(Linear_Chain_1, 'A'))
print(dijkstra_abs(Linear_Chain_1, 'A'))

# Linear / Chain
Linear_Chain_test_basic1 = ''' 
dijkstra_basic(Linear_Chain_1, 'A')
'''
Linear_Chain_test_abs1 = ''' 
dijkstra_abs(Linear_Chain_1, 'A')
'''

Linear_Chain_test_basic2 = ''' 
dijkstra_basic(Linear_Chain_2, '1')
'''
Linear_Chain_test_abs2 = ''' 
dijkstra_abs(Linear_Chain_2, '1')
'''

# Sparse Tree
Sparse_Tree_test_basic1 = ''' 
dijkstra_basic(Sparse_Tree_1, 'A')
'''
Sparse_Tree_test_abs1 = ''' 
dijkstra_abs(Sparse_Tree_1, 'A')
'''

Sparse_Tree_test_basic2 = ''' 
dijkstra_basic(Sparse_Tree_2, '1')
'''
Sparse_Tree_test_abs2 = ''' 
dijkstra_abs(Sparse_Tree_2, '1')
'''

# Dense Graph
Dense_Graph_test_basic1 = ''' 
dijkstra_basic(Dense_Graph_1, 'A')
'''
Dense_Graph_test_abs1 = ''' 
dijkstra_abs(Dense_Graph_1, 'A')
'''

Dense_Graph_test_basic2 = ''' 
dijkstra_basic(Dense_Graph_2, '1')
'''
Dense_Graph_test_abs2 = ''' 
dijkstra_abs(Dense_Graph_2, '1')
'''

# Star Graph
Star_Graph_test_basic1 = ''' 
dijkstra_basic(Star_Graph_1, 'A')
'''
Star_Graph_test_abs1 = ''' 
dijkstra_abs(Star_Graph_1, 'A')
'''

Star_Graph_test_basic2 = ''' 
dijkstra_basic(Star_Graph_2, '0')
'''
Star_Graph_test_abs2 = ''' 
dijkstra_abs(Star_Graph_2, '0')
'''

# Disconnected Graph
Disconnected_Graph_test_basic1 = ''' 
dijkstra_basic(Disconnected_Graph_1, 'A')
'''
Disconnected_Graph_test_abs1 = ''' 
dijkstra_abs(Disconnected_Graph_1, 'A')
'''

Disconnected_Graph_test_basic2 = ''' 
dijkstra_basic(Disconnected_Graph_2, '1')
'''
Disconnected_Graph_test_abs2 = ''' 
dijkstra_abs(Disconnected_Graph_2, '1')
'''

# Cycle Graph
Cycle_Graph_test_basic1 = ''' 
dijkstra_basic(Cycle_Graph_1, 'A')
'''
Cycle_Graph_test_abs1 = ''' 
dijkstra_abs(Cycle_Graph_1, 'A')
'''

Cycle_Graph_test_basic2 = ''' 
dijkstra_basic(Cycle_Graph_2, '1')
'''
Cycle_Graph_test_abs2 = ''' 
dijkstra_abs(Cycle_Graph_2, '1')
'''

# Equal Weights
Equal_Weights_test_basic1 = ''' 
dijkstra_basic(Equal_Weights_1, 'A')
'''
Equal_Weights_test_abs1 = ''' 
dijkstra_abs(Equal_Weights_1, 'A')
'''

Equal_Weights_test_basic2 = ''' 
dijkstra_basic(Equal_Weights_2, '1')
'''
Equal_Weights_test_abs2 = ''' 
dijkstra_abs(Equal_Weights_2, '1')
'''

# Large Uniform Graph
Large_Uniform_Graph_test_basic1 = ''' 
dijkstra_basic(Large_Uniform_Graph_1, 'A')
'''
Large_Uniform_Graph_test_abs1 = ''' 
dijkstra_abs(Large_Uniform_Graph_1, 'A')
'''

Large_Uniform_Graph_test_basic2 = ''' 
dijkstra_basic(Large_Uniform_Graph_2, '1')
'''
Large_Uniform_Graph_test_abs2 = ''' 
dijkstra_abs(Large_Uniform_Graph_2, '1')
'''

# Worst-case Tie Graph
Worst_Case_Tie_test_basic1 = ''' 
dijkstra_basic(Worst_Case_Tie_1, 'A')
'''
Worst_Case_Tie_test_abs1 = ''' 
dijkstra_abs(Worst_Case_Tie_1, 'A')
'''

Worst_Case_Tie_test_basic2 = ''' 
dijkstra_basic(Worst_Case_Tie_2, '1')
'''
Worst_Case_Tie_test_abs2 = ''' 
dijkstra_abs(Worst_Case_Tie_2, '1')
'''

# Real-world-like Graph
Real_World_Like_test_basic1 = ''' 
dijkstra_basic(Real_World_Like_1, 'Home')
'''
Real_World_Like_test_abs1 = ''' 
dijkstra_abs(Real_World_Like_1, 'Home')
'''

Real_World_Like_test_basic2 = ''' 
dijkstra_basic(Real_World_Like_2, 'Apt')
'''
Real_World_Like_test_abs2 = ''' 
dijkstra_abs(Real_World_Like_2, 'Apt')
'''

print("--------------------------------------------------------------------------")
print("Runtime with float('inf') for Linear Chain Test 1:"+str(timeit.timeit(stmt=Linear_Chain_test_basic1, setup=setup_code, number=50000)))
print("Runtime with abstract infinity for Linear Chain Test 1:"+str(timeit.timeit(stmt=Linear_Chain_test_abs1, setup=setup_code, number=50000)))
print("Runtime with float('inf') for Linear Chain Test 2:"+str(timeit.timeit(stmt=Linear_Chain_test_basic2, setup=setup_code, number=50000)))
print("Runtime with abstract infinity for Linear Chain Test 2:"+str(timeit.timeit(stmt=Linear_Chain_test_abs2, setup=setup_code, number=50000)))
print("--------------------------------------------------------------------------")
print("Runtime with float('inf') for Sparse Tree Test 1:"+str(timeit.timeit(stmt=Sparse_Tree_test_basic1, setup=setup_code, number=50000)))
print("Runtime with abstract infinity for Sparse Tree Test 1:"+str(timeit.timeit(stmt=Sparse_Tree_test_abs1, setup=setup_code, number=50000)))
print("Runtime with float('inf') for Sparse Tree Test 2:"+str(timeit.timeit(stmt=Sparse_Tree_test_basic2, setup=setup_code, number=50000)))
print("Runtime with abstract infinity for Sparse Tree Test 2:"+str(timeit.timeit(stmt=Sparse_Tree_test_abs2, setup=setup_code, number=50000)))
print("--------------------------------------------------------------------------")
print("Runtime with float('inf') for Dense Graph Test 1:"+str(timeit.timeit(stmt=Dense_Graph_test_basic1, setup=setup_code, number=50000)))
print("Runtime with abstract infinity for Dense Graph Test 1:"+str(timeit.timeit(stmt=Dense_Graph_test_abs1, setup=setup_code, number=50000)))
print("Runtime with float('inf') for Dense Graph Test 2:"+str(timeit.timeit(stmt=Dense_Graph_test_basic2, setup=setup_code, number=50000)))
print("Runtime with abstract infinity for Dense Graph Test 2:"+str(timeit.timeit(stmt=Dense_Graph_test_abs2, setup=setup_code, number=50000)))
print("--------------------------------------------------------------------------")
print("Runtime with float('inf') for Star Graph Test 1:"+str(timeit.timeit(stmt=Star_Graph_test_basic1, setup=setup_code, number=50000)))
print("Runtime with abstract infinity for Star Graph Test 1:"+str(timeit.timeit(stmt=Star_Graph_test_abs1, setup=setup_code, number=50000)))
print("Runtime with float('inf') for Star Graph Test 2:"+str(timeit.timeit(stmt=Star_Graph_test_basic2, setup=setup_code, number=50000)))
print("Runtime with abstract infinity for Star Graph Test 2:"+str(timeit.timeit(stmt=Star_Graph_test_abs2, setup=setup_code, number=50000)))
print("--------------------------------------------------------------------------")
print("Runtime with float('inf') for Disconnected Graph Test 1:"+str(timeit.timeit(stmt=Disconnected_Graph_test_basic1, setup=setup_code, number=50000)))
print("Runtime with abstract infinity for Disconnected Graph Test 1:"+str(timeit.timeit(stmt=Disconnected_Graph_test_abs1, setup=setup_code, number=50000)))
print("Runtime with float('inf') for Disconnected Graph Test 2:"+str(timeit.timeit(stmt=Disconnected_Graph_test_basic2, setup=setup_code, number=50000)))
print("Runtime with abstract infinity for Disconnected Graph Test 2:"+str(timeit.timeit(stmt=Disconnected_Graph_test_abs2, setup=setup_code, number=50000)))
print("--------------------------------------------------------------------------")
print("Runtime with float('inf') for Cycle Graph Test 1:"+str(timeit.timeit(stmt=Cycle_Graph_test_basic1, setup=setup_code, number=50000)))
print("Runtime with abstract infinity for Cycle Graph Test 1:"+str(timeit.timeit(stmt=Cycle_Graph_test_abs1, setup=setup_code, number=50000)))
print("Runtime with float('inf') for Cycle Graph Test 2:"+str(timeit.timeit(stmt=Cycle_Graph_test_basic2, setup=setup_code, number=50000)))
print("Runtime with abstract infinity for Cycle Graph Test 2:"+str(timeit.timeit(stmt=Cycle_Graph_test_abs2, setup=setup_code, number=50000)))
print("--------------------------------------------------------------------------")
print("Runtime with float('inf') for Equal Weights Test 1:"+str(timeit.timeit(stmt=Equal_Weights_test_basic1, setup=setup_code, number=50000)))
print("Runtime with abstract infinity for Equal Weights Test 1:"+str(timeit.timeit(stmt=Equal_Weights_test_abs1, setup=setup_code, number=50000)))
print("Runtime with float('inf') for Equal Weights Test 2:"+str(timeit.timeit(stmt=Equal_Weights_test_basic2, setup=setup_code, number=50000)))
print("Runtime with abstract infinity for Equal Weights Test 2:"+str(timeit.timeit(stmt=Equal_Weights_test_abs2, setup=setup_code, number=50000)))
print("--------------------------------------------------------------------------")
print("Runtime with float('inf') for Large Uniform Graph Test 1:"+str(timeit.timeit(stmt=Large_Uniform_Graph_test_basic1, setup=setup_code, number=50000)))
print("Runtime with abstract infinity for Large Uniform Graph Test 1:"+str(timeit.timeit(stmt=Large_Uniform_Graph_test_abs1, setup=setup_code, number=50000)))
print("Runtime with float('inf') for Large Uniform Graph Test 2:"+str(timeit.timeit(stmt=Large_Uniform_Graph_test_basic2, setup=setup_code, number=50000)))
print("Runtime with abstract infinity for Large Uniform Graph Test 2:"+str(timeit.timeit(stmt=Large_Uniform_Graph_test_abs2, setup=setup_code, number=50000)))
print("--------------------------------------------------------------------------")
print("Runtime with float('inf') for Worst Case Tie Graph Test 1:"+str(timeit.timeit(stmt=Worst_Case_Tie_test_basic1, setup=setup_code, number=50000)))
print("Runtime with abstract infinity for Worst Case Tie Graph Test 1:"+str(timeit.timeit(stmt=Worst_Case_Tie_test_abs1, setup=setup_code, number=50000)))
print("Runtime with float('inf') for Worst Case Tie Graph Test 2:"+str(timeit.timeit(stmt=Worst_Case_Tie_test_basic2, setup=setup_code, number=50000)))
print("Runtime with abstract infinity for Worst Case Tie Graph Test 2:"+str(timeit.timeit(stmt=Worst_Case_Tie_test_abs2, setup=setup_code, number=50000)))
print("--------------------------------------------------------------------------")
print("Runtime with float('inf') for Real World Graph Test 1:"+str(timeit.timeit(stmt=Real_World_Like_test_basic1, setup=setup_code, number=50000)))
print("Runtime with abstract infinity for Real World Graph Test 1:"+str(timeit.timeit(stmt=Real_World_Like_test_abs1, setup=setup_code, number=50000)))
print("Runtime with float('inf') for Real World Graph Test 2:"+str(timeit.timeit(stmt=Real_World_Like_test_basic2, setup=setup_code, number=50000)))
print("Runtime with abstract infinity for Real World Graph Test 2:"+str(timeit.timeit(stmt=Real_World_Like_test_abs2, setup=setup_code, number=50000)))
print("--------------------------------------------------------------------------")