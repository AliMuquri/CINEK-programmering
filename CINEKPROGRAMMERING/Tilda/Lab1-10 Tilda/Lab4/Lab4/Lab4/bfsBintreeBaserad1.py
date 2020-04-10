from bintreeFile import Bintree

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
        for ordet in läsInfil:
            ord=ordet.strip()
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
def makechildren(startNod,slutNod):
    albeta=["a,b,c,d,e,f,g,h,j,i,k,l,m,n,o,p,r,s,t,u,v,x,y,z,å,ä,ö"]
    albeta=albeta[0].split(",")
    barnen=[]
    #Loopar tills kö listan är tom
    tempOrd=startNod.värde
    for i in range(len(tempOrd)):
        for bokstav in albeta:
            #Skapar ett barn och lägger det i listan
            barn = tempOrd[:i] + bokstav + tempOrd[i+1:]
            #Om barnet finns i ordlistan(alltså är ett äkta barn) samt saknas i dumlistan (alltså ny incestbarn)
            if barn in sTräd and barn not in dumbarn:
                    print(barn)
                    nodbarn=nod(barn)
                    nodbarn.fadder=startNod
                    barnen.append(nodbarn)
                    dumbarn.put(barn)

#Skapar alla träd som ska hålla ordlista & dumbarnen så
#man passerar barnen en enda gång
#funktion läsaIntext läser in ordlista och fyller sTräd.
sTräd=Bintree()
dumbarn=Bintree()
läsaIntext("svenska")

#För att göra det smidigare har jag valt att bestämma orden i förtur.
startOrd="blå"
startNod=nod(startOrd)
slutOrd="röd"
slutNod=nod(slutOrd)    
dumbarn.put(startOrd)
#Funktionen makechildren kallas med inp start/slut-noderna.
makechildren(startNod,slutNod)
