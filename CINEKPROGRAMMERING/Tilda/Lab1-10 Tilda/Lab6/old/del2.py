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
        
    def __It__(self,artist):
        if float(self.låttid) >float(artist.låttid):
            return True
        elif float(self.låttid)< float(artist.låttid):
            return False
        else:
            pass
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
def delaUpplistor(låtOlista):
    return låtOlista[:1000],låtOlista[:10000],#låtOlista[:50000], låtOlista[:200000]

#De tre nedanstående funktionerna möjligör att man kan tilldela en statement till timeit.timeit() metoden
#m.h.a "decorators".

#söktlåtid funktion har lokal dict-listan som sparar element som har identifierats som längsta låten.
#templåt variabeln används både för att temporärt hålla den senaste längstalåten för att varje iteration
#spara den i dict-listan men också  för att returnera den nästlängsta låten av en viss ordning som bestäms
#av inparametern n som bestäms av programkörarna tidigare. Funktionen använder sig av låt klass metodens
#__It__ för att jämföra om en objekts self.låttid är större eller mindre än annans låts låttid.
def sökLåttid(låtOlista,n):
    längstalåtlistan={}
    längstalåten=0
    templåt=0
    while 0<n:
        for j in range(len(låtOlista)-1):
            if j==0:
                templåt=låtOlista[j]
            else:
                if templåt.__It__(låtOlista[j])==True:
                    pass
                elif templåt.__It__(låtOlista[j])==False and längstalåtlistan.get(låtOlista[j].artistnamn+låtOlista[j].trackid)==None:
                    #print("LåtOlistalåt:" + låtOlista[j].artistnamn + "låttid:" + låtOlista[j].låttid)
                    templåt=låtOlista[j]
                    #print("templåt:" + templåt.artistnamn + "låttid:" + templåt.låttid)
        längstalåtlistan[templåt.artistnamn+templåt.trackid]=templåt
        n-=1
    return templåt

def sökT(lista,n):
    def sökT1():
        sökLåttid(låtOlista,n)
    return sökT1

def tidsöktid(låtOlista,n):
    sökTf=sökT(låtOlista,n)
    tid=timeit.timeit(sökTf, number=1)
    print("Testmängd: "+ str(len(låtOlista))+ " Tid: " + str(tid))
    

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
        if float(vänsterLista[vänsterInd].låttid)>float(högerLista[högerInd].låttid):
            resultat.append(vänsterLista[vänsterInd])
            vänsterInd+=1
        else:
            resultat.append(högerLista[högerInd])
            högerInd+=1

    resultat.extend(vänsterLista[vänsterInd:])
    resultat.extend(högerLista[högerInd:])
    return resultat

def merg1(låtOlista):
    def merg2():
        mergeSort(låtOlista)
    return merg2

def mergetid(låtOlista):
    mergT=merg1(låtOlista)
    tid=timeit.timeit(mergT, number=1)
    print("Testmängd: " + str(len(låtOlista)) +" Tid: " + str(tid))

#De tre följande funktionerna följer samma upplägg som sök-funktionerna tidigare.
#slå upp funktion tar in en sorterad lista, på låttid, som inparameter tillsammans med vilket ordning av nästlängstalåt
#man söker i variabeln n. Då kan man enkelt slå upp (n-1) då första elementet är börjar på 0. Vilket ger oss
#den låten vi söker.
def slåupp(sortLista, n):
    return sortLista[n]

def su1(sortLista,n):
    def su2():
        slåupp(sortLista,n)
    return su2

def tidslåupp(sortLista,n):
    slåUPP=su1(sortLista,n)
    tid=timeit.timeit(slåUPP,number=1)
    print("Testmängd: " + str(len(sortLista)) + " Tid :" + str(tid))
    
låtOlista=läsaIn()
sortLista=mergeSort(låtOlista)
n=int(input("Ange vilken av längstalåten du söker: "))
print("Osorterad lista")
längstalåt=sökLåttid(låtOlista,n)
tidsöktid(låtOlista,n)
print(längstalåt.artistnamn +" :" + längstalåt.låttid)
print("Sorterad lista")
tidslåupp(sortLista,n)
print(sortLista[n-1].artistnamn+ ":" + sortLista[n-1].låttid)
print("Mergetid:")
mergetid(låtOlista)
