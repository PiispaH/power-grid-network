import networkx as nx


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
