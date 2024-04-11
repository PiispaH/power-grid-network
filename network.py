from pprint import pprint
from itertools import combinations

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class Network:
    """This class represents a network in dict as well as matrix form"""

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

    def run(self):
        print(f"Mean degree: {self.calc_mean_degree():.3g}")

        a = self.calc_degree_distribution()
        self.plot_degree_distribution(a)

        # n = 10
        # a = self.calc_paths_of_len_n(n)
        # for n in range(n-1):
        #     print(f"Paths of lenght {n + 2}: {a[n]}")

    def calc_mean_degree(self):
        sum = 0
        for i in self.graph:
            sum += len(self.graph[i])
        return 2 * sum / len(self.graph)

    def calc_degree_distribution(self):
        degrees = {}
        for i in self.graph:
            degree = len(self.graph[i])
            if degree not in degrees:
                degrees[degree] = 0
            degrees[degree] += 1
        return {key: value / self.nodes for key, value in degrees.items()}

    def plot_degree_distribution(self, distr: dict):
        plot = sns.barplot(distr)
        # plot.set_yscale("log")
        plot.set_xlabel("degree k")
        plot.set_ylabel("Fraction of vertices with degree k")
        plt.show()

    def calc_paths_of_len_n(self, n: int):
        lens = []

        adj = self.graph_as_matrix
        matrix = adj
        for _ in range(n-1):
            matrix = matrix @ adj
            jou = 0
            for x, y in combinations(range(4941), 2):
                jou += matrix[x][y]
            lens.append(int(jou))
        return lens


if __name__ == "__main__":
    Analyzer("data/power.gml").run()
