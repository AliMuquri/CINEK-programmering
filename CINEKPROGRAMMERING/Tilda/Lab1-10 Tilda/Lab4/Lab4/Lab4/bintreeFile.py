class Nod:
    def __init__(self,nyVärde):
        self.värde=nyVärde
        self.vänsterNod=None
        self.högerNod=None
        
class Bintree:
    def __init__(self):
        self.root = None

    def put(self,nyVärde):
        # Sorterar in nyvärde i trädet. Initialt börjar den med att tilldela ett värde till roten
        # När den är skild från None så anropas funktionen putta för att sortera in värdet korrekt i "trädet"
        if self.root==None:
            self.root=Nod(nyVärde)
        else:
            putta(self.root,nyVärde)
            
    #Metoden undersöker om root är inte tom och sedan anropar på finns funktion med inparameter av root-noden
    #och det söktaVärdet. HÄR RETURNERAR TRUE ELLER FALSE ist för text som förut.
    def __contains__(self,söktaVärde):
        # True om value finns i trädet, False annars
        if self.root!=None:
            if finns(self.root,söktaVärde):
                return True
            else:
                return False
            
        else:
            return False
        
    #Utskrivnings metod fortsätter om det finns en nod i root.
    #Här anropas funktionen skriv med inparameter root.    
    def write(self):
        # Skriver ut trädet i inorder
        if self.root != None:
            skriv(self.root)
            print("\n")
            
#putta funktionen undersöker om det nya värdet i noden ligger till vänster
#eller till höger om aktuellaNodens värde, d.v.s. om det är mindre eller större värde.
#Om sann vilkor uppfylls till ena av de vilkoren och samtidigt så är den vänstra eller högra Noden tom
#så tilldelas den aktuellaNoden ett höger eller vänster nod med det nya värdet.
#Om vänster eller högernod till aktuellaNoden är inte tom, så anropas funktionen om igen, med ny relevant inparameter.
#Vilket leder till att den aktuellaNoden ersätts, mot antigen den tidigare aktuellaNodens vänstra eller högra nod
#och det nya värdet prövas om igen tills en tom vänster eller höger nod har hittats.            
def putta (aktuellNod, nyVärde):  
    if nyVärde < aktuellNod.värde:
        if aktuellNod.vänsterNod==None:
            aktuellNod.vänsterNod=Nod(nyVärde)
            return aktuellNod
        else:            
            putta(aktuellNod.vänsterNod,nyVärde)
    elif nyVärde > aktuellNod.värde:
        if aktuellNod.högerNod==None:
            aktuellNod.högerNod=Nod(nyVärde)
            return aktuellNod
        else:
            putta(aktuellNod.högerNod,nyVärde)
    

        

#Metoden undersöker om det söktaVärde:t är större eller mindre (ligger till höger/vänster)
# av det aktuellaNoden. Nästa vilkor undersöker om det finns flera noden i lägre nivåer.
# Om vilkoret uppfylls så anropas finns metoden om igen med ny inparameter (höger/vänster-nod)
# Den fortsätter att undersökaa till antigen det söktaVärde och aktuellaNoden värde överstämmer (True)
#Eller tills det finns ina fler nivåer (vänster/höger-Nodar) vilket isf returnerar (False)
def finns(aktuellNod,söktaVärde):
    t=False
    if söktaVärde == aktuellNod.värde:
        t=True
    elif söktaVärde < aktuellNod.värde and aktuellNod.vänsterNod!=None:
        t=finns(aktuellNod.vänsterNod, söktaVärde)
    elif söktaVärde > aktuellNod.värde and aktuellNod.högerNod!=None:
        t=finns(aktuellNod.högerNod, söktaVärde)
    return t
#Skriva funktionen prövar om aktuellNod är inte tom och så länge den inte är det
#anroppar det skriva funktionen igen med ny inparameter(vänster eller högernod av aktuellaNoden)
# Samtidigt så printar den ut den aktuellaNodens värde
def skriv (aktuellNod):
    if aktuellNod != None:
            skriv(aktuellNod.vänsterNod)
            print(aktuellNod.värde)
            skriv(aktuellNod.högerNod)
