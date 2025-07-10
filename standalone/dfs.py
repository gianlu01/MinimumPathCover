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

            dfs_visit_cover_iterative(node, graph)



def dfs_visit_cover(node: str, graph : nx.DiGraph) -> None:

    #Se una lista di adiancenza è vuota (non ha successori)
  
    if not list(graph.successors(node)):

        graph.nodes[node]['u'] = graph.nodes[node]['m']

    else:

        max = -1
        max_node = ""

        for neigh in list(graph.successors(node)):

            if graph.nodes[neigh]['color'] == 1:

                dfs_visit_cover(neigh, graph)

            if graph.nodes[neigh]['u'] > max:

                max = graph.nodes[neigh]['u']
                max_node = neigh

        graph.nodes[node]['u'] = graph.nodes[node]['m'] + graph.nodes[max_node]['u']
        

    graph.nodes[node]['color'] = 0
    topological_order.insert(0, node)



def dfs_visit_cover_iterative(start_node: str, graph: nx.DiGraph) -> None:

    stack = [start_node]
    visitato = set()

    while stack:

        #Prendo il primo elemento dello stack

        node = stack[-1]

        if graph.nodes[node]['color'] == 1:

            #Segno il nodo come scoperto

            graph.nodes[node]['color'] = 2

            #Variabile per preservare il post-order della visità in profondità
            #Posticipo l'elaborazione del nodo corrente, se ci sono successori 
            #non ancora completamente esplorati. Nella ricorsiva, questa logica
            #è implicita: il codice dopo la chiamata ricorsiva non viene 
            #eseguito finché non torno a quella chiamata.
            #Serve quindi a simulare questa attesa implicitamente

            #In un grafo A : [B, C] - B : [D] - C : [D] - D : []

            #stack = [A], A diventa grigio
            #   Successori: B, C -> Inserisco B nello stack
            #       tutti_visitati = False (almeno un successore è ancora da
            #                               visitare)
            #stack = [A, B], B diventa grigio
            #   Successori: [D]
            #       tutti_visitati = False (almeno un successore è ancora da
            #                               visitare)
            #stack = [A, B, D], D è foglia, u[D] = m[D] = 1
            #   etc..

            tutti_visitati = True

            for neigh in graph.successors(node):

                if graph.nodes[neigh]['color'] == 1:

                    stack.append(neigh)
                    tutti_visitati = False

            if not tutti_visitati:

                continue  # aspetta di visitare prima tutti i successori

        #Tutti i successori sono già stati esplorati

        if node not in visitato:

            if not list(graph.successors(node)):

                graph.nodes[node]['u'] = graph.nodes[node]['m']

            else:

                max_u = -1
                max_node = ""

                for neigh in graph.successors(node):

                    if graph.nodes[neigh]['u'] > max_u:

                        max_u = graph.nodes[neigh]['u']
                        max_node = neigh

                graph.nodes[node]['u'] = graph.nodes[node]['m'] + graph.nodes[max_node]['u']

            #Visita terminata

            graph.nodes[node]['color'] = 0
            topological_order.insert(0, node)
            visitato.add(node)
            stack.pop()

        else:

            stack.pop()  # già completato, rimuovilo



def get_topological_order() -> list:

    return topological_order.copy()



def clear_topological_order() -> None:

    topological_order.clear()


#Visita in profondità utilizzata nel calcolo del flusso tramite l'algoritmo di
#Ford-Fulkerson. Serve a riempire il dizionario dei predecessori

def dfs_visit_flow_recursive(node: str, graph : nx.DiGraph) -> None:

    graph.nodes[node]['color'] = 2 #Imposto a grigio il colore, nodo scoperto    

    for neigh in list(graph.successors(node)):

        if graph.nodes[neigh]['color'] == 1:

            graph.nodes[neigh]['predecessor'] = node
            dfs_visit_flow_recursive(neigh, graph)

    graph.nodes[node]['color'] = 0



def dfs_visit_flow_iterative(start_node: str, graph: nx.DiGraph) -> None:

    #Alla fine non è necessario l'utilizzo di tutti_visitati perché non c'è
    #nessun calcolo che dipende dai successori. Dato che serve sono a segnare
    #i successori.

    stack = [start_node]

    while stack:

        # Prendo il nodo in cima allo stack

        node = stack[-1]  

        if graph.nodes[node]['color'] == 1:

            graph.nodes[node]['color'] = 2  # grigio = scoperto

            for neigh in graph.successors(node):

                if graph.nodes[neigh]['color'] == 1:

                    graph.nodes[neigh]['predecessor'] = node

                    #Inserisco nello stack il nodo successore

                    stack.append(neigh)

                    #Interrompo il ciclo in modo da "entrare" nel nodo appena
                    #aggiunto come nella ricorsione
                    break 
        else:
            
            #Se siamo tornati al nodo chiamante, lo marchio come nero
            #e lo rimuovo dallo stack
            graph.nodes[node]['color'] = 0
            stack.pop()

        
        

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