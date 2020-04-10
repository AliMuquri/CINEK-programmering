import timeit

# Klassen för pokeobjekt

# hashNode klassen har som inparametrar nyckel och associerad data
# Den har tre attributer i konstruktorn. variabel nästa används senare för att
# kunna bläddrar i "slots".


class hashNode:
    def __init__(self, nyckel, data):
        self.nyckel = nyckel
        self.data = data
        self.nästa = None

    def getNyckel(self):
        return self.nyckel

# Hashtabellen har tre attributer. dimension bestämer hur stor tabell som ska skapas.
# tabellen bevarar hashNoderna. n attributen används för att hålla reda på
# n antalet kollisioner vid insättning.


class Hashtable:

    def __init__(self, size):
        self.size = 2 * size
        # Skapar en lista med size st None element
        self.hashTable = [None] * self.size
        self.n = 0
        self.max = 0
        self.maxN = 0

    # Metode tar in nyckel som parameter och omvandlar den med en algoritm till
    # till ett hashNyckel
    def hashfunction(self, nyckel):
        hashNyckel = 0
        # Olika hashfunktioner

# for siffra, bokstav in enumerate(nyckel):
# print("siffra: " + str(siffra) + "  Längdnyckel: "+ str(len(nyckel)) + "  Upphöjt: " + str(ord(bokstav)))
# hashNyckel+=(siffra+len(nyckel)**ord(bokstav))
# hashNyckel=hashNyckel%self.dimension

        for siffra, bokstav in enumerate(nyckel):
            hashNyckel += hashNyckel * \
                32**(len(nyckel) - siffra) + ord(bokstav)
            hashNyckel = hashNyckel % self.size

        # Kvadratiskt
# for siffra, bokstav in enumerate(nyckel):
# hashNyckel+=hashNyckel*32**(len(nyckel)-siffra)+ord(bokstav)
# hashNyckel=hashNyckel%self.dimension
##
# hashNyckel=str((hashNyckel)**2)
# print(hashNyckel)
# längd=len(hashNyckel)-1
# mittpunkt=int(längd/2)
# hashNyckel=int(hashNyckel[mittpunkt-2:mittpunkt]+hashNyckel[mittpunkt:mittpunkt+4])
# print(hashNyckel)

        # Vi lägger ihop tecken
# for siffra, bokstav in enumerate(nyckel):
# hashNyckel=str(hashNyckel)+str(int(hashNyckel)*32**(len(nyckel)-siffra)+ord(bokstav))
# hashNyckel=int(hashNyckel)%self.dimension

        return hashNyckel

    # Krockhantering med "länkad krocklista" tillväggasätt
    # metoden hashfunction anropas och en hashNyckel genereras.
    # Kollisontestas genom  man kollar i tableen
    # med det nya hashNyckeln. Om hashNoden inte
    # skapas en hashNode objekt med data och nyckel
    # samtidigt som om den placeras i listan med index:hashNyckel
    # Ifall hashNoden existerar i tableen listan
    # så använder man hashNoden:s nästa attribut och ifall den är tom
    # så skapas en ny hashNode med givna nyckeln och datat. Observera
    # att hashNyckeln är samma men inte nyckeln.
    def store(self, nyckel, data):
        hashNyckel = self.hashfunction(nyckel)
        hashNod = self.hashTable[hashNyckel]
        if hashNod == None:
            self.hashTable[hashNyckel] = hashNode(nyckel, data)
            return
        self.n += 1
        förra = hashNod
        tempmax = 0
        while hashNod != None:
            tempmax += 1
            förra = hashNod
            hashNod = hashNod.nästa
        förra.nästa = hashNode(nyckel, data)
        if tempmax > self.max:
            self.max = tempmax
            self.maxN = 0
        elif tempmax == self.max:
            self.maxN += 1

    # Där vi avslutade i metoden store är grunden till
    # den här metoden. En nyckel ges som inparameter. Metoden hashfunction anropas
    # en hashNyckel returneras. Man söker med hashNyckeln och nyckeln
    # med en while loop för att söka genom den länkade listan i den givna index:hashNyckeln
    # efter den hashNoden som har det specifika nyckeln.

    def search(self, nyckel):
        hNyckel = self.hashfunction(nyckel)
        hashNod = self.hashTable[hNyckel]
        while hashNod != None and hashNod.getNyckel() != nyckel:
            hashNod = hashNod.nästa
        if hashNod != None:
            return hashNod.data
        else:
            raise KeyError
