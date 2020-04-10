import timeit
#Klasse låtar har en konstruktor som innehåller profilen för låten.
#Metodnen __It__ jämför self med annan objekt m.a.p. namnordning
class låtar:
    def __init__(self,trackid,låttid,artistnamn,låttitel):
        self.trackid=trackid
        self.artistnamn=artistnamn
        self.låttid=låttid
        self.låttitel=låttitel

    def __It__(self,artist):
        if self.artistnamn.lower() >artist.artistnamn.lower():
            return True
        elif self.artistnamn.lower()< artist.artistnamn.lower():
            return False
        else:
            print("LIKA")

#Funktionen läser in textfilen och m.h.a. strip() och split()
#skapas en matris, en lista med en annna lista i varje element.
#därefter kallas på funktionen skapaObjekt.
def läsaIn():
    fil=open("unique_tracks.txt", 'r', encoding ="utf-8")
    textrad=fil.readlines()
    profillista=[]
    for text in textrad:
        profillista.append(text.strip().split("<SEP>"))
    return skapaObjekt(profillista)[0],skapaObjekt(profillista)[1]

#Här skapas objekten och de tilldelas till en seperat lista och dict
#som key används trackid och artistnamn.
def skapaObjekt(profillista):
    låtobjektlista=[]
    låtobjektdict={}
    for profil in profillista:

        låt=låtar(profil[0],profil[1],profil[2],profil[3])
        låtobjektlista.append(låt)
        låtobjektdict[profil[2]+profil[0]]=låt
    return låtobjektlista, låtobjektdict
#Funktion används för att skapa listor med olika antal testmängder /låtobjekt.
def delaUpplistor(låtOlista):
    return låtOlista[:250000],låtOlista[:500000],låtOlista[:1000000],# låtOlista[:200000]

#Det här upplägget upprepas för de andra funktionerna också.

#Funktion söker låt-"Objekt"-listan efter söknamnet. if-satsens vilkor
#innnebär att for loopen bryts om namnet hittas. Variabeln sök returnerar om
#artisten hittades eller inte.
def linjärsökning(låtOlista,söknamn):
    sök=False
    for i in range(len(låtOlista)):
        if låtOlista[i].artistnamn==söknamn:
            sök=True
            break
    return sök


def tidlinjärsökning(ulåtOlista,söknamn):
    for låtlista in ulåtOlista:
        tid=timeit.timeit(lambda:linjärsökning(låtlista, söknamn), number=1000)
        print("Testmängd: " + str(len(låtlista)) +" Tid: " + str(round(tid  ,4)))

#https://www.youtube.com/watch?v=rAqBlKhy_oI

#mergeSort funktion delar objekt listan i rekursiv form tills listan blir en element lista .
#if-satsen stoppar rekursiva anrop när lista av enstaka element har uppnåts
#mergeSort anropar funktion merge i sin retursats. De sorteras först parvis element
#och slås ihop till en lista. Därefter sorteras listorna parvis och slås ihop till större listor
#Tills en hel sorterad lista har skapats i resultat som returneras.
def mergeSort(låtOlista):
    if len(låtOlista) <=1:
        return låtOlista

    #mittpunkt=int(len(låtOlista))/2
    vänsterLista = mergeSort(låtOlista[:int(len(låtOlista)/2)])
    högerLista = mergeSort(låtOlista[int(len(låtOlista)/2):])

    return merge(vänsterLista, högerLista)

def merge(vänsterLista, högerLista):
    resultat=[]
    vänsterInd=högerInd=0
    while  vänsterInd<len(vänsterLista) and högerInd < len(högerLista):
        if not vänsterLista[vänsterInd].__It__(högerLista[högerInd]):
            resultat.append(vänsterLista[vänsterInd])
            vänsterInd+=1
        else:
            resultat.append(högerLista[högerInd])
            högerInd+=1

    resultat.extend(vänsterLista[vänsterInd:])
    resultat.extend(högerLista[högerInd:])
    return resultat


#De tre följande funktionerna följer samma upplägg som sök-funktionerna tidigare.

#binärsök funktion tar en sorterad lista. Söknning börjar i mitten av listan. Söknamn variabeln
#jämförs med det mellersta elementet om elementet är inte hittad så går den vidare med antingen
#den med mindre sidan eller högre beroende på om sökelementet var mindre eller större än elementen i mitten.
#Det här upprepas för den nästa sida av listan som ska sökas. På det här sättet utesluter man 50% av listan/sidan
#för varje iteration.
def binärSök(sortLista,söknamn):
        första=0
        sista=len(sortLista)-1
        t=False
        while första <=sista and not t:
            mittpunkt =int((första + sista)/2)
            if sortLista[mittpunkt].artistnamn.lower()==söknamn.lower():
                t=True
            else:
                if söknamn.lower() < sortLista[mittpunkt].artistnamn.lower():
                    sista=mittpunkt-1
                else:
                    första=mittpunkt+1

def tidbinärsökning(usortLista,söknamn):
    for sortLista in usortLista:
        tid=timeit.timeit(lambda: binärSök(sortLista,söknamn), number=1000)
        print("testmängd: " + str(len(sortLista)) +" Tid:" + str(round(tid  ,4)))

#De tre följande funktionerna följer samma upplägg som sök-funktionerna tidigare.

#Sök funktionen tar parametern söknamn som innehåller key till det låt man söker
def dictSök(låtOdict,söknamn):
    låtOdict.get(söknamn)

def tidDictSök(låtOdict,söknamn):
    tid=timeit.timeit(lambda:dictSök(låtOdict,söknamn), number=1000)
    print("Testmängd: " + str(len(låtOdict)) +" Tid: " + str(round(tid  ,4)))

# Skapar osorterad lista & dict av object
låtOlista,låtOdict=läsaIn()
#Skapar sorterad lista av obj med mergeSort
sortLista=mergeSort(låtOlista)
#Skapar lista som innehåller olika storlek av listor av objekt
ulåtOlista=delaUpplistor(låtOlista)
usortLista=delaUpplistor(sortLista)
#Ordet vi söker på (ligger ganska mycket i början)
söknamn="Christian Castro"
print("Osorterad lista")
tidlinjärsökning(ulåtOlista,söknamn)
print("Sorterad lista")
tidlinjärsökning(usortLista,söknamn)
print("Binärsök")
tidbinärsökning(usortLista,söknamn)
print("Dict-sök")
söknamn=("Christian CastroTRMMMPJ128F9306985")
tidDictSök(låtOdict,söknamn)
#
# sökfunktioner			Tidskomplexitet
# _________________________________________________
# Linjärsökning			O(n)
# _________________________________________________
# Binärsökning			O(log(n)) eller O(n)
# 				beror på om det element
# 				man söker efter hittas i
# 				 början av s�kningen
# __________________________________________________
# Dict-sök 			O(1)
# (samma gäller för en
# sorterad lista om man
# har en given index)
# (slå upp)
# _________________________________________________
#
# Anmärkning:
#
# Hash-tabell baserade sökningar
# _______________________________
#
# Dict och sorterad lista med given index är effektivaste sökfunktionerna med tidskomplexitet av O(1)
# då index/nyckeln är direkt assoscierad till elementet man s�ker.
#

#
# Binärs�kning (kräver sorterad lista)
# ------------------------------------
# Binär sökningar har en tidskomplexitet av Olog(n) eller O(n).
# Om elementen man söker identifieras i precis av början av sökningen
# så får den samma komplexitet som linjårsökning O(n).
# Annars gör den över till O(log(n)),varje iteration utesluter 50% av
# den mngd av listan som man söker i. Det här går
# den väldigt effektivare än en linjärs�kning.
#
# Linjärsökning (med sorterad lista)
# ---------------------------------------
# Tidskomplexitet är  O(n) som vanligt linjärsökning.
#
# Linjärsökning (osorterad lista)
# _________________________________________
# Tidskomplexitet är O(n). Tidsåtgången
# direkt associerad till vilken element med söker och vad den har får placering i den sorterade
# och osorterade listan. Om den ligger tidigt i den osorterade listan man hamnar längre bak i listan
# när den blir sorterad så är den osorterade mer gynsamm och vice verse. Dessto större lista desto
# större effekter kan man färvänta sig.
