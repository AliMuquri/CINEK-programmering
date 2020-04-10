from bintreeFile import Bintree

#Läser in texten
def läsaIntext(text):
    text+=".txt"
    fil = open(text, 'r', encoding ="utf-8")
    läsInfil= fil.readlines()
    fil.close()
    return delaUppfil(läsInfil,text)

#Vilkoret delar upp den svenska/engelska texten.
#Orden rensas på tecken och mellanslag innan de läggs in
#Här testas också om någon engelskt text finns i den svenska binära trädet.
def delaUppfil(läsInfil,text):
    if text =="word3.txt":
        for ordet in läsInfil:
            ord=ordet.strip()
            sTräd.put(ord)
    elif text =="engelska.txt":
        for text in läsInfil:
            text=text.split(" ")
            for ordet in text:
                ord=ordet.strip()
                #ord=ord.replace(" ","").replace('"',"").replace("\n","").replace(".","").replace(",","").replace("!","")
                if ord not in sTräd:
                    eTräd.put(ord)
                else:
                   print("dubblet: " + ord)

#Här skapas två olika objekt av klassen bintree.
sTräd=Bintree()
eTräd=Bintree()
#Anropar funktionen läsaIntext för att skapa noder.
läsaIntext("word3")
läsaIntext("engelska")
