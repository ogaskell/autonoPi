"""Non-automated graphical test methods for navigation.py."""

import os
import sys

import matplotlib.pyplot as plt
import networkx as nx

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# noqa required here as there's no way I can comply with E402.
from autonopi import navigation as nav  # noqa: E402


def test_edges() -> None:
    """pass."""
    navigation = nav.Navigation()

    for n in range(5):
        navigation.add_node(nav.Node(navigation, n))

    dists = [[-1, 3, 1, 12, 2],
             [3, -1, 2, 5, 12],
             [1, 2, -1, -1, -1],
             [12, 5, -1, -1, 0.5],
             [2, 12, -1, 0.5, -1],
             ]

    navigation.setup_edges(dists)

    pos = nx.circular_layout(navigation.graph)
    nx.draw(navigation.graph, pos, with_labels=True)
    labels = nx.get_edge_attributes(navigation.graph, 'weight')
    nx.draw_networkx_edge_labels(navigation.graph, pos, edge_labels=labels)
    plt.show()


if __name__ == "__main__":
    test_edges()
