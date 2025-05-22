import gfa_paths

#Dato l'ordine topologico e la path cover minima, questo algoritmo crea la 
#matrice booleana avente come colonne l'ordinamento topologico e come righe 
#la path cover. La matrice ha valore se un nodo di dell'ordinamento topologico
#appartiene ad un percorso, False altrimenti.

def path_cover_binary_matrix(topological_order : list, path_cover : list) -> list[list[bool]]:

    #Inizializzo la matrice rettangolare con tutti i valori a False.
    #La matrice ha n righe quanti sono i percorsi e m colonne per quanti sono i
    #vertici.

    matrix = [[False for _ in range(len(topological_order))] for _ in range(len(path_cover))]

    #Scorrendo ogni percorso, scrivo il valore True nella posizione 
    #corrispondente, ovvero matrice[numero_percorso][indice_colonna]

    for path in path_cover:

        for node in path:

            matrix[path_cover.index(path)][topological_order.index(node)] = True

    return matrix.copy()



def print_matrix(matrix : list[list[bool]]) -> None:

    for riga in matrix:
        print(matrix.index(riga))
        print(' '.join(str(val) for val in riga))
        print("")



#Converte i percorsi specificati nel grafo in liste lunghe quanto
#l'ordinamento topologico con valore True se il nodo appartiene al percorso,
#False altrimenti.

def to_boolean_array(topological_order : list, graph_path : list) -> list:

    boolean_array = [False] * len(topological_order)

    for node in graph_path:
 
        boolean_array[topological_order.index(node)]  = True

    return boolean_array.copy()



def blocks_decompose(boolean_array : list, boolean_matrix : list[list[bool]]) -> list:

    index = 0
    num_colonne = len(boolean_matrix[0])
    matched_block = list()

    while index < num_colonne:

        #Devo saltare gli 0 (soprattutto quello iniziali), successivamente
        #devo riprendere dal primo uno

        while index < num_colonne and boolean_array[index] == False:

            matched_block.append(-1)
            index += 1

        if index  == num_colonne:
            
            break

        (p, l) = longest_match(boolean_array, index, boolean_matrix)

        #Devo togliere gli 0 finali del match. Il match deve essere da 1 a 1
        #al posto degli 0 tolti devo inserire (possibile out of bound)

        while boolean_array[index + l - 1] == False:

            l -= 1

        index += l
        matched_block.extend([p] * l)

    return matched_block



#Calcola il più lungo match dell'array booleano con una riga della matrice a
#partire dalla posizione i (indice della colonna)

def longest_match(boolean_array : list, starting_column_index : int, boolean_matrix : list[list[bool]]) -> tuple:

    num_righe = len(boolean_matrix)
    num_colonne = len(boolean_matrix[0])
    max_path = 0
    max_length = 0

    for indice_riga in range(num_righe):

        index = starting_column_index
        match_lenght = 0

        #Finché matcho, proseguo
            
        while (index < num_colonne) and (boolean_array[index] == boolean_matrix[indice_riga][index]):
          
            match_lenght += 1
            index += 1

        #Se non matcho, devo controllare se tutto ciò che ho matchato
        #prima è il più lungo match trovato

        if match_lenght > max_length:

            max_length = match_lenght
            max_path = indice_riga       
    
    return (max_path, max_length)



#Scrive nel file del grafo, come commento GFA, i percorsi iniziali nel
#seguente modo:
#
#   *   nome_percorso   percorso
#
#Seguito dalla decomposizione in blocchi con lo stesso formato.  

def write_blocks(nomeFile : str, input_paths : gfa_paths, matching_blocks : list) -> None:

    with open(f"standalone/Grafi/{nomeFile}.gfa", "a") as f:

        for path_name in input_paths.nomi_percorsi():

            path = input_paths.get_percorso(path_name)
            formatted_graph_path = f"\n#\tP\t{path_name}\t>"

            for node in path:

                formatted_graph_path += f"{node}>"
            
            #Tolgo l'ultimo > in eccesso

            formatted_graph_path = formatted_graph_path[:-1]
            
            #Aggiungo l'ultimo campo opzionale vuoto

            formatted_graph_path += "\t*"

            #Scrivo su file

            f.write(formatted_graph_path)
            formatted_graph_path = ""

        for block in matching_blocks:

            formatted_block_path = f"\n#\tB\t>"

            for node in block:

                formatted_block_path += f"{node}>"


            #Tolgo l'ultimo > in eccesso

            formatted_block_path = formatted_block_path[:-1]
            
            #Aggiungo l'ultimo campo opzionale vuoto

            formatted_block_path += "\t*"
            f.write(formatted_block_path)
            formatted_block_path = ""

        f.close()






    
