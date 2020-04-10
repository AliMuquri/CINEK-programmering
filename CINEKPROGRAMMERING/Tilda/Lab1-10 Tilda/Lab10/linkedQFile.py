#Node klass med en konstruktor med 1 inparameter och tva attributer.
class Node:
    def __init__(self, varde):
        self.varde=varde
        self.nastaNod=None

#LinkedQ klassen har konsktruktor med tva privata attributer        
    
class LinkedQ(Node):
    
    def __init__(self):
        self._forstaNod=None
        self._sistaNod=None
        
    #Den ar metoden anvands for att skapa nya Noder
    #Metodens Inparameter ar varde som ar en inparamater som skickas vidare till noden    
    def enqueue(self,varde):

        #Skapar en ny nod-objekt i metoden
        nyNod=Node(varde)
        
        #Kallar pa metoden i klassen som kallas isEmpty() 
        t=self.isEmpty()
        #Vilkoret nedanfor anvands vid skapandet av forsta nod-objektet
        if t== True:
            self._forstaNod = nyNod
            return
    
        #Vilkoret nedanfor hanger ihop med att, vid forsta noden sa har inte
        #nasta referens nod an tilldelats.
        t=self.isEmpty()
        if t==False and self._forstaNod.nastaNod == None:
            self._forstaNod.nastaNod=nyNod
            
        #Vilkorer hangder ihop med man ska endast tillge den nuvarande-sista-noden sin
        #sin nasta ref nod.   
        if self._sistaNod!=None:
            self._sistaNod.nastaNod=nyNod
            
        #Sistanoden blir omdefinerad som den nyaste noden.    
        self._sistaNod=nyNod
        
    def dequeue(self):
        
        #tempNod far behalla den forsta noden. Forsta noden omdefinieras som forsta nodens nasta nod.
        #Referenskedjan hanger kvar med nasta noden. Pa satt kan man tanka sig en analogi dar
        #man tar bort forsta noden i kon och man flyttar upp alla noder efter upp ett steg.    
        tempNod=self._forstaNod
        self._forstaNod=self._forstaNod.nastaNod
        #returnerar vardet pa noden till kortricket funktionen
        #Antigen kommer den hamna langst bak i kon i en ny nod
        #eller laggas fram. 
        return  tempNod.varde

        #Kollar om kon ar tom eller inte. 
    def isEmpty(self):
        if self._forstaNod==None:
            return True
        else:
            return False

    def peek(self):
        if self._forstaNod==None:
            return None
        else:
            return self._forstaNod.varde

       

