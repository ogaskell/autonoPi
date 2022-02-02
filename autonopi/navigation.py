#!/usr/bin/env python3

"""Navigation module."""

from math import inf
from typing import List

import networkx as nx


class Navigation:
    """A class to contain the navigation system."""

    def __init__(self):
        self.graph = nx.Graph()

        # This list will store a list of the node's IDs. This means the graph will only have to store an integer which
        # refers to an index in this list.
        self.nodes = []

    def add_node(self, node: object) -> None:
        """Add a node to the navigation graph."""
        self.nodes.append(node)
        self.graph.add_node(len(self.nodes) - 1)

    def setup_edges(self, distances: List[List[float]]) -> None:
        """Setup graph edges from a distance matrix.

        Note that any value < 0 indicates no connection, and this assumes an undirected graph so passing an assymetric
        distance matrix will result in undefined behaviour.
        """
        for x in range(len(self.nodes) - 1):
            for y in range(x + 1, len(self.nodes)):
                if distances[y][x] < 0:
                    continue
                else:
                    self.graph.add_edge(x, y, weight=distances[y][x])

        n = len(self.nodes)
        self.floyds_distances = nx.to_dict_of_dicts(self.graph)
        self.floyds_routes = [[x for x in range(n)] for y in range(n)]
        self.routes_current = False

    def floyds(self) -> None:
        """Run the Floyd-Warshall algorithm on the network.

        This will generate the shortest paths between any two nodes, which can be used in pathfinding.
        """
        n = len(self.nodes)
        distances = nx.to_dict_of_dicts(self.graph)
        routes = [[x for x in range(n)] for y in range(n)]

        # Ensure the distance matrix is "full".
        for y in range(n):
            if y not in distances.keys():
                distances[y] = {}

            for x in range(n):
                if x not in distances[y].keys():
                    distances[y][x] = {"weight": inf}

        # Actual Floyd's algorithm.
        for a in range(n):  # "Shaded" node
            # Only need to check one side of the diagonal, since the matrix is undirected.
            for y in range(n - 1):
                for x in range(y + 1, n):
                    if y == a or x == a:  # Don't need to consider shaded squares
                        continue

                    d0 = distances[y][x]["weight"]
                    d1 = distances[y][a]["weight"] + distances[a][x]["weight"]
                    if d0 > d1:
                        # Ensure both sides of the diagonal are updated.
                        distances[y][x]["weight"] = d1
                        distances[x][y]["weight"] = d1
                        routes[y][x] = a
                        routes[x][y] = a

        # Update distance, route matrices at a class level, and set the current route flag.
        self.floyds_distances = distances
        self.floyds_routes = routes
        # This flag will ensure that distance/route matrices are only used when they correspond
        # to the current graph state.
        self.routes_current = True

    def shortest_path(self, a: int, b: int) -> List[int]:
        """Using floyd's distance and route matrices, find the shortest path between two nodes.

        Returns a list of node IDs.
        """
        if a == b:
            return [a]
        else:
            return self.shortest_path(a, self.floyds_routes[b][a]) + [b]


class Node:
    """A Single node within a navigation graph."""

    def __init__(self, nav: Navigation, id: int):
        self.parent = nav  # Store reference to parent class

        self.id = id
