from bintreeFile import Bintree

def läsaIntext():
    fil = open("word3.txt", 'r')
    läsInfil= fil.readlines()

    return delaUppfil(läsInfil)

def delaUppfil(läsInfil):
    for ordet in läsInfil:
        ord=ordet.strip()
        if ord in b:
            print("Dubblet:", ord)
        else:
            b.put(ord.replace("\n",""))

b=Bintree()
läsaIntext()
