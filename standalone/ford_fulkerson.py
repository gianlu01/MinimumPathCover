import networkx as nx

from copy import deepcopy
from dfs import reset_colors
from dfs import dfs_visit_flow_recursive
from dfs import get_dfs_path
from graph import reset_flow
from sys import maxsize



def ford_fulkerson(graph : nx.DiGraph, cover : list) -> list:

    residual_graph = deepcopy(graph)
    max_flow = deepcopy(graph)
    source = next((n for n in graph.nodes if graph.in_degree(n) == 0), None)
    sink  = next((n for n in graph.nodes if graph.out_degree(n) == 0), None)

    #Per prima cosa inizializzo i colori per la DFS, non utilizzo la procedura
    #già presente nella DFS perchè quella serve per la path cover. In questo
    #caso i colori vengono modificati man mano dal calcolo del grafo residuo
    #e devono rimanere modificati così per il corretto calcolo di un cammino
    #aumentante e non inizializzati ogni volta a 1.
    
    reset_colors(residual_graph)
    reset_flow(max_flow)

    for u, v in graph.edges():

        #c = f(e) - d(e) (per ciascun arco) flusso - domanda

        residual_graph[u][v]['flow'] -= residual_graph[u][v]['demand'] 

        #Come detto in precedenza, scarto tutti i valori <= 0 e provvedo già 
        #ad inizializzare i valori per la DFS "scartando" i nodi che non 
        #possono più essere attraversati. Dato che un nodo con valore 0
        #non può più essere attraversato, significa anche che non può
        #ne più essere raggiunto ne collegarsi ad altri nodi in quanto
        #privo di capacità residua. Provvedo quindi ad impostare a 0 il 
        #colore di questo nodo (-, +) per escluderlo dalla DFS.

        if residual_graph[u][v]['flow'] <= 0:

            residual_graph.remove_edge(u, v)


    #Una volta trovata la rete residua, procedo a trovare un cammino aumentante
    #dalla sorgente alla destinazione tramite una visita in profondità. Il
    #cammino aumentante sarà dato proprio dall'ordinamento topologico T come
    #nella path cover.  

    dfs_visit_flow_recursive(source, residual_graph)
    predecessor_path = get_dfs_path(sink, residual_graph)

    #Una volta che ho trovato il cammino aumentante procedo a trovare il valore
    #minimo (bottleneck) e sottrarlo al dal flusso. Il cammino aumentante
    #ci permette di migliorare l'approssimazione della path cover. Proseguo
    #finché non trovo più cammini aumentanti.

    while predecessor_path:

        if not(predecessor_path[0] == source and predecessor_path[len(predecessor_path) - 1] == sink):

            break

        else:

            print("Cammino aumentante:")
            print(predecessor_path)

            index = 0
            bottleneck = maxsize

            #Calcolo il bottleneck (minimo del cammino aumentante)

            while index < len(predecessor_path) - 1:

                u = predecessor_path[index]
                v = predecessor_path[index+1]

                if residual_graph[u][v]['flow'] < bottleneck:

                    bottleneck = residual_graph[u][v]['flow']

                index += 1

            index = 0

            while index < len(predecessor_path) - 1:

                u = predecessor_path[index]
                v = predecessor_path[index+1]
                residual_graph[u][v]['flow'] -= bottleneck

                #Controllo se esiste l'arco inverso

                if residual_graph.has_edge(v, u):
                    
                    residual_graph[v][u]['flow'] += bottleneck

                else:

                    attr = residual_graph.get_edge_data(u, v)
                    residual_graph.add_edge(v, u, **attr)

                #Rimuovo gli archi nulli dalla rete residua.
                
                if residual_graph[u][v]['flow'] <= 0:

                    residual_graph.remove_edge(u, v)

                if residual_graph[v][u]['flow'] == 0:
            
                    residual_graph.remove_edge(v, u)

                #Sommo il bottleneck al MAX_FLOW
                max_flow[u][v]['flow'] += bottleneck
                index += 1

            print("Path Cover ridotta")

            predecessor_path.clear()
            reset_colors(residual_graph)
            dfs_visit_flow_recursive(source, residual_graph)
            predecessor_path = get_dfs_path(sink, residual_graph)


    print("Nessun percorso disponibile")
   
    #Una volta che non trovo più cammini aumentanti posso procedere a calcolare
    #la path cover finale, ovvero il path_flow - max_flow

    for u, v in max_flow.edges():

        graph[u][v]['flow'] -= max_flow[u][v]['flow']

        #Cancello gli archi nulli

        if graph[u][v]['flow'] == 0:

            graph.remove_edge(u, v)

    #Ora che ho in mano il flusso finale, procedo ad effettuare delle visite
    #in profondità per estrarre la cover finale. Ogni volta che estraggo un
    #percorso procedo a sottrarre quel percorso dal flusso attuale in modo
    #tale da poter successivamente cancellare tutti gli archi che hanno
    #capacità 0. 

    #Procedo a svuotare la COVER

    #Faccio una copia del PATH FLOW per tenere salvati i valori sugli archi
    #in modo tale da poterli visualizzare nella stampa del grafo

    cover.clear()
    min_flow = deepcopy(graph)
    reset_colors(min_flow)
    dfs_visit_flow_recursive(source, min_flow)
    predecessor_path = get_dfs_path(sink, min_flow)

    while predecessor_path:

        if not(predecessor_path[0] == source and predecessor_path[len(predecessor_path) - 1] == sink):

            break

        else:

            index = 0
            
            while index < len(predecessor_path) - 1:

                u = predecessor_path[index]
                v = predecessor_path[index + 1]
                graph[u][v]['flow'] -= 1
                index += 1

            for u, v in max_flow.edges:

                if (u, v) in graph.edges and graph[u][v]['flow'] <= 0:

                    graph.remove_edge(u, v)

            min_flow = deepcopy(graph)
            cover.append(predecessor_path.copy())
            predecessor_path.clear()

            if min_flow.number_of_edges() > 0:

                reset_colors(min_flow)
                dfs_visit_flow_recursive(source, min_flow)
                predecessor_path = get_dfs_path(sink, min_flow)

            else:

                break
            
    
    return cover