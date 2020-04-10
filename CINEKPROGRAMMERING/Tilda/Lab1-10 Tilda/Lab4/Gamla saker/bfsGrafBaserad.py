from bintreeFile import Bintree
from grafFilen import Graf

#Läser in textfilen svenska
def läsaIntext(text):
    text+=".txt"
    fil = open(text, 'r', encoding ="utf-8")
    läsInfil= fil.readlines()
    fil.close()
    return rensaFil(läsInfil)

#rensar den inlästa textfilen på onödiga mellanslag osv.   
def rensaFil(läsaInfil):
    rensadLäsInfil=[]
    for ord in läsaInfil:
        ord=ord.replace("\n","")
        rensadLäsInfil.append(ord)
    return skapaOrdhinkar(rensadLäsInfil)[0],skapaOrdhinkar(rensadLäsInfil)[1], rensadLäsInfil

#funktionen skapar graf-objektet. Inparameter är den (rensade-ord-filen)
#Varje ord genomgår en "blankning" på varje bokstav i ordet
#En dict använder det nya blankade ordet som en nyckel och lägger till själva fullständiga ordet som ett värde.
#Senare kan, efter annan ord har blankats, samma nyckel påträffas. På det sättet så läggs nästa fullständiga ord
# in under samma nyckel.
#Därefter loopas nycklarna,varje nyckel ger en sammling av ord som läggs in som grannar om de skiljer sig åt.
def skapaOrdhinkar(rensadLäsInFil):
    ordDict = {}
    graf = Graf()
    for ord in rensadLäsInFil:
        #Blankning av bokstaven
        for i in range(len(ord)):
            hink = ord[:i] + '_' + ord[i+1:]
            if hink in ordDict:
                ordDict[hink].append(ord)
            else:
                ordDict[hink] = [ord]
    for hink in ordDict.keys():
        for ord1 in ordDict[hink]:
            for ord2 in ordDict[hink]:
                if ord1 != ord2:
                    graf.läggTillKant(ord1,ord2)
    
    return graf, ordDict


[graf,ordDict, rensadLäsInfil]=läsaIntext("svenska")

print(graf.hämtaVert(input("Ange vilken ord du söker: ")))
##for nyckel in rensadLäsInfil:
##  print(graf.hämtaVert(nyckel))






