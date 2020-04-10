import csv

#Hämtar modulen csv
class Gym:

    def __init__(self):
        pass

class pokedex(object): 

    def __init__(self, namn, massa):
        
        self.namn=namn
        self.massa=massa
        
    #Gör så att man kan printa objekten"
    def __str__(self):
        return self.namn

    def __It__(self, other):
        
        if self.massa > other.massa:
            return print("%s väger mer än %s"%(pokemon,other))

        elif self.massa==other.massa:
            return print("%s och %s väger lika mycket"%(pokemon,other))
            
        else:
             return ("%s väger mer ä %s" %(other,pokemon))
            

##Använder csv modulens instanser

def skapaKlasser():
    pokemon=[]
    lista=importeraFiler()
    for pokeInfo in lista:
        pokemon.append(pokedex(pokeInfo[0],pokeInfo[1]))
    
    return pokemon    
def importeraFiler(): 

    with open('Pokedex.csv', mode='r') as csvFil:
        reader = csv.reader(csvFil)
        lista=skapaLista(reader)
        return lista
        
def skapaLista(reader):
    integ=0;
    namn=0;
    massindex=0;
    lista=[];
    for rad in reader:
        if integ == 0:
            integ+=1;
            ##Utöka till flera attributer 5st tot
            namnIndex=rad.index("Pokemon")
            massIndex=rad.index("Mass")
            
        else:
            lista.append([rad[namnIndex],rad[massIndex]])
           
    return lista
            
pokedex=skapaKlasser()
fatlist=[]
for pokemon in pokedex:
    for other in pokedex:
        pokemon.__It__(other)
            



    
