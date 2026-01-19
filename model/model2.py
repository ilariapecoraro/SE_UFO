from database.dao2 import DAO
import networkx as nx
from geopy import distance

class Model:
    def __init__(self):
        self.list_sighting = []
        self.list_states = []

        self.G = nx.Graph()
        self._nodes = []
        self._edges = []
        self.id_map = {}
        self.sol_best = 0

        self.path = []
        self.path_edge = []

        self.load_sighting()
        self.load_states()

    def load_sighting(self):
        self.list_sighting = DAO.get_all_sighting()

    def load_states(self):
        self.list_states = DAO.get_all_states()

    def get_shapes(self, selected_year):
        return DAO.get_all_shapes(selected_year)

    def build_graph(self, s, a):
        self.G.clear()
        print(a, s)

        for p in self.list_states:
            self._nodes.append(p)

        self.G.add_nodes_from(self._nodes)
        self.id_map = {}
        for n in self._nodes:
            self.id_map[n.id] = n

        tmp_edges = DAO.get_all_weighted_neigh(a, s)

        self._edges.clear()
        for e in tmp_edges:
            self._edges.append((self.id_map[e[0]], self.id_map[e[1]], e[2]))

        self.G.add_weighted_edges_from(self._edges)

    def get_sum_weight_per_node(self):
        pp = []
        for n in self.G.nodes():
            sum_w = 0
            for e in self.G.edges(n, data=True):
                sum_w += e[2]['weight']
            pp.append((n.id, sum_w))
        return pp

    def compute_path(self):
        self.path = []
        self.path_edge = []
        self.sol_best = 0

        partial = []
        for n in self.get_nodes():
            partial.clear()
            partial.append(n)
            self._ricorsione(partial, [])

    def _ricorsione(self, partial, partial_edge):
        n_last = partial[-1]

        neighbors = self.get_admissible_neighbs(n_last, partial_edge)

        if len(neighbors) == 0:
            weight_path = self.compute_weight_path(partial_edge)
            if weight_path > self.sol_best:
                self.sol_best = weight_path + 0.0
                self.path = partial[:]
                self.path_edge = partial_edge[:]
            return

        for n in neighbors:
            partial_edge.append((n_last, n, self.G.get_edge_data(n_last, n)['weight']))
            partial.append(n)

            self._ricorsione(partial, partial_edge)

            partial.pop()
            partial_edge.pop()

    def get_admissible_neighbs(self, n_last, partial_edges):
        all_neigh = self.G.edges(n_last, data=True)
        result = []
        for e in all_neigh:
            if len(partial_edges) != 0:
                if e[2]["weight"] > partial_edges[-1][2]:
                    result.append(e[1])
            else:
                result.append(e[1])
        return result

    def compute_weight_path(self, mylist):
        weight = 0
        for e in mylist:
            weight += distance.geodesic((e[0].lat, e[0].lng),
                                        (e[1].lat, e[1].lng)).km
        return weight

    def get_distance_weight(self, e):
        return distance.geodesic((e[0].lat, e[0].lng),
                                 (e[1].lat, e[1].lng)).km

    def get_nodes(self):
        return self.G.nodes()

    def get_edges(self):
        return list(self.G.edges(data=True))

    def get_num_of_nodes(self):
        return self.G.number_of_nodes()

    def get_num_of_edges(self):
        return self.G.number_of_edges()