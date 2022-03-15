"""Non-automated graphical test methods for navigation.py."""

import os
import sys
from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# noqa required here as there's no way I can comply with E402.
from autonopi import navigation as nav  # noqa: E402


class Tests:
    """Test suite."""

    def __init__(self):
        self.navigation = nav.Navigation()

        for n in range(5):
            self.navigation.add_node(nav.Node(self.navigation, n))

            dists = [[-1, 3, 1, 12, 2],
                     [3, -1, 2, 5, 12],
                     [1, 2, -1, -1, -1],
                     [12, 5, -1, -1, 0.5],
                     [2, 12, -1, 0.5, -1],
                     ]

            self.navigation.setup_edges(dists)

    def test_edges(self) -> None:
        """pass."""
        pos = nx.circular_layout(self.navigation.graph)
        nx.draw(self.navigation.graph, pos, with_labels=True)
        labels = nx.get_edge_attributes(self.navigation.graph, 'weight')
        nx.draw_networkx_edge_labels(self.navigation.graph, pos, edge_labels=labels)
        plt.show()

    def test_floyds(self) -> None:
        """Test floyd's algorithm."""
        self.navigation.floyds()
        pprint(self.navigation.floyds_routes)
        pprint(self.navigation.floyds_distances)

        print(self.navigation.shortest_path(2, 3))


if __name__ == "__main__":
    T = Tests()
    T.test_edges()
    T.test_floyds()
    print(T.navigation.floyds_distances[3][0] is T.navigation.floyds_distances[0][3])
