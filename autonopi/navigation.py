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

    def __init__(self, nav: Navigation, id: int = None):
        self.parent = nav  # Store reference to parent class

        if id is None:  # Check if an ID is provided.
            self.id = self.generate_id()  # If not, generate one.
        else:
            self.id = id

    def __hash__(self) -> int:
        """Return the ID of the Node as a hash value.

        Technically this is a very incorrect was of calculating a hash, since
        it should be calculated based on the objects data. However, the Node
        doesn't really have any data the hash may be calculated from, and the ID
        will be unique so should suffice for my use.
        """
        return self.id

    def generate_id(self) -> int:
        """Generate a unique ID for the current node.

        Currently just a template, will need to be replaced with functional
        code at a later date.
        """
        return 0
