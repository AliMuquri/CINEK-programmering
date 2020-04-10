import timeit
#Klasse låtar har en konstruktor som innehåller profilen för låten.
#Metodnen __It__ jämför self med annan objekt m.a.p. låtlängd/tid
class låtar:
    def __init__(self,trackid,artistnamn,låttitel,låttid,år):
        self.trackid=trackid
        self.artistnamn=artistnamn
        self.låttid=låttid
        self.låttitel=låttitel
        self.år=år

    def __lt__(self,artist):

        if self.artistnamn.lower() <artist.artistnamn.lower():
            return True
        elif self.artistnamn.lower()> artist.artistnamn.lower():
            return False

    def __str__(self):
        return self.artistnamn

#Funktionen läser in textfilen och m.h.a. strip() och split()
#skapas en matris, en lista med en annna lista i varje element.
#därefter kallas på funktionen skapaObjekt.
def läsaIn():
    fil=open("sang-artist-data.txt", 'r', encoding ="utf-8")
    textrad=fil.readlines()
    profillista=[]
    for text in textrad:
        profillista.append(text.replace("\n","").split("\t"))
    return skapaObjekt(profillista)

#Här skapas objekten och de tilldelas till en seperat lista
def skapaObjekt(profillista):
    låtobjektlista=[]
    for profil in profillista:
        låt=låtar(profil[0],profil[1],profil[2],profil[3],profil[4])
        låtobjektlista.append(låt)
    return låtobjektlista

#Funktion används för att skapa listor med olika antal testmängder /låtobjekt.
def delaUpplistor1(låtOlista):
    return låtOlista[:100],låtOlista[:1000],låtOlista[:10000], #låtOlista[:1000000]

def delaUpplistor2(låtOlista):
    return låtOlista[:1000],låtOlista[:10000],låtOlista[:100000], #låtOlista[:1000000]

#https://www.geeksforgeeks.org/python-program-for-bubble-sort/

def bubbleSort(låtlista):
    låtlistan=låtlista
    n=len(låtlistan)
    for i in range(n):
        temp=None
        for j in range(0,n-i-1):
            if not låtlistan[j] < (låtlistan[j+1]):
                låtlistan[j], låtlistan[j+1]=låtlista[j+1],låtlista[j]

    return låtlistan

def bubbelSorttid(låtOlista):
    for låtlista in låtOlista:
        tid=timeit.timeit(lambda:bubbleSort(låtlista), number=1)
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
    #SÖNDRA
    vänsterLista = mergeSort(låtOlista[:int(len(låtOlista)/2)])
    högerLista = mergeSort(låtOlista[int(len(låtOlista)/2):])

    return merge(vänsterLista, högerLista)

def merge(vänsterLista, högerLista):
    resultat=[]
    vänsterInd=högerInd=0
    #HÄRSKA
    while  vänsterInd<len(vänsterLista) and högerInd < len(högerLista):
        if vänsterLista[vänsterInd] < (högerLista[högerInd]):
            resultat.append(vänsterLista[vänsterInd])
            vänsterInd+=1
        else:
            resultat.append(högerLista[högerInd])
            högerInd+=1

    resultat.extend(vänsterLista[vänsterInd:])
    resultat.extend(högerLista[högerInd:])
    return resultat

def mergetid(låtOlista):
    for låtlista in låtOlista:
        tid=timeit.timeit(lambda:mergeSort(låtlista), number=1)
        print("Testmängd: " + str(len(låtlista)) +" Tid: " + str(round(tid  ,4)))


låtOlista=läsaIn()
#Ändrar antalet element för bubbelsort. Mönstret är likadant men 100000 element är opraktiskt
#förväntad körning blir 83min.
låtlistor=delaUpplistor1(låtOlista)
låtlistor1=delaUpplistor2(låtOlista)
print("Långsamt metod:Bubbelsort")
bubbelSorttid(låtlistor)

print("Snabbare metod: Mergetid")
mergetid(låtlistor1)

#Sorterad lista (med mergeSort)
# ________________________________
# Tidskomplexiteten av mergeSort �r O(nlog(n))
# Metodens effektivtet är bortom tvivel. Samsortering via söndra och härska
# har fördelar i form av effektivitet men kräver mer minne.
#______________________________________

#T Tidskomplexitet av Bubbelsort O(n^2)
#Är starkt påverkad av antalet element som ligger i omvändning ordning.
