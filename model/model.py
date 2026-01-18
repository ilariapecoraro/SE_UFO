import copy

from networkx.classes import neighbors
from geopy import distance

from copy import deepcopy
from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.dict_states = {}  # dizionario degli states {id: state}
        self.lista_state = []  # lista degli oggetti state
        self.connessioni = []  # lista di tuple (id1, id2, weight)
        self.all_years = []
        self.all_shapes = []

        # Per la ricorsione
        self._max_weight = 0
        self.soluzione_best = []

    def get_all_years(self):
        self.all_years = DAO.get_all_years()

    def get_all_shapes(self, year):
        self.all_shapes= DAO.get_all_shapes(year)

    def get_all_states(self, year, shape):
        self.lista_state = DAO.get_all_states()

        for s in self.lista_state:
            if s.id not in self.dict_states:
                self.dict_states[s.id] = s

    def get_connessioni(self, year, shape):
        self.connessioni = DAO.get_connection(year, shape)

    def build_graph(self, year, shape):
        """
        Costruisce il grafo (self.G) pesato
         dei team considerando solo le connessioni di anno e di forma selezionati
        Quindi il grafo avrà solo i nodi che appartengono almeno ad una connessione
        """

        # Pulisco il grafo e lo ricreo
        self.G.clear()
        self.dict_states = {}
        self.lista_state = []
        self.connessioni = []

        self.get_all_states(year, shape)

        # prendo le connessioni
        self.get_connessioni(year, shape)

        # aggiungo gli archi
        self.G.add_nodes_from(self.lista_state)

        # seleziono gli oggetti e il peso
        for s1_id, s2_id, peso in self.connessioni:
            if s1_id in self.dict_states and s2_id in self.dict_states:
                s1 = self.dict_states[s1_id]
                s2 = self.dict_states[s2_id]

                # aggiungi l'arco con l'attributo
                self.G.add_edge(s1, s2, weight=peso)

        print(self.G)

    def get_num_of_nodes(self):
        return self.G.number_of_nodes()

    def get_num_of_edges(self):
        return self.G.number_of_edges()

    def ricerca_cammino(self):

        self.best_path = []
        self.max_weight = 0

        for u in self.G.nodes():
            partial = [u]
            partial_edges = []
            self.ricorsione(partial, partial_edges, u, 0)

        return self.max_weight, self.best_path

    def ricorsione(self, partial_nodes, partial_edges, u, last_weight):

        weight_path = self.compute_weight_path(partial_edges)
        if weight_path > self.max_weight:
            self.best_path = copy.deepcopy(partial_edges)
            self.max_weight = weight_path

        neigh = self._get_admissible_neighbors(u, partial_nodes, last_weight)
        if not neigh:
            return

        for n, peso in neigh:
            print("...")
            partial_nodes.append(n)
            partial_edges.append((u, n, self.G.get_edge_data(u, n)))
            self.ricorsione(partial_nodes, partial_edges, n, peso)
            partial_nodes.pop()
            partial_edges.pop()

    def _get_admissible_neighbors(self, node, partial_nodes, last_weight):
        result = []
        for v, peso in self.get_vicino(node):
            if v in partial_nodes:
                continue
            if peso < last_weight:
                continue
            result.append((v,peso))
        return result

    def compute_weight_path(self, mylist):
        weight = 0
        for e in mylist:
            weight += e[2]['weight']
        return weight

    def compute_distanza(self, n1, n2):
        d = distance.geodesic((n1.lng, n2.lng), (n1.lat, n2.lat)).km
        return d

    def get_vicino(self, node):

        neigh = []
        if node in self.G.nodes():
            for neighbor in self.G.neighbors(node):
                attr = self.G.get_edge_data(node, neighbor)
                if attr:
                    peso = attr.get("weight")
                    neigh.append((neighbor, peso))
        neigh_ordinati = sorted(neigh, key=lambda x: x[1], reverse = True)
        return neigh_ordinati
