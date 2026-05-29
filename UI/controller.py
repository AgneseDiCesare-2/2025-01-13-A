import flet as ft
from UI.view import View
from model.model import Model


class Controller:

    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._localization = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        if self._localization is None or self._localization=="":
            self._view.txt_result.controls.append(ft.Text("Seleziona una localizzazione per proseguire!", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(self._localization)
        self._view.txt_result.controls.append(ft.Text(f"Creato grafo con {self._model.num_nodi()} nodi e {self._model.num_archi()} archi. "))
        archi=self._model.get_archi_ordinati()
        for arco in archi:
            self._view.txt_result.controls.append(ft.Text(f"{arco[0].GeneID} <--> {arco[1].GeneID}: peso {arco[2]["weight"]}"))
        self._view.update_page()
        return

    def analyze_graph(self, e):
        connesse=self._model.componenti_connesse()
        self._view.txt_result.controls.append(ft.Text(f"Le componenti connesse sono: "))
        for c in connesse:
            stringa=""
            for n in c:
                stringa+=str(n)+","
            self._view.txt_result.controls.append(ft.Text(f"{stringa[:-1]} | dimensione componente={len(c)}"))
        self._view.update_page()
        return

    def handle_path(self, e):
        self._view.txt_result.controls.append(ft.Text("Cammino Migliore (Ricorsione): "))
        best_solution=self._model.handle_ricorsione()
        for nodo in best_solution:
            self._view.txt_result.controls.append(ft.Text(str(nodo)))
        self._view.update_page()
        return


    def fillDD(self):
        aeroporti = self._model.getLocalizations()
        for n in aeroporti:
            self._view.dd_localization.options.append(
                ft.dropdown.Option(key=n, data=n, on_click=self.getAirArrivo)
            )
        self._view.update_page()
        pass

    def getAirArrivo(self, e):
        selected_key = e.control.data
        self._localization = selected_key
        return

