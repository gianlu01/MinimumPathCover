from path_cover import path_cover
from graph import read_gfa
from graph import convert_graph
from ford_fulkerson import ford_fulkerson
from sys import setrecursionlimit


def stampa_cover(cover : list) -> None:

    for path in cover:

        print(f"\n[{cover.index(path)}]:\n\t{path}")
        print("-" * 100)


#Grafi non - aciclici:

#   A-3105
#   DMB-3109
#   DQA1-3117
#   DQB1-3119
#   DRB1-3123
#   DRB3-3125
#   F-3134
#   H-3136
#   MICB-4277



#Non funzionanti:

#   DPA1-3113   -   Corretto
  


def main():   
    
    setrecursionlimit(10000)

    nomeFile = "spoa/DPA1-3113"
    grafo, percorsi = read_gfa(nomeFile)
    g_star = convert_graph(grafo)
    cover = path_cover(g_star)

    if len(cover) <= len(percorsi):

        print("Path cover iniziale ottenuta:\n")

        stampa_cover(cover)

        print("Procedo a creare il flusso minimo:")

        cover = ford_fulkerson(g_star, cover.copy())
        
        print("La copertura minima finale è:")

        stampa_cover(cover)




if __name__ == "__main__":
    
    main()