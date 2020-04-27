import datetime
import math


primefile = open("prime.txt", 'r')
primetext = primefile.readlines()


class BlumBlumShub():

    def __init__(self):
        self.M = None
        self.thisGen = None

    def setSeed(self):
        tNow = datetime.datetime.now()
        p, q = self.getPrimes()
        M = p * q
        n = len(str(M))
        s = tNow.microsecond
        while M < s:
            tNow = datetime.datetime.now()
            s = tNow.microsecond
            if n < 6:
                s = str(s)
                s = int(s[:n])
        self.M = M
        seed = s**2 % M
        return seed

    def getPrimes(self):
        x, y = 1, 1

        while x % 4 != 3 or y % 4 != 3:
            if x % 4 != 3:
                tNow = datetime.datetime.now()
                index1 = tNow.second
                if index1 > 9:
                    index1 = int(str(index1)[1])
                index = int(str(tNow.microsecond)[:2])
                x = int(primetext[index].split()[index1])

            if y % 4 != 3:
                tNow = datetime.datetime.now()
                index1 = tNow.second
                if index1 > 9:
                    index1 = int(str(index1)[1])
                index = int(str(tNow.microsecond)[:2])
                y = int(primetext[index].split()[index1])

            if x == y:
                x, y = 1, 1

        return x, y

    def generate(self, length):
        n = math.floor(math.log2(length)) + 1
        check = True
        self.thisGen = self.setSeed()
        x, M = self.thisGen, self.M
        while check:
            seq = []
            for i in range(n):
                self.thisGen = (x**2) % M
                seq.append(self.thisGen)
                if x == self.thisGen:
                    self.thisGen = self.generate()
                    return self.thisGen
                x = self.thisGen

            newNum = ""
            for par in seq:
                if int(par) % 2 == 0:
                    newNum += "1"
                else:
                    newNum += "0"
            self.thisGen = int(newNum, 2)
            if self.thisGen <= length:
                check = False
        return self.thisGen
