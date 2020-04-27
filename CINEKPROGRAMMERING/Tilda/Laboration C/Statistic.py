import timeit
from BlumBlumShub import *
from Rule30 import*
from statistics import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import *
from PIL import Image
from math import *


class Statistic():
    def __init__(self, length, size):
        self.BBS = BlumBlumShub()
        self.Rule30 = Rule30()
        self.BBSNums, self.Rule30Nums = self.runGenerate(length, size)
        self.PRNGs = [self.BBSNums, self.Rule30Nums]
        self.freqBBS = None
        self.freqRule30 = None
        self.tableBBS = []
        self.tableRule30 = []
        self.descreptiveStats()
        self.chi2(length)
        #self.mediantest(length, size)
        self.runGraph(length)
        self.randompixelImage(size)

    def runGenerate(self, length, size):
        print("Running number generators")
        BBS = []
        Rule30 = []
        for i in range(size):
            progress = str(i / size)
            print(progress, end='\r')
            BBS.append(self.BBS.generate(length))
            Rule30.append(self.Rule30.generate(length))

        return BBS, Rule30

    def runGraph(self, length):
        print("Running Histrogram")
        # %matplotlib inline
        i = 0
        for x in self.PRNGs:
            text = "Rule30"
            plt.hist(x, bins=np.arange(length + 2) - 0.5, density=True)
            if i == 0:
                text = "BBS"
            plt.title(text)
            plt.ylabel('Frequency')
            plt.xticks(range(0, length + 2))
            i += 1
            plt.show()

    def descreptiveStats(self):
        print("Running Descreptive statistics")
        text = ""
        operands = ["median", "max", "min", "len"]
        for PRNG in self.PRNGs:
            for operation in operands:
                data = str(eval(operation + "(PRNG)"))
                set = operation + " : " + data
                if PRNG == self.BBSNums:
                    self.tableBBS.append(set)
                else:
                    self.tableRule30.append(set)
        freqB, freqR = itemfreq(self.PRNGs[0]), itemfreq(self.PRNGs[1])
        freqBBS = []
        freqRule30 = []
        for f_obs in freqB:
            freqBBS.append(f_obs[1])
        for f_obs in freqR:
            freqRule30.append(f_obs[1])
        self.freqBBS, self.freqRule30 = freqBBS, freqRule30

    def chi2(self, length):
        print("Running Chi2-test")
        dof = (length - 1)

        chiBBS, pBBS = chisquare(self.freqBBS, ddof=dof)
        chiRule30, pRule30 = chisquare(self.freqRule30, ddof=dof)
        text = "          Chisquare values  |    P-values \n"
        text += "BBS      " + str(chiBBS) + "     " + str(pBBS) + "\n"
        text += "Rule30   " + str(chiRule30) + \
            "     " + str(pRule30)
        print(text)

    def mediantest(self, length, size):
        median = size / length
        n = [median] * size
        zBBS, pBBS, medianBBS, tblB = median_test(self.freqBBS, n)
        zRule30, pRule30, medianRule30, tblR = median_test(self.freqRule30, n)
        text = "          Z- values         |    P-values  |            Medianfrequency  \n "
        text += "BBS     " + str(zBBS) + "      " + \
            str(pBBS) + "      " + str(medianBBS) + "\n"
        text += "Rule30   " + str(zRule30) + "      " + \
            str(pRule30) + "        " + str(medianRule30)
        print(text)

    def randompixelImage(self, size):
        size = int(sqrt(size))
        print(size)
        arrayBBS = np.asarray(self.BBSNums) / 256
        arrayBBS = arrayBBS.reshape(size, size)
        arrayRule30 = np.asarray(self.Rule30Nums) / 256
        arrayRule30 = arrayRule30.reshape(size, size)

        im = Image.fromarray(arrayBBS, 'L')
        im.show()
        im = Image.fromarray(arrayRule30, 'L')
        im.show()

    def __repr__(self):
        return "\n".join(["".join(str(self.tableBBS)), "".join(str(self.tableRule30))])


if __name__ == "__main__":
    while True:
        check = False
        length = 10
        size = 10000
        statistic = Statistic(length, size)
        print(statistic)
