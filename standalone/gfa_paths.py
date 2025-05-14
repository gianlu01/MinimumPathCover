#Classe che permette di salvare i percorsi appartenenti ad un GFA in un
#dizionario del tipo nomePercorso : [elenco di nodi]


class GFAPaths:

    def __init__(self):

        self.paths = {}



    #Aggiunge un percorso al dizionario

    def aggiungi_percorso(self, nome, nodi):
       
        if nome in self.paths:

            raise ValueError(f"Il percorso '{nome}' esiste già.")
        
        self.paths[nome] = nodi

    

    #Restituisce un percoso dal dizionario

    def get_percorso(self, nome):
        
        return self.paths.get(nome)



    #Rimuove un percorso dal dizionario

    def rimuovi_percorso(self, nome):
        
        if nome in self.paths:
            del self.paths[nome]



    #Restituisce i nomi dei percorsi

    def nomi_percorsi(self):
        
        return list(self.paths.keys())
    


    #Stampa i percorsi

    def stampa_percorsi(self):
    
        for nome_percorso, nodi in self.paths.items():

            print(f"Percorso:\t{nome_percorso}")
            print(f"Nodi:\t{nodi}")
            print("-" * 20)



    #Metodi necessari per il corretto funzionamento della classe ad esempio per
    #chiamare la funzione len()

    def __contains__(self, nome):

        return nome in self.paths



    def __iter__(self):
        
        return iter(self.paths)



    def __len__(self):

        return len(self.paths)



    def __str__(self):
        return "\n".join(f"{k}: {v}" for k, v in self.paths.items())
    
