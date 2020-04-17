import datetime
import math


class Rule30():

    def __init__(self):
        self.rule30 = {
            "111": "0",
            "110": "0",
            "101": "0",
            "100": "1",
            "011": "1",
            "010": "1",
            "001": "1",
            "000": "0"
        }

        self.thisGen=None
    def setSeed(self,n):
        seed =[None]*n
        value=""
        while len(value) <=n-1:
            tNow = datetime.datetime.now()
            value += str(tNow.microsecond)

        if len(value)>n:
            value=value[:n]

        for i, val in enumerate(value):
            if int(val) % 2 == 0:
                seed[i] = "1"
            else:
                seed[i] = "0"
        return seed

    def generate(self,length):
        n=math.floor(math.log2(length))+1

        check=True
        while check:
            self.thisGen=self.setSeed(n)
            newGen=[None]*n
            seed=self.thisGen
            i=0
            for s in range(3,n+1):
                newGen[s-2]=self.rule30["".join(seed[i:s])]
                i+=1
            end=n-1
            if int("".join(newGen[1:end-1]))%2==0:
                newGen[0]="0"
            else:
                newGen[0]="1"
            if int("".join(newGen[:end-1]))%2==0:
                newGen[end]="1"
            else:
                newGen[end]="0"
            self.thisGen=newGen
            randomNr=int("".join(newGen),2)
            if randomNr<=length:
                check=False

        return randomNr
