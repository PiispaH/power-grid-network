from pprint import pprint
from itertools import combinations
import time

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

PATHS_UP_TO_N = 5  # Determines up to what path lenght the amount of paths are calculated


class Network:
    """This class represents a network in dict as well as in matrix form"""

    def __init__(self, filepath: str):
        self._load_graph(filepath)
        if not self.graph:
            raise Exception("Something bad happened when loading the graph...")
        self.graph_as_matrix = nx.to_numpy_array(self.nx_graph)
        self.nodes = self.nx_graph.number_of_nodes()
        self.edges = self.nx_graph.number_of_edges()


    def _load_graph(self, filepath: str):
        self.nx_graph = nx.read_gml(filepath, label=None)

        self.graph = {key: {x for x in value} for key, value in nx.to_dict_of_dicts(self.nx_graph).items()}


class Analyzer(Network):
    """This class analyzes a network"""

    def __init__(self, filepath: str):
        super().__init__(filepath)
        self.mean_degree = 0
        self.degree_distribution = []
        self.paths_of_len_n = []
        self.eigenvalue_centralities = {}
        self.clustering_coefficients = []

    def run(self):
        # self.mean_degree = self._calc_mean_degree()
        # self.degree_distribution = self._calc_degree_distribution()
        # self.paths_of_len_n = self._calc_paths_of_len_n(PATHS_UP_TO_N)
        
        # self.eigenvalue_centrality = nx.eigenvector_centrality(self.nx_graph)
        # Tai jos tän saa toimimaan...
        # self.eigenvalue_centrality = self._eigenvalue_centrality()

        self.clustering_coefficients = self._calc_clustering_coefficients()
        print(self.clustering_coefficients)


    def plot_and_print(self):
        # Mean degree
        print(f"Mean degree: {self.mean_degree:.3g}\n")
        
        # Degree distribution
        self._plot_degree_distribution()

        # Paths of length n
        for n in range(PATHS_UP_TO_N-1):
            print(f"Paths of lenght {n + 2}: {self.paths_of_len_n[n]}")
        
        # Eigenvalue centrality
        plt.plot(self.eigenvalue_centrality.keys(), self.eigenvalue_centrality.values())
        plt.show()

    def _calc_clustering_coefficients(self):
        """Calculates the individual clustering coefficients for each node"""
        coeffs = []
        for i in self.graph:
            conn_neighs = 0
            neighbors = self.graph[i]
            neigh_pairs = 0.5 * len(neighbors) * (len(neighbors) - 1)
            for neigh in neighbors:
                for pair in neighbors:
                    if neigh == pair:
                        continue
                    if neigh in self.graph[pair]:
                        conn_neighs += 1
            if neigh_pairs:
                coeffs.append(conn_neighs / neigh_pairs)
            else:
                coeffs.append(-1)
        return coeffs

    def _eigenvalue_centrality(self):
        eigenvalues, eigenvectors = np.linalg.eig(self.graph_as_matrix)
        return eigenvectors[np.argmax(eigenvalues)]

    def _calc_mean_degree(self):
        """Calculates the mean degree of the network"""
        sum = 0
        for i in self.graph:
            sum += len(self.graph[i])
        return 2 * sum / len(self.graph)

    def _calc_degree_distribution(self):
        """Caclulates the degree distribution of the network"""
        degrees = {}
        for i in self.graph:
            degree = len(self.graph[i])
            if degree not in degrees:
                degrees[degree] = 0
            degrees[degree] += 1
        return {key: value / self.nodes for key, value in degrees.items()}

    def _plot_degree_distribution(self):
        """Plots the degree distribution"""
        plot = sns.barplot(self.degree_distribution)
        # plot.set_yscale("log")
        plot.set_xlabel("degree k")
        plot.set_ylabel("Fraction of vertices with degree k")
        plt.show()

    def _calc_paths_of_len_n(self, n: int):
        """Caclulates paths of up to n edges long"""
        lengths = []
        adj = self.graph_as_matrix
        matrix = adj
        for _ in range(n-1):
            matrix = matrix @ adj
            paths = 0
            for x, y in combinations(range(self.nodes), 2):
                paths += matrix[x][y]
            lengths.append(int(paths))
        return lengths


if __name__ == "__main__":
    PATHS_UP_TO_N = 10

    start = time.time()

    x = Analyzer("data/power.gml")
    x.run()
    # x.plot_and_print()

    duration = time.time() - start
    print(f"duration: {duration:.3g}s")
