import datetime


class BlumBlumShub():

    def __init__(self):
        self.M = None
        self.thisGen = self.setSeed()

    def setSeed(self):
        tNow = datetime.datetime.now()
        s = str(tNow.microsecond)
        p, q = self.getPrimes()
        M = pq
        n = len(M)
        s = str(tNow.microsecond)
        while M < s:
            s = tNow.microsecond
            if n < 6:
                s = str(s)
                s = s[:n]
        self.M = M
        seed = s**2 % M
        return seed


    def getPrimes(self):
        x, y = 1, 1
        primefile = open("prime.txt", 'r')
        primetext = primefile.readlines()
        while x % 4 != 3 or y % 4 != 3:
            tNow = datetime.datetime.now()
            index = str(tNow.microsecond)
            if x % 4 != 3:
                x = int(primetext[int(index[:1])].split()[int(index[4])])
            if y % 4 != 3:
                y = int(primetext[int(index[2:3])].split()[int(index[5])])
            print(x)
            print(y)
        return x, y

    def generate(self):
        x, M = self.thisGen, self.M
        self.thisGen = (x**2) mod M

        return randomN

m = BlumBlumShub()
print(m.generate())
