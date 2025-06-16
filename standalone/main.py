import traceback

from path_cover import path_cover
from graph import read_gfa
from graph import convert_graph
from graph import get_graph_topological_order
from ford_fulkerson import ford_fulkerson
from sys import setrecursionlimit
from decompose import path_cover_binary_matrix
from decompose import to_boolean_array
from decompose import blocks_decompose
from decompose import write_blocks

def stampa_cover(cover : list) -> None:

    for path in cover:

        print(f"\n[{cover.index(path)}]:\n\t{path}")
        print("-" * 100)


#Grafi non - aciclici:

#   /spoa

#   A-3105
#   DMB-3109
#   DQA1-3117
#   DQB1-3119
#   DRB1-3123
#   DRB3-3125
#   F-3134
#   H-3136
#   MICB-4277



def main():   
    
    setrecursionlimit(10000)

    nomeFile = "testing/MHC_graph_1000"

    try:

        grafo, percorsi = read_gfa(nomeFile)
        g_star = convert_graph(grafo)
        cover = path_cover(g_star)

        #Cambiare in <= se non si usa il grafo 5
        #Reinserire inoltre la global source e global sink in caso di grafi
        #non appartenenti alla cartella testing

        if len(cover) <= len(percorsi):

            print("Path cover iniziale ottenuta:\n")

            stampa_cover(cover)

            print("\tProcedo a creare il flusso minimo:")

            cover = ford_fulkerson(g_star, cover.copy())
            final_cover = list()

            #Una volta ottenuta la cover finale, procedo a ripulirla dalla 
            #sorgente globale e destinazione globale. Devo inoltre rimuovere
            #tutti i nodi "m" e "p" lasciando solamente il nodo

            for path in cover:

                final_path = list()

                for node in path:

                    if (node != "global_source" and node != "global_sink") and (node[:-1] not in final_path):

                        final_path.append(node[:-1])

                print(final_path)
                final_cover.append(final_path.copy())
                final_path.clear()

            
            print("\t\tLa copertura minima finale è:")

            stampa_cover(final_cover)

            print("Creo la matrice binaria della path cover")

            topological_order = get_graph_topological_order(grafo)
            matrix = path_cover_binary_matrix(topological_order, final_cover)
            boolean_path = list()
            decompose = list()

            print("\tMatrice binaria creata")
            print("Procedo a creare gli array booleani dei percorsi sul grafo")

            for percorso in percorsi.nomi_percorsi():

                path = percorsi.get_percorso(percorso)
                boolean_path.append(to_boolean_array(topological_order, path))

            print("\tPercorsi booleani creati")
            print("Procedo con la decomposizione in blocchi tramite PBWT")

            for path in boolean_path:

                blocks = blocks_decompose(path, matrix)
                decompose.append(blocks)

                print(blocks)
            
            print(f"\tDecomposizioni in blocchi effettuata per {len(percorsi)} percorsi.")
            print("Procedo a salvare il tutto su file:")
            write_blocks(nomeFile, percorsi, decompose)
            print("\tFatto.")

        else:

            print("I percosi trovati sono maggiori di quelli sul grafo!")

    except Exception as e:

        traceback.print_exc()




if __name__ == "__main__":
    
    main()