
from BlumBlumShub import *
from Rule30 import*
from statistics import *
import numpy as np
from scipy import misc


class Statistic():
    def __init__(self,length,size):
        self.BBS=BlumBlumShub()
        self.Rule30=Rule30()
        self.BBSNums, self.Rule30Nums= self.generate(length,size)
        self.PRNGs=[self.BBSNums,self.Rule30Nums]
        self.tableBBS=[]
        self.tableRule30=[]
        self.descreptiveStats()
        self.chi2()

    def generate(self,length,size):
        BBS=[]
        Rule30=[]
        for i in range(size):
            BBS.append(self.BBS.generate(length))
            Rule30.append(self.Rule30.generate(length))
        return BBS, Rule30

    def descreptiveStats(self):
        text=""
        operands=["stdev","mean","multimode","max","min"]

        for PRNG in self.PRNGs:
            for operation in operands:
                data=str(eval(operation+"(PRNG)"))
                set=operation+" : " +data
                if PRNG==self.BBSNums:
                    self.tableBBS.append(set)
                else:
                    self.tableRule30.append(set)
    def chi2(self):
        chisquare(self.BBSNums),chisquare(self.Rule30)
    def __repr__(self):
        return "\n".join(["".join(str(self.tableBBS)), "".join(str(self.tableRule30))])
if __name__=="__main__":
    length=100
    size=100
    statistic=Statistic(length,size)
    print(statistic)
