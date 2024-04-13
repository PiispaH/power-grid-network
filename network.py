#
# Simple "analysis" of some power grid network in the united states
#

from pprint import pprint
import time

import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns


class Network:
    """This class represents a network"""

    def __init__(self, filepath: str):
        self.network = None
        self._load_network(filepath)
        if not self.network:
            raise Exception("Something bad happened when loading the graph...")
        # Amount of nodes and edges
        self.nodes = self.network.number_of_nodes()
        self.edges = self.network.number_of_edges()

    def _load_network(self, filepath: str):
        self.network = nx.read_gml(filepath, label=None)


class Sabotage:
    """Terrorizes the network by removing vertices from it"""
    def __init__(self, network: nx.graph, degree_centralities: dict):
        self.network = network
        self.n_of_nodes = self.network.number_of_nodes()
        self.degree_centralities = degree_centralities

    def destroy_vertices(self, fraction: float=None, number: int=None):
        """removes a given amount of the most important vertices from the network"""
        if fraction and number:
            raise Exception("Only one input type can be given")
        elif fraction and not 0 < fraction < 1:
            raise ValueError(f"Given percentage {fraction * 100:.2f}% is not in range 0-100%.")
        elif number and not 0 < number < self.n_of_nodes:
            raise ValueError(f"Given amount of vertices to remove must be between 0-{self.n_of_nodes}")

        num_to_remove = number if number else int(len(self.network.nodes) * fraction)
        sorted_nodes_by_degree = sorted(self.degree_centralities, key=self.degree_centralities.get, reverse=True)
        nodes_to_remove = sorted_nodes_by_degree[:num_to_remove]

        bombfield = self.network.copy()
        bombfield.remove_nodes_from(nodes_to_remove)
        return bombfield

class Analyzer(Network):
    """This class analyzes a network"""

    def __init__(self, filepath: str):
        super().__init__(filepath)
        self.mean_degree = 0
        self.degree_distribution = []
        self.eigenvalue_centralities = {}
        self.degree_centralities = {}
        self.clustering_coefficients = []

    def run(self):
        degrees = dict(self.network.degree())
        self.mean_degree = sum(degrees.values()) / len(degrees)
        self.clustering_coefficients = nx.clustering(self.network)
        self.degree_distribution = self._calc_degree_distribution()
        self.degree_centralities = nx.degree_centrality(self.network)
        self.eigenvalue_centralities = nx.eigenvector_centrality(self.network)

        print(nx.is_connected(self.network))
        print(nx.number_connected_components(self.network))

        hurricane = Sabotage(self.network, self.degree_centralities)
        network_911 = hurricane.destroy_vertices(fraction=0.01)  # fraction=0.01 or number=100

        print(nx.is_connected(network_911))
        print(nx.number_connected_components(network_911))

        sizes_of_components = list(len(i) for i in sorted(nx.connected_components(network_911), key=len, reverse=True))
        print(sizes_of_components)

    def plot_and_print(self):
        """Prints the data and plots the graphs"""
        print(f"Mean degree: {self.mean_degree:.3g}\n")
        self._plot_degree_distribution()
        self._plot_eigenvalue_centralities()
        self._plot_clustering_coefficients()
        self._plot_degree_centralities()

    def _calc_degree_distribution(self):
        """Caclulates the degree distribution of the network"""
        degrees = {}
        network = {key: {x for x in value} for key, value in nx.to_dict_of_dicts(self.network).items()}
        for i in network:
            degree = len(network[i])
            if degree not in degrees:
                degrees[degree] = 0
            degrees[degree] += 1
        return {key: value / self.nodes for key, value in degrees.items()}

    def _plot_anything(self, data_type: str):
        """This is not needed but would make for prettier code"""
        selected = {
            "d_distr": self.degree_distribution,
            "e_centr": self.eigenvalue_centralities,
            "d_centr": self.degree_centralities,
            "c_coeff": self.clustering_coefficients,
        }.get(data_type)
        if not selected:
            raise Exception("Option not registered.")
        
        # TODO the actual implementation...

    def _plot_degree_distribution(self):
        """Plots the degree distribution"""
        plot = sns.barplot(self.degree_distribution)
        # plot.set_yscale("log")
        plot.set_xlabel("degree k")
        plot.set_ylabel("Fraction of vertices with degree k")
        plt.show()

    def _plot_eigenvalue_centralities(self):
        """Plots the eigenvalue centralities"""
        plot = sns.histplot(self.eigenvalue_centralities, bins=10)
        plot.set_yscale("log")
        plot.set_xlabel("eigenvalue centralities")
        plot.set_ylabel("Count")
        plt.show()

    def _plot_clustering_coefficients(self):
        """Plots the clustering coefficients"""
        plot = sns.histplot(self.clustering_coefficients, bins=10)
        plot.set_yscale("log")
        plot.set_xlabel("clustering coefficients")
        plot.set_ylabel("Count")
        plt.show()

    def _plot_degree_centralities(self):
        """Plots the clustering coefficients"""
        plot = sns.histplot(self.degree_centralities, bins=10)
        plot.set_yscale("log")
        plot.set_xlabel("clustering coefficients")
        plot.set_ylabel("Count")
        plt.show()


if __name__ == "__main__":
    start = time.time()

    x = Analyzer("data/power.gml")
    x.run()
    # x.plot_and_print()

    duration = time.time() - start
    print(f"duration: {duration:.3g}s")
