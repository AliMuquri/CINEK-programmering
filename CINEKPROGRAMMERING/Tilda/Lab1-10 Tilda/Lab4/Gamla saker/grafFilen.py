#Klassen Vertex(hörn) (väldigt lik en nod)
class Vertex:
    
    #Vertexens konstruktor har attributen nyckel som tilldelas som hörnets
    #identitet. En dic finns också
    #för att ange vilka grannar som den här hörnen är koppad till. 
    #Alltså varje vertex har sitt eget id i form en variabel "string"
    def __init__(self,nyckel):
        self.id = nyckel
        self.koppladTill = {}
        
    #Metoden lägger till grannar i form av dict-object.
    #Viktad anger vad kostnaden för övergången mellan de är. 
    def läggTillGranne(self,grannen,viktad=0):
        self.koppladTill[grannen] = viktad

    #När objekten printas så returnerar de både id och sina grannar
    #som den är kopplad till.
    def __str__(self):
        return str(self.id) + ' koppladTIll: ' + str([x.id for x in self.koppladTill])

    #Metoden returnerar alla grannar i formav "nycklar". Metoden
    #använder sig av dicts egna metod keys()
    def hämtaKopplingar(self):
        return self.koppladTill.keys()
    
    #Metoden returnerar id, nyckeln till vertexen
    def hämtaId(self):
        return self.id
    
    #Metoden hämtar ---------------
    def hämtaViktning(self,grannen):
        return self.koppladTill[grannen]
    
    
class Graf:
    #Grafens konstruktor har behåller en dict-lista på alla vertexer och
    #håller räkningen på antalet.
    def __init__(self):
        self.vertLista = {}
        self.antalVert = 0
    #Skapar en Vertex-objekt med nyckel som parameter(för id), som läggs till vertLista:n
    #och tilldelar sin dict-element nyckel som "key" 
    #Gör tillägg till antalVert:exer.
    #Returnerar dessutom den nya Vertex-objekten.
    def läggTillVert(self,nyckel):
        self.antalVert = self.antalVert + 1
        #Här skickas nyckel som parameter för self.id=nyckel
        nyVertex = Vertex(nyckel)
        #Här tilldelas nyckel som "key" till dict-elementet som tilldelas Vertex-objekten
        #(som nu innehåller self.id) som värde
        self.vertLista[nyckel] = nyVertex
        return nyVertex

    #Metoden används för att hämta en specifc vertex
    #som innehåller en specifik nyckel.
    #Returnerar antigen den eftersökta vertex-objekten eller None. 
    def hämtaVert(self,nyckel):
        if nyckel in self.vertLista:
            return self.vertLista[nyckel]
        else:
            return None
        
    #Metoden returnerar antigen True eller False om den hittar
    #vertexen med en specifik nyckel i vertLista.
    def __contains__(self,nyckel):
        return nyckel in self.vertLista
    
    #Här läggs till kanter till varje vertex med
    #hjälp av läggTillGranne metoden i Vertex klassen.
    def läggTillKant(self,f,t,cost=0):
        if f not in self.vertLista:
            nv = self.läggTillVert(f)
        if t not in self.vertLista:
            nv = self.läggTillVert(t)
        self.vertLista[f].läggTillGranne(self.vertLista[t], cost)
    #Metoden returnerar alla vertexer i form av "nycklar". Metoden
    #använder sig av dicts egna metod keys() som returnerar nycklar 
    def hämtaAllaVert(self):
        return self.vertLista.keys()
    
    #Iter() metoden skapar en objekt som tillåter en smidig iteration av alla Vert-objekt i vertLista:n.
    #De blir härmed returnerade en i taget.
    def __iter__(self):
        return iter(self.vertLista.values())    
