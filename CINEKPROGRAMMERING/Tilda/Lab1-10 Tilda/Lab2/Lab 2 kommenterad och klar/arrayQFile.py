from array import array


class ArrayQ():
    #Bestämmer vad för typ av data man ska lagra
    def __init__(self):
         self._q=array("i",[])
         self._size=int(0)

    #Bestämmer stoppar in något sist (append)
    def enqueue(self,element):
            self._size+=1
            self._q.append(element)

    #Plockar ut det som står först
    def dequeue(self):
        self._size-=1
        element1=self._q.pop(0)
        return int(element1)

    #Kollar om kön är tom
    def isEmpty(self):
        if len(self._q)==0:
            return True
        else:
            return False
    def size(self):
        print("Antal element:", self._size)
