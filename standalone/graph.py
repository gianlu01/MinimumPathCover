import networkx as nx

from parse_error import ParseError
from gfa_paths import GFAPaths



#Legge un file GFA e crea un grafo in formato DiGraph di NetworkX

def read_gfa(nomeFile : str) -> tuple:

    grafo = nx.DiGraph()
    paths = GFAPaths()

    with open(f"standalone/Grafi/{nomeFile}.gfa", 'r') as gfa_file:

        nodi = list()
        archi = list()

        for line in gfa_file:

            #Nodi

            if line.startswith('S'): 

                campi = line.strip().split('\t')
                node_id = campi[1]
                nodi.append(node_id)

            #Archi

            elif line.startswith('L'):  

                campi = line.strip().split('\t')
                
                if campi[2] != "+" or campi[4] != "+":
                    
                    raise ParseError(f"Impossibile importare il file {nomeFile}.gfa. I link devo essere tutti del tipo + +!")

                from_node = campi[1]
                to_node = campi[3]
                edge = (from_node, to_node)
                archi.append(edge)

            elif line.startswith('P'):
            
                campi = line.strip().split('\t')
                nome_percorso = campi[1]
                segmenti = campi[2].split(',')

                # Rimuove l'orientamento del nodo togliendo + o -
                nodi = [s[:-1] for s in segmenti]
                paths.aggiungi_percorso(nome_percorso, nodi)

        #Ordino gli i nodi e gli archi in ordine crescente:

        nodi_ordinati = sorted(nodi, key=int)
        archi_ordinati = sorted(archi, key=lambda x: (int(x[0]), int(x[1])))

        #Aggiungo i nodi e gli archi al grafo

        for nodo in nodi_ordinati:

            grafo.add_node(nodo)
        
        for u, v in archi_ordinati:

            grafo.add_edge(u, v)

    if nx.is_directed_acyclic_graph(grafo):

        return (grafo, paths)
    
    else:

        cycles = list(nx.simple_cycles(grafo))
        
        for cycle in cycles:

            print(f"[{cycles.index(cycle)}]\t{cycle}")

        raise ParseError("Il grafo non è aciclico!")



#Converte un grafo in g_star, aggiungendo tutti i valori necessari per
#calcolare la path cover iniziale

def convert_graph(grafo : nx.DiGraph) -> nx.DiGraph:

    global_source = "G"
    global_sink = "S"

    g_star = nx.DiGraph()

    # Sdoppia ogni nodo in Ap e Am
    for node in grafo.nodes:

        g_star.add_node(f"{node}m", color=1, u=0, m=1, predecessor=None)
        g_star.add_node(f"{node}p", color=1, u=0, m=1, predecessor=None)
        g_star.add_edge(f"{node}m", f"{node}p", demand=1, flow=0)  # collegamento interno

    # Ricollega gli archi da - a +
    for u, v in grafo.edges:

        g_star.add_edge(f"{u}p", f"{v}m", demand=0, flow=0)

    #Aggiungo la sorgente globale e la destinazione globale

    g_star.add_node(global_source, color=1, u=0, m=1, predecessor=None)
    g_star.add_node(global_sink, color=1, u=0, m=1, predecessor=None)

    for node in grafo.nodes:

        g_star.add_edge(global_source, f"{node}m", demand=0, flow=0)
        g_star.add_edge(f"{node}p", global_sink, demand=0, flow=0)

    return g_star



#Resetta i valori dei predecessori. 

def reset_predecessor(grafo : nx.DiGraph) -> None:

    for node in grafo.nodes():

        grafo.nodes[node]['predecessor'] = None



def reset_flow(graph : nx.DiGraph) -> None:

    for u, v, values in graph.edges(data=True):

        values['flow'] = 0