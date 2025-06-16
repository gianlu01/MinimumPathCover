import gfa_paths
import BitVector as bv

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
    a_totale, y_totale = pbwt(boolean_matrix)

    while index < num_colonne:

        #Devo saltare gli 0 (soprattutto quello iniziali), successivamente
        #devo riprendere dal primo uno

        while index < num_colonne and boolean_array[index] == False:

            matched_block.append(-1)
            index += 1

        if index  == num_colonne:
            
            break

        (p, l) = longest_match_pbwt(boolean_array, a_totale, y_totale, boolean_matrix, index)

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

        path_and_blocks = ""

        for path_name, block in zip(input_paths.nomi_percorsi(), matching_blocks):

            # Inizializzo le stringhe

            formatted_graph_path = f"\n#\tP\t{path_name}\t>"
            formatted_block_path = f"\n#\tB\t>"

            # Ottengo il nome del percorso

            path = input_paths.get_percorso(path_name)

            for node in path:

                formatted_graph_path += f"{node}>"
            
            #Tolgo l'ultimo > in eccesso

            formatted_graph_path = formatted_graph_path[:-1]
            
            #Aggiungo l'ultimo campo opzionale vuoto

            formatted_graph_path += "\t*"


            # Passo a formattare la stringa con i blocchi matchati

            for node in block:

                formatted_block_path += f"{node}>"

            #Tolgo l'ultimo > in eccesso

            formatted_block_path = formatted_block_path[:-1]
            
            #Aggiungo l'ultimo campo opzionale vuoto

            formatted_block_path += "\t*"


            # Aggiungo alla stringa completa quanto appena calcolato e scrivo
            # su file

            path_and_blocks += formatted_graph_path
            path_and_blocks += formatted_block_path
            f.write(path_and_blocks)

            # Resetto per il nuovo ciclo

            path_and_blocks = ""
            formatted_graph_path = ""
            formatted_block_path = ""

        f.close()



# Implementazione PBWT senza array delle divergenze in quanto non sono 
# necessari i match a ritroso.

def pbwt(matrix: list[list[bool]]) -> tuple:

    aplotipi = len(matrix)              # numero di righe (aplotipi)
    nodi = len(matrix[0])               # lunghezza delle sequenze
    sigma = [False, True]               # alfabeto binario in termini booleani

    # a_precedente è la lista della permutazione inziale, ovvero l'ordinamento 
    # originale della matrice

    a_totale = []   # lista degli a_k (tutti gli ordinameti del paper)
    y_totale = []   # lista di tutti gli y_k ovvero tutti i bitvector
    a_precedente = list(range(aplotipi))      # a_0: [0, 1, ..., aplotipi-1]
    a_totale.append(a_precedente)

    # Parto dalla colonna 1 quindi y_k sarà colonna k+1

    for k in range(nodi):

        # Inizializzo la lista associata agli ordinamenti per ogni lettera
        # dell'alfabeto

        a = {s: [] for s in sigma}

        y_k = []

        # Scorro quindi gli aplotipi

        for i in range(aplotipi):

            # Aquisisco l'indice dell'aplotipo i nell'ordinamento precedente

            indice_aplotipo_ordinamento_precedente = a_precedente[i]

            # c è True o False ed è il valore della riga nella posizione 
            # dell'ordinamento precedente (idx), nella colonna di riferimento k

            c = matrix[indice_aplotipo_ordinamento_precedente][k]

            # Aggiungo alla lista del dizionario l'indice precedente

            a[c].append(indice_aplotipo_ordinamento_precedente)
            y_k.append(c)

        # Eseguo l'append dei valori, prima tutti gli 0 poi gli 1

        a_k = a[False] + a[True]
        a_totale.append(a_k)
        y_totale.append(bv.BitVector(bitlist = y_k))

        # Aggiorno l'ordinamento corrente in modo da portarlo avanti man mano
        # che scorro tutti i nodi

        a_precedente = a_k

    # Una volta scansionati i nodi restituisco la lista di a_totale ovvero per 
    # ogni colonna ho l'ordinamento fino alla posizione nella quale
    # mi trovo attualmente

    return a_totale, y_totale



# Implementazione del calcolo dei rank 0 e 1
# rank(0) = i - rank(1, i)

def rank_0(y_k, indice) -> int:

    return (indice + 1) - rank_1(y_k, indice)



# Calcola il rango di 1 fino alla posizione desiderata (esclusa)

def rank_1(y_k, indice) -> int:

    if indice == -1:

        return 0

    # La libreria funziona solo se y_k[indice] == 1

    if y_k[indice] == 0:

        y_k[indice] = 1
        r =  (y_k.rank_of_bit_set_at_index(indice))
        y_k[indice] = 0

        # Tolgo 1 perché ho modificato il vettore

        r -= 1

    else:

        r = y_k.rank_of_bit_set_at_index(indice)

    return r



# Implementazione longest match tramite ranghi e array a e y della PBWT

def longest_match_pbwt(z, a_totale, y_totale, matrix_paper, start) -> tuple[int, int]:

    num_aplotipi = len(matrix_paper)
    lunghezza_z = len(z)

    # f deve essere inizializzato sempre alla prima posizione di 1 perchè il
    # match parte sempre da 1

    bit = z[start]
    y_k = y_totale[start]
    f = 0
    g = num_aplotipi

    if f == g:

        return (None, 0)

    # All'inizio ho già calcolato [f, g), non ha senso mantenere invariato 
    # l'indice perché otterrei lo stesso risultato

    colonna_estensione = start

    while colonna_estensione < lunghezza_z:

        bit = z[colonna_estensione]
        y_k = y_totale[colonna_estensione]

        if bit == 0:

            f_new = rank_0(y_k, f - 1)
            g_new = rank_0(y_k, g - 1)

        else:

            # Intervallo deve essere:
            # f = il primo 1 prima di f
            # g = l'ultimo 1 prima di g

            r_0 = rank_0(y_k, num_aplotipi - 1)
            r_1_f = rank_1(y_k, f - 1)
            r_1_g = (rank_1(y_k, g - 1))
            f_new = r_0 + r_1_f
            g_new = r_0 + r_1_g

        #Aggiorno gli indici

        if f_new == g_new:

            break

        f = f_new
        g = g_new
        colonna_estensione += 1

    riga_longest = a_totale[colonna_estensione][f]
    lunghezza = colonna_estensione - start

    return (riga_longest, lunghezza)



    
