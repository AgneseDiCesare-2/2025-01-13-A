import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo=nx.Graph() #grafo semplice e pesato
        self._idMap={}

    def getLocalizations(self):
        return DAO.getLocalization()

    def buildGraph(self, localization):
        self._grafo.clear()
        self._idMap = {}

        nodi=DAO.getNodi(localization)
        self._grafo.add_nodes_from(nodi)

        for n in nodi:
            self._idMap[n.GeneID]=n
        print(len(self._grafo.nodes))

        archi=DAO.getArchi()

        for tupla in archi:
            if tupla[0] in self._idMap.keys() and tupla[1] in self._idMap.keys():
                nodo1=self._idMap[tupla[0]]
                nodo2=self._idMap[tupla[1]]
                peso=tupla[2]

                self._grafo.add_edge(nodo1,nodo2, weight=peso)
        return

    def num_nodi(self):
        return len(self._grafo.nodes)

    def num_archi(self):
        return len(self._grafo.edges)

    def get_archi_ordinati(self):
        edges = list(self._grafo.edges(data=True)) #lista di tuple (nodo1, nodo2, weight: peso)
        edges_ordinati=sorted(edges, key=lambda x: x[2]["weight"])
        return edges_ordinati

    def componenti_connesse(self):
        connesse=list(nx.connected_components(self._grafo))
        result=[]
        for connessa in connesse:
            if len(connessa)>1:
                result.append(connessa)
        result_ordered = sorted(result, key=len, reverse=True)
        return result_ordered #lista di tuple (spero)

    def handle_ricorsione(self):
        self._bestSoluzione=[]
        self._max=0

        for nodo in self._grafo.nodes:
            self.ricorsione([nodo])
        return self._bestSoluzione

    def ricorsione(self, parziale):
        #condizione terminale
        #condizione ottimale:
        if len(parziale)>self._max:
            self._max=len(parziale)
            self._bestSoluzione=copy.deepcopy(parziale)

        elif len(parziale)==self._max:
            if len(nx.subgraph(self._grafo, parziale)) < len(nx.subgraph(self._grafo, self._bestSoluzione)):
                self._max = len(parziale)
                self._bestSoluzione = copy.deepcopy(parziale)

        #?chiede un cammino o un sottoinsieme generico di nodi (anche se non connessi da un arco?)
        for nodo in nx.neighbors(self._grafo, parziale[-1]):
            if nodo not in parziale and self.checkValidity(nodo, parziale):
                parziale.append(nodo)
                self.ricorsione(parziale)
                parziale.pop()

    def checkValidity(self, nodo, parziale):
        if nodo.GeneID>parziale[-1].GeneID and nodo.Essential==parziale[-1].Essential:
            return True
        return False