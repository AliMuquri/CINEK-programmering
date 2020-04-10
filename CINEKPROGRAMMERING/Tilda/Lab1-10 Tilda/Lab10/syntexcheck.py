import string
import sys
from linkedQFile import LinkedQ
from Molgrafik import *
from atomDict import*
# Klassen molekylfel är en subklass som ärver Exceptions klassens metoder
# Den här kan vi använda senare i vår try /exception.


class Syntexerror(Exception):
    pass


def readNum(q):
    strnum = q.dequeue()
    num = int(strnum)
    if num > 0:
        if not q.isEmpty():
            while q.peek().isdigit():
                strnum += q.dequeue()
                if q.isEmpty():
                    break

    if int(strnum) > 1:
        return int(strnum)

    raise Syntexerror("För litet tal vid radslutet")


def letter(q):
    l = q.peek()
    alfabet = list(string.ascii_lowercase)
    if l in alfabet:
        return True


def Letter(q):
    l = q.peek()
    alfabet = list(string.ascii_uppercase)
    if l in alfabet:
        return
    raise Syntexerror("Saknad stor bokstav vid radslutet")


def readAtom(q):
    atomer = "H   He  Li  Be  B   C   N   O   F   Ne  Na  Mg  Al  Si  P   S   Cl  Ar  K   Ca  Sc  Ti  V Cr \
Mn  Fe  Co  Ni  Cu  Zn  Ga  Ge  As  Se  Br  Kr  Rb  Sr  Y   Zr  Nb  Mo  Tc  Ru  Rh  Pd  Ag  Cd \
In  Sn  Sb  Te  I   Xe  Cs  Ba  La  Ce  Pr  Nd  Pm  Sm  Eu  Gd  Tb  Dy  Ho  Er  Tm  Yb  Lu  Hf \
Ta  W   Re  Os  Ir  Pt  Au  Hg  Tl  Pb  Bi  Po  At  Rn  Fr  Ra  Ac  Th  Pa  U   Np  Pu  Am  Cm \
Bk  Cf  Es  Fm  Md  No  Lr  Rf  Db  Sg  Bh  Hs  Mt  Ds  Rg  Cn  Fl  Lv "
    atom = ""
    atomlist = list(filter(None, atomer.split(" ")))

    Letter(q)
    atom += q.dequeue()
    if not q.isEmpty():
        if q.peek().isalpha():
            if letter(q):
                atom += q.dequeue()

    if atom in atomlist:
        return atom

    raise Syntexerror("Okänd atom vid radslutet")

# I det här steget uppfylls:<group> ::= <atom> |<atom><num> | (<mol>) <num>
# Funktione har två delar men uppfyller syntaxen tre regler
# I första delen hanteras samtliga anrop för readAtom() när bokstäver upptäcks
# i den andra delen hanteras upptäcker av paranteser och upptäckter av fel.
# Vi upptäckt av parantes ( så följs det av ytterliga stacking av funktioner genom att man kallar
# på readMolecule för att läsa innehållet i parantesen som i sin tur använder readGroup för det.
# Och som tills slut returneras till ursprunliga readGroup som vill ha en ) för att avsluta (<mol>)
# korrekt
# Att hantera att det finns siffor efter paranteser( samt att om en siffra upptäcks så
# anropas readNum() ) hanteras på båda delarna


def readGroup(q):
    rutan = Ruta()
    if q.peek().isalpha():
        rutan.atom = readAtom(q)
        if q.isEmpty():
            return rutan
        if q.peek().isdigit():
            rutan.num = readNum(q)
        return rutan

    if q.peek() == "(":
        q.dequeue()
        rutan.down = readMolecule(q)
        if q.peek() == ")":
            q.dequeue()
            if not q.isEmpty():
                if q.peek().isdigit():
                    rutan.num = readNum(q)
                    return rutan

            raise Syntexerror("Saknad siffra vid radslutet")
        else:
            raise Syntexerror("Saknad högerparentes vid radslutet")

    return rutan

# Det första steget i den rekursa nedåkningen med länkade kön så kollar vi efter
# felaktiga gruppstart i form av ) eller siffror som bryter mot syntaxen
# samt andra ogiltiga tecken.
# För att undvika beräkna paranteser så stackas anropas av funktioner samt unyttjas reskursiv anrop.
# I det här steget uppfyllls:
# <mol>   ::= <group> | <group><mol>


def readMolecule(q):
    if q.isEmpty():
        return
    if q.peek() == ")" or q.peek().isdigit():
        raise Syntexerror("Felaktig gruppstart vid radslutet")
    else:
        if not q.peek().isalpha():
            if not q.peek() == "(":
                raise Syntexerror("Felaktig gruppstart vid radslutet")
        # Här ifrån stackas anrop
        mol = readGroup(q)
        if q.isEmpty():
            return mol
        if q.peek() == ")":
            return mol
        mol.next = readMolecule(q)
        return mol
# funktion readFormel tar molekyl strängen, anropar qMaker, istället skapas
# en länkad kö av elementen i strängen.
# Vi utnyttjar en try /Exception när vi påbörjar reskursiva nedåkningen.
# Där ifall fel upptäcks längre ned så fångas felet upp och returneras
# till huvudfunktionen annars så returneras att formeln är korrekt.
# I det här steget uppfylls:
# <formel>::= <mol> \n
# En while loop utnyttjas för att se till att man inte avslutar för tidigt.


def readFormel(molecule):
    q = qMaker(molecule)
    try:
        if q.isEmpty():
            q.enqueue(" ")
        while not q.isEmpty():
            mol = readMolecule(q)

        return mol  # "Formeln är syntaktiskt korrekt"

    except Syntexerror as fel:
        t = str()
        if q.peek() != None:
            while not q.isEmpty():
                t += q.dequeue()
        return str(fel).strip() + " " + str(t)

# Funktionen används för att skapa en kö av elementen i molekylen


def qMaker(molecule):
    q = LinkedQ()
    for m in molecule:
        q.enqueue(m)
    return q

# Huvudfunktion där vi stegvis tar input tills # upptäcks
# För varje input så anropas readFormel
# Resultatet(return) av anropet av readFormel skrivs ut (ges som output)


def weight(mol, atomDict):
    w = float(0)
    if mol.atom.isalpha():
        w = float(mol.num) * float(atomDict.search(mol.atom))

    if mol.down is not None:
        w += float(mol.num) * float(weight(mol.down, atomDict))
    if mol.next is not None:
        w += float(weight(mol.next, atomDict))

    return w


def main():
    atomDict = makeAtomDict()
    line = input("Molecule: ")
    while line:
        print(line)
        if line[0] == "#":
            print("EXIT PROGRAM")
            break
        molecule = line.strip("\n")
        mol = readFormel(molecule)

        if isinstance(mol, str):
            print(mol)
            line = input("Molecule: ")
        else:
            moleculeweight = weight(mol, atomDict)
            print(moleculeweight)
            mg = Molgrafik()
            mg.show(mol)
            line = input("Molecule: ")


# Porgrammet startar här
if __name__ == "__main__":
    main()
