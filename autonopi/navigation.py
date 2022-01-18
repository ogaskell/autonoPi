#!/usr/bin/env python3

"""Navigation module."""


class Navigation:
    """A class to contain the navigation system."""

    def __init__(self):
        pass


class Node:
    """A Single node within a navigation graph."""

    def __init__(self, nav: Navigation, id: int = None):
        self.parent = nav  # Store reference to parent class

        if id is None:  # Check if an ID is provided.
            self.id = self.generate_id()  # If not, generate one.
        else:
            self.id = id

    def generate_id(self) -> int:
        """Generate a unique ID for the current node.

        Currently just a template, will need to be replaced with functional
        code at a later date.
        """
        return 0
