import networkx as nx

from dfs import dfs
from dfs import get_topological_order
from dfs import clear_topological_order



#Aggiorna il numero di vertici scoperti solamente se non erano stati ancora
#effettivamente scoperti. Sottrae quindi uno al valore totale e restituisce
#il valore.

def update_covered_node(node :str, grafo : nx.DiGraph, to_be_covered: int) -> int:

    if grafo.nodes[node]['m'] == 1:

        grafo.nodes[node]['m'] = 0
        to_be_covered -= 1
        
        return to_be_covered

    else:

        return to_be_covered



#Algoritmo che calcola la path cover iniziale restituendola in una lista.

def path_cover(graph : nx.DiGraph) -> list:

    #Variabile che serve per contare i vertici ancora da scoprire, termino 
    #quando gli ho scoperti tutti

    to_be_covered = graph.number_of_nodes()
    cover = list()
    temp_cover = list()

    while to_be_covered > 0:

        #Calcolo l'ordinamento topologico per iniziare ad inserire
        #nella cover la sorgente segnangola successivamente come coperta.
        
        #Definisco inoltre un indice per spostarmi direttamente al nodo 
        #massimo tra ogni predecessore.

        dfs(True, graph)
        topological_index = 0
        topological_order = get_topological_order()
        temp_cover.append(topological_order[0])
        to_be_covered = update_covered_node(topological_order[0], graph, to_be_covered)
        inspected_node = topological_order[topological_index]

        #Attraverso l'ordinamento topologico selezionando il massimo tra
        #ogni predecessore (guardando la lista di adiacenza). Posso eseguire 
        #questa operazione solamente se il nodo ispezionato ha una lista di 
        #adiacenza.

        while not (not list(graph.successors(inspected_node))):

            max = -1
            max_node = ""

            for w in list(graph.successors(inspected_node)):

                if graph.nodes[w]['u'] > max:

                    max = graph.nodes[w]['u']
                    max_node = w


            #Una volta trovato il massimo lo segno come preso m[x] = 0 e lo
            #aggiungo alla copertura, spostandomi successivamente 
            #sull'elemento massimo appena trovato.

            to_be_covered = update_covered_node(max_node, graph, to_be_covered)
            temp_cover.append(max_node)
            graph[inspected_node][max_node]['flow'] += 1
            topological_index = topological_order.index(max_node)
            inspected_node = topological_order[topological_index]

           
        cover.append(temp_cover.copy())
        temp_cover.clear()
        topological_order.clear()
        clear_topological_order()

    return cover
        


