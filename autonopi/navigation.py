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


class Node:
    """A Single node within a navigation graph."""

    def __init__(self, nav: Navigation, id: int):
        self.parent = nav  # Store reference to parent class

        self.id = id
