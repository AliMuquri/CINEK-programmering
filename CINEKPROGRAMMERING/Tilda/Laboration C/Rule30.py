import datetime


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
        self.thisGen = self.setSeed()

    def setSeed(self):
        seed =[None]*8
        tNow = datetime.datetime.now()
        value = str(tNow.second)+str(tNow.microsecond)
        for i, val in enumerate(value):
            if int(val) % 2 == 0:
                seed[i] = 1
            else:
                seed[i] = 0

        x=seed.find(None)
        if x==-1:
            return seed
        else:
            seed[0]
            return seed

    def generate(self):

        return randomN



m = Rule30()
#print(m.generate())
