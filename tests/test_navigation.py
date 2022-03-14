"""Test navigation.py."""

import random
import unittest
from math import inf

# Note that due to the way the module is imported, this file must be ran from the root directory of the project,
#  not from the tests folder.
from autonopi import navigation as nav


class TestNode(unittest.TestCase):
    """Test the Node() class."""

    def test_init(self) -> None:
        """Test initialising Nodes."""
        # Setup
        id = random.randint(0, 1000)

        # Code to Test
        n = nav.Node(None, id)

        # Testing
        self.assertEqual(n.id, id)  # Ensure ID is set correctly
        self.assertIsInstance(n, nav.Node)  # Ensure n is actually a Node object


class TestNavigation(unittest.TestCase):
    """Test the Navigation class."""

    def test_add_node(self) -> None:
        """Test adding Nodes."""
        # Setup
        n = nav.Navigation()
        nodes = [nav.Node(n, x) for x in range(10)]

        # Code to test
        for node in nodes:
            n.add_node(node)

        # Testing
        for x, node in enumerate(nodes):
            self.assertIs(n.nodes[x], nodes[x])

    def test_setup_weights(self) -> None:
        """Test setting up the distance matrix."""
        # Setup
        n = nav.Navigation()
        nodes = [nav.Node(n, x) for x in range(5)]
        for node in nodes:
            n.add_node(node)

        # Code to Test
        dists = [[-1, 3, -1, 12, 2],
                 [3, -1, 2, 5, 12],
                 [-1, 2, -1, -1, -1],
                 [12, 5, -1, -1, 0.5],
                 [2, 12, -1, 0.5, -1],
                 ]

        n.setup_edges(dists)

        # Testing
        for y in range(5):
            for x in range(5):
                # This check is required since the distance matrix includes edges that don't exist as -1, wheras
                #  looking these up in the NetworkX graph simply throws a KeyError.
                if (d := dists[y][x]) >= 0:
                    self.assertEqual(d, n.graph[y][x]["weight"])

    def test_floyds(self) -> None:
        """Test Implementation of the Floyd-Warshall algorithm."""
        # Setup
        n = nav.Navigation()
        nodes = [nav.Node(n, x) for x in range(5)]
        for node in nodes:
            n.add_node(node)

        expected_distances = {
            0: {
                0: {'weight': inf},
                1: {'weight': 3},
                2: {'weight': 5},
                3: {'weight': 2.5},
                4: {'weight': 2},
            },
            1: {
                0: {'weight': 3},
                1: {'weight': inf},
                2: {'weight': 2},
                3: {'weight': 5},
                4: {'weight': 5}},
            2: {
                0: {'weight': 5},
                1: {'weight': 2},
                2: {'weight': inf},
                3: {'weight': 7},
                4: {'weight': 7},
            },
            3: {
                0: {'weight': 2.5},
                1: {'weight': 5},
                2: {'weight': 7},
                3: {'weight': inf},
                4: {'weight': 0.5}
            },
            4: {
                0: {'weight': 2},
                1: {'weight': 5},
                2: {'weight': 7},
                3: {'weight': 0.5},
                4: {'weight': inf},
            },
        }

        expected_routes = [
            [0, 1, 1, 4, 4],
            [0, 1, 2, 3, 0],
            [1, 1, 2, 1, 1],
            [4, 1, 1, 3, 4],
            [0, 0, 1, 3, 4],
        ]

        dists = [[-1, 3, -1, 12, 2],
                 [3, -1, 2, 5, 12],
                 [-1, 2, -1, -1, -1],
                 [12, 5, -1, -1, 0.5],
                 [2, 12, -1, 0.5, -1],
                 ]

        n.setup_edges(dists)

        # Code to Test
        n.floyds()

        # Testing
        self.assertEqual(n.floyds_distances, expected_distances)
        self.assertEqual(n.floyds_routes, expected_routes)


if __name__ == "__main__":
    unittest.main()
