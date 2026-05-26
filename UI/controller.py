import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def fillDDsRating(self):
        ratings = self._model.getRatings()
        for voto in ratings:
            self._view._ddrating1.options.append(ft.dropdown.Option(voto))
            self._view._ddrating2.options.append(ft.dropdown.Option(voto))
        self._view.update_page()


    def handleCreaGrafo(self,e):
        self._model.buildGraph(self._view._ddrating1.value, self._view._ddrating2.value)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi:{self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi:{self._model.getNumEdges()}"))

        topEdges = self._model.getTop5Edges()

        self._view.txt_result.controls.append(ft.Text("Top 5 archi:"))

        for u, v, data in topEdges:
            self._view.txt_result.controls.append(
                ft.Text(f"{u.Name} -> {v.Name} : {data['weight']}"))

        self._view.update_page()

        components, largest = self._model.getConnectedComponents()

        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {len(components)} componenti connesse"))

        self._view.txt_result.controls.append(ft.Text(f"La più grande componente connessa è lunga {len(largest)}:"))

        for u in largest:
            self._view.txt_result.controls.append(
                ft.Text(f"{u.Name}"))

        self._view.update_page()

    def handleCammino(self,e):
        bestPath = self._model.getBestPath()
        self._view.txt_result.controls.append(ft.Text(f"Cammino massimo trovato ({len(bestPath)} nodi):"))

        for a in bestPath:
            self._view.txt_result.controls.append(ft.Text(a.Name))

        self._view.update_page()