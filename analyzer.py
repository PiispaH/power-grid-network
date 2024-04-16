#
# Simple "analysis" of some power grid network in the united states
#

import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

from network import Network
from sabotage import Sabotage


class Analyzer(Network):
    """This class analyzes a network"""

    def __init__(self, filepath: str):
        super().__init__(filepath)
        self.mean_degree = 0
        self.degree_distribution = []
        self.eigenvalue_centralities = {}
        self.degree_centralities = {}
        self.katz_centralities = {}
        self.clustering_coefficients = []

    def run(self):
        """Runs the simulation"""
        degrees = dict(self.network.degree())
        self.mean_degree = sum(degrees.values()) / len(degrees)
        self.clustering_coefficients = nx.clustering(self.network)
        self.degree_distribution = self._calc_degree_distribution()
        self.degree_centralities = nx.degree_centrality(self.network)
        self.eigenvalue_centralities = nx.eigenvector_centrality(self.network)
        self.katz_centralities = nx.katz_centrality(self.network)

        self._simulate_sabotage(0.05)
        self._simulate_sabotage(0.10)

    def _simulate_sabotage(self, fraction: float):
        """Sabotages the network based on three different metrics"""
        print(f"\n{'='.center(34, '=')}", end="")
        print(f"\nResults for {fraction:.2f} vertices removed:")
        print(f"{'='.center(34, '=')}")

        print("Degree centrality:")
        hurricane = Sabotage(self.network, self.degree_centralities)
        sabotaged_network = hurricane.destroy_vertices(fraction=fraction)
        print("Components:", nx.number_connected_components(sabotaged_network))
        sizes_of_components = list(len(i) for i in sorted(nx.connected_components(sabotaged_network), key=len, reverse=True))[1:]
        print("Average size:", sum(sizes_of_components)/len(sizes_of_components))
        print()

        print("Katz centrality:")
        hurricane = Sabotage(self.network, self.katz_centralities)
        sabotaged_network = hurricane.destroy_vertices(fraction=fraction)
        print("Components:", nx.number_connected_components(sabotaged_network))
        sizes_of_components = list(len(i) for i in sorted(nx.connected_components(sabotaged_network), key=len, reverse=True))[1:]
        print("Average size:", sum(sizes_of_components)/len(sizes_of_components))
        print()

        print("Eigenvalue centrality:")
        hurricane = Sabotage(self.network, self.eigenvalue_centralities)
        sabotaged_network = hurricane.destroy_vertices(fraction=fraction)
        print("Components:", nx.number_connected_components(sabotaged_network))
        sizes_of_components = list(len(i) for i in sorted(nx.connected_components(sabotaged_network), key=len, reverse=True))[1:]
        print("Average size:", sum(sizes_of_components)/len(sizes_of_components))

    def plot_and_print(self):
        """Prints the data and plots the graphs"""
        print(f"Mean degree: {self.mean_degree:.3g}\n")
        self._plot_degree_distribution()
        self._plot_eigenvalue_centralities()
        self._plot_clustering_coefficients()
        self._plot_degree_centralities()
        self._plot_katz_centralities()

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

    def _plot_degree_distribution(self):
        """Plots the degree distribution"""
        plot = sns.barplot(self.degree_distribution)
        plot.set_xlabel("degree k")
        plot.set_ylabel("Fraction of vertices with degree k")
        plot.set_title("Degree distribution")
        plt.show()

    def _plot_clustering_coefficients(self):
        """Plots the clustering coefficients"""
        plot = sns.histplot(self.clustering_coefficients, bins=10)
        plot.set_yscale("log")
        plot.set_xlabel("Coefficient")
        plot.set_ylabel("Count")
        plot.set_title("clustering coefficients")
        plt.show()

    def _plot_eigenvalue_centralities(self):
        """Plots the eigenvalue centralities"""
        plot = sns.histplot(self.eigenvalue_centralities, bins=10)
        plot.set_yscale("log")
        plot.set_xlabel("centrality")
        plot.set_ylabel("Count")
        plot.set_title("Eigenvalue centralities")
        plt.show()

    def _plot_degree_centralities(self):
        """Plots the clustering coefficients"""
        plot = sns.histplot(self.degree_centralities, bins=10)
        plot.set_yscale("log")
        plot.set_xlabel("Centrality")
        plot.set_ylabel("Count")
        plot.set_title("Degree centralities")
        plt.show()

    def _plot_katz_centralities(self):
        """Plots the eigenvalue centralities"""
        plot = sns.histplot(self.katz_centralities, bins=10)
        plot.set_yscale("log")
        plot.set_xlabel("centrality")
        plot.set_ylabel("Count")
        plot.set_title("Katz centralities")
        plt.show()
