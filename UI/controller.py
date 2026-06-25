import flet as ft
import networkx as nx

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDsRating(self):
        possible_values = DAO.load_selectable_values()
        dd1: ft.Dropdown = self._view._ddrating1
        dd2: ft.Dropdown = self._view._ddrating2

        dd1.options = [
           ft.dropdown.Option(key=str(v), text=str(v)) for v in possible_values
        ]
        dd2.options = [
            ft.dropdown.Option(key=str(v), text=str(v)) for v in possible_values
        ]

    def handleCreaGrafo(self, e):
        min_r = self._view._ddrating1.value
        max_r = self._view._ddrating2.value

        if min_r is None or max_r is None:
            self._view.create_alert("Selezionare un intervallo di rating")
            return

        m = float(min_r)
        M = float(max_r)

        if m > M:
            self._view.create_alert("Il primo deve essere minore del secondo")

        self._model.create_graph(m, M)
        txt_result: ft.ListView = self._view.txt_result
        graph: nx.Graph = self._model.graph

        txt_result.controls = [
            ft.Text("Creazione grafo avvenuta con successo. "),
            ft.Text(f"Grafo con {graph.number_of_nodes()} nodi e {graph.number_of_edges()} archi. ")
        ]

        edges = sorted(graph.edges(data=True), key = lambda edge: edge[2]["weight"], reverse=True)[0:5]
        for edge in edges:
            txt_result.controls.append(ft.Text(f"{edge[0].name} -> {edge[1].name} con peso {edge[2]["weight"]}"))

        txt_result.controls.append(ft.Text(f"Numero di componenti connesse: {nx.number_connected_components(graph)}"))

        c_comps = max(nx.connected_components(graph), key=len)
        sub_graph = graph.subgraph(c_comps).copy()
        txt_result.controls.append(ft.Text(f"La componente connessa più grande ha {sub_graph.number_of_nodes()} nodi"))
        for node in sub_graph:
            txt_result.controls.append(ft.Text(node.name))

        self._view.update_page()

    def handleCammino(self, e):
        pass