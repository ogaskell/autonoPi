#!/usr/bin/env python3

"""Navigation module."""

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

    def setup_edges(self, distances: list[list[float]]) -> None:
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


class Node:
    """A Single node within a navigation graph."""

    def __init__(self, nav: Navigation, id: int):
        self.parent = nav  # Store reference to parent class

        self.id = id
