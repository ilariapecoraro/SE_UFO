import flet as ft
from geopy import distance


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        # funzione che riempie la dropdown degli anni
        self._model.get_all_years()
        self._view.dd_year.options = [ft.dropdown.Option(str(y)) for y in self._model.all_years]


    def handle_year_change(self,e):
        """ Aggiorna il dropdown delle forme quando cambia anno"""
        year = self._view.dd_year.value

        if year is None:
            self._view.show_allert("Seleziona un anno")
            self._view.dd_shape.options = []
            return

        try:
            year = int(year)
        except ValueError:
            self._view.show_allert("anno non valido")
            self._view.dd_shape.options = []
            return

        # Recupero le forme
        self._model.get_all_shapes(year)
        self._view.dd_shape.options = [ft.dropdown.Option(str(y)) for y in self._model.all_shapes]
        self._view.dd_shape.update()



    def handle_graph(self,e):
        """ Handler per gestire creazione del grafo """
        try:
            year = int(self._view.dd_year.value)
        except ValueError:
            self._view.show_allert("Anno non valido")
            return
        try:
            shape = str(self._view.dd_shape.value)
        except ValueError:
            self._view.show_allert("forma non valido")
            return
        self._model.build_graph(year, shape)

        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f"Numero di vertici: {self._model.get_num_of_nodes()}, Numero di archi: {self._model.get_num_of_edges()}"))
        for u, v, attr in self._model.G.edges(data=True):
            if attr['weight'] is None:
                attr['weight'] = 0
            self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Nodo {u}{v} Peso dell'arco: {attr['weight']}"))

        self._view.update()

    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
        # ricerca cammino massimo
        self._model.ricerca_cammino()

        # pulizia dell'output
        self._view.lista_visualizzazione_2.controls.clear()

        # stampa il peso totale
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Peso Totale: {self._model.max_weight}"))

        # stampa cammino trovato
        for nodo_1, nodo_2, attr in self._model.best_path:
            distanza = distance.geodesic((nodo_1.lat, nodo_1.lng), (nodo_2.lat, nodo_2.lng)).km
            self._view.lista_visualizzazione_2.controls.append(ft.Text(
                f"{nodo_1} --> {nodo_2}: {distanza}"))

        self._view.update()
