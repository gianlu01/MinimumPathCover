import networkx as nx

from graph import reset_predecessor



topological_order = list()



#Dato che devo riutilizzare questo algoritmo per Ford_Fulkerson, devo poter
#escludere il calcolo di m[v] e u[v] quando necessario tramite il valore 
#booleano path_cover che mi permette di dire di calcolarla (True) o non
#calcolarla (False).

def dfs(path_cover : bool, graph : nx.DiGraph) -> None:

    #Imposto bianchi tutti i vertici.
    if path_cover:

        reset_colors(graph)

    for node in graph.nodes():

        if graph.nodes[node]['color'] == 1:

            dfs_visit_cover(node, graph)



def dfs_visit_cover(node: str, graph : nx.DiGraph) -> None:

    #Se una lista di adiancenza è vuota (non ha successori)
  
    if not list(graph.successors(node)):

        graph.nodes[node]['u'] = graph.nodes[node]['m']

    else:

        max = -1
        max_node = ""

        for neigh in list(graph.successors(node)):

            if graph.nodes[neigh]['color'] == 1:

                print("")

                dfs_visit_cover(neigh, graph)

            if graph.nodes[neigh]['u'] > max:

                max = graph.nodes[neigh]['u']
                max_node = neigh

        graph.nodes[node]['u'] = graph.nodes[node]['m'] + graph.nodes[max_node]['u']
        

    graph.nodes[node]['color'] = 0
    topological_order.insert(0, node)



def get_topological_order() -> list:

    return topological_order.copy()



def clear_topological_order() -> None:

    topological_order.clear()


#Visita in profondità utilizzata nel calcolo del flusso tramite l'algoritmo di
#Ford-Fulkerson. Serve a riempire il dizionario dei predecessori

def dfs_visit_flow(node: str, graph : nx.DiGraph) -> None:

    graph.nodes[node]['color'] = 2 #Imposto a grigio il colore, nodo scoperto    

    for neigh in list(graph.successors(node)):

        if graph.nodes[neigh]['color'] == 1:

            graph.nodes[neigh]['predecessor'] = node
            dfs_visit_flow(neigh, graph)

    graph.nodes[node]['color'] = 0
        
        

#Estrae il cammino aumentante dal dizionario dei predecessori

def get_dfs_path(sink : str, grafo : nx.DiGraph) -> list | None:

    if grafo.nodes[sink]['predecessor'] is None:

        return None
    
    else:

        predecessor_path = list()

        while grafo.nodes[sink]['predecessor'] is not None:

            predecessor_path.insert(0, sink)
            sink = grafo.nodes[sink]['predecessor']

        predecessor_path.insert(0, sink)
        reset_predecessor(grafo)
        
        return predecessor_path



#Reimposta tutti i colori a bianco

def reset_colors(grafo : nx.DiGraph):
    
    for nodo in grafo.nodes():

        grafo.nodes[nodo]['color'] = 1