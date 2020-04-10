
from bintreeFile import Bintree
from linkedQFile import LinkedQ
import sys


#klassen noden har attributerna värde och fadder.
class nod:
    def __init__(self,värde):

        self.värde=värde
        self.fadder=None

#läser in ordlistan
def läsaIntext(text):
    text+=".txt"
    fil = open(text, 'r', encoding ="utf-8")
    läsInfil= fil.readlines()
    fil.close()
    return delaUppfil(läsInfil,text)

#Vilkoret delar upp den svenskatexten.
#Orden rensas på brytningar innan de läggs in i sTräd.
def delaUppfil(läsInfil,text):
        for ord in läsInfil:
            ord=ord.replace("\n","")
            if ord not in sTräd:
                sTräd.put(ord)

#Funktionen har inparametern startNod, q. startNod är i det här fallet
#noden som varierar med anrop och används till skapa nya barn.
# Variabeln albeta som omvandlas till listan albeta
#som innehåller hela alfabetet elementvis. En for loop används för att
#variera en char i taget i hela str som startNodens värde.
#Varje "mutation" blir en barn som kollas om den finns i sTräd(ordlistan)
#samt om den inte finns i dumbarnen(så att vi har inte redan besökt den här nodvärdet).
#Ifall vilkoret uppfylls så skapas en ny nodbarn, startnoden tilldelas som nodfaddern och
#varje nod tills till en listan av nya "godkänd" barn samt läggs nodvärdet in i dumbarn så de
#förbjuds i nästa iterationer.
#sista så läggs alla godkända nodbarn in i kön q.
def makechildren(startNod,q):
    albeta=["a,b,c,d,e,f,g,h,j,i,k,l,m,n,o,p,r,s,t,u,v,x,y,z,å,ä,ö"]
    albeta=albeta[0].split(",")
    barnen=[]
    #Loopar tills kö listan är tom
    tempOrd=startNod.värde.värde
    for i in range(len(tempOrd)):
        for bokstav in albeta:
            #Skapar ett barn och lägger det i listan
            barn = tempOrd[:i] + bokstav + tempOrd[i+1:]
            #Om barnet finns i ordlistan(alltså är ett äkta barn) samt saknas i dumlistan (alltså ny incestbarn)
            if barn in sTräd and barn not in dumbarn:
                    nodbarn=nod(barn)
                    nodbarn.fadder=startNod
                    barnen.append(nodbarn)
                    dumbarn.put(barn)


    for nodbarn in barnen:
        q.enqueue(nodbarn)

#Rekursiv funktion som anropar på sig själv tills startnoden är nådd. Första vilkoret
#finns för att garantera att bfs&writechildren hittade en lösning. Andra vilkoret
#garanterar att vi inte träder in i ett Noneobjekt d.v.s att stamfaddern är funnen.
#För varje iteration så returneras ett print sats med aktuella tempnodens värde.
#p.g.a. rekursiviteten innebär det att första print satsen som returneras/skrivs ut
#kommer bli stamfadder och det sista den sökta barnbarn...
def writechildren(tempnod):
    if tempnod!=None:
        if tempnod.värde.fadder!=None:
            writechildren(tempnod.värde.fadder)
            return print(tempnod.värde.värde)
        else:
            return print(tempnod.värde.värde)

#I bfs funktion skapas en kö q. Start/slut-värdet används till att skapa start/slut-noden.
#Inittialt så stoppas startNoden i kön och av taktiska skäll så skapas en ny tempnod med startNoden.
#startvärde stoppas i sista begynneslesteget in i dumbarn-trädet för att förhindra nya nodbarn att skapas
#på med det värdet.
#Själva bfs strategin börjar med while not loopen. Den fortgår så länge kön q är inte tom.
#En vilkor för att jämföra tempnoder mot slutnoden är insat. Så länge vilkor är uppfylld (d.v.s de är skilda)
#så dequeues första noden i kön(sparas i en mellannod) och därefter anropas funktionen makechildren med inparameter av
#det dequeue:ade noden och kön q. Om vilkoret inte uppfylls så bryts while not loopen och det senaste dequeue:ade noden
#returneras
def bfs(startvärde, slutvärde):
    q=LinkedQ()
    startNod=nod(startVärde)
    slutNod=nod(slutVärde)
    q.enqueue(startNod)
    dumbarn.put(startVärde)
    tempnod = nod(startNod)
    while not q.isEmpty():
        if tempnod.värde.värde!=slutNod.värde:
            tempnod = q.dequeue()
            makechildren(tempnod,q)
        else:
            q.dequeue()
    if tempnod.värde.värde==slutNod.värde:
        return tempnod
    else:
        print("Den här vägen är omöjligt")


#Skapar alla träd som ska hålla ordlista & dumbarnen så
#man passerar barnen en enda gång
#funktion läsaIntext läser in ordlista och fyller sTräd.
sTräd=Bintree()
dumbarn=Bintree()
läsaIntext("svenska")
#För att göra det smidigare har jag valt att bestämma orden i förtur.
startVärde="söt"
slutVärde="sur"

#Här anropar vi på rekursiva funktion writechildren och bfs.
writechildren(bfs(startVärde, slutVärde))
#sys.exit() avslutar programmet
sys.exit()
