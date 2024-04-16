import networkx as nx


class Sabotage:
    """Sabotages the network by removing vertices from it"""
    def __init__(self, network: nx.graph, centralities: dict):
        self.network = network
        self.n_of_nodes = self.network.number_of_nodes()
        self.centralities = centralities

    def destroy_vertices(self, fraction: float=None, number: int=None):
        """Removes a given amount of the most important vertices (based on given centralities) from the network"""
        if fraction and number:
            raise Exception("Only one input type can be given")
        elif fraction and not 0 < fraction < 1:
            raise ValueError(f"Given percentage {fraction * 100:.2f}% is not between 0-100%.")
        elif number and not 0 < number < self.n_of_nodes:
            raise ValueError(f"Given amount of vertices to remove must be between 1-{self.n_of_nodes - 1}")

        num_to_remove = number if number else int(len(self.network.nodes) * fraction)
        sorted_nodes_by_degree = sorted(self.centralities, key=self.centralities.get, reverse=True)
        nodes_to_remove = sorted_nodes_by_degree[:num_to_remove]

        network_copy = self.network.copy()
        network_copy.remove_nodes_from(nodes_to_remove)
        return network_copy
