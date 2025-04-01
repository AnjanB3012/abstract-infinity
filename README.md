# Optimizing Dijkstra's Algorithm with Abstract Infinity

## Overview
This project explores an optimization technique for Dijkstra's shortest path algorithm by replacing ```float('inf')``` with an abstract infinity representation. Through various graph structures, we demonstrate that using abstract infinity leads to improved performance in terms of runtime efficiency.

## Motivation
Dijkstra's algorithm traditionally initializes node distances using ```float('inf')``` to represent unvisited nodes. However, this can introduce inefficiencies due to floating-point operations and memory handling. By leveraging an abstract infinity representation (such as a custom class or a high integer value), we optimize performance across different graph types.

