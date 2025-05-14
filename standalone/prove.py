import networkx as nx
import os

def read_gfa(nomeFile : str) -> nx.DiGraph:

    grafo = nx.DiGraph()

    with open(f"Grafi/{nomeFile}.gfa", 'r') as gfa_file:

        for line in gfa_file:

            if line.startswith('S'): 

                parti = line.strip().split('\t')
                node_id = parti[1]
                grafo.add_node(node_id)

            elif line.startswith('L'):  

                parti = line.strip().split('\t')
                da = parti[1]
                a = parti[3]
                grafo.add_edge(da, a)
    
    return grafo



grafo = read_gfa("Grafo 5")
print(grafo)
