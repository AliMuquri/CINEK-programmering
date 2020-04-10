from bintreeFile import Bintree

def läsaIntext():
    fil = open("word3.txt", 'r')
    läsInfil= fil.readlines()

    return delaUppfil(läsInfil)

def delaUppfil(läsInfil):
    for ordet in läsInfil:
        ord=ordet.strip()
        b.put(ord)

b=Bintree()
läsaIntext()
b.write()
