#Node klass med en konstruktor med 1 inparameter och två attributer.
class Node:
    def __init__(self, värde):
        self.värde=värde
        self.nästaNod=None

#LinkedQ klassen har konsktruktor med två privata attributer        
    
class LinkedQ(Node):
    
    def __init__(self):
        self._förstaNod=None
        self._sistaNod=None
        
    #Den är metoden används för att skapa nya Noder
    #Metodens Inparameter är värde som är en inparamater som skickas vidare till noden    
    def enqueue(self,värde):

        #Skapar en ny nod-objekt i metoden
        nyNod=Node(värde)
        
        #Kallar på metoden i klassen som kallas isEmpty() 
        t=self.isEmpty()
        #Vilkoret nedanför används vid skapandet av första nod-objektet
        if t== True:
            self._förstaNod = nyNod
            self._sistaNod=nyNod

        #Vilkoret nedanför hänger ihop med att, vid första noden så har inte
        #nästa referens nod än tilldelats.
        t=self.isEmpty()
        if t==False and self._förstaNod.nästaNod == None:
            self._förstaNod.nästaNod=nyNod
            
        #Vilkorer hängder ihop med man ska endast tillge den nuvarande-sista-noden sin
        #sin nästa ref nod.   
        if self._sistaNod!=None:
            self._sistaNod.nästaNod=nyNod
            
        #Sistanoden blir omdefinerad som den nyaste noden.    
        self._sistaNod=nyNod
        
    def dequeue(self):
        
        #tempNod får behålla den första noden. Första noden omdefinieras som första nodens nästa nod.
        #Referenskedjan hänger kvar med nästa noden. På sätt kan man tänka sig en analogi där
        #man tar bort första noden i kön och man flyttar upp alla noder efter upp ett steg.    
        tempNod=self._förstaNod
        self._förstaNod=self._förstaNod.nästaNod
        #returnerar värdet på noden till kortricket funktionen
        #Antigen kommer den hamna längst bak i kön i en ny nod
        #eller läggas fram. 
        return  tempNod

        #Kollar om kön är tom eller inte. 
    def isEmpty(self):
        if self._förstaNod==None:
            return True
        else:
            return False
        
       

