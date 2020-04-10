from arrayQFile import ArrayQ
#Importera modul

#Funktion används för att mata in kortdata 1-13 efter
#man har anget antalet kort man vill ange.

def mataIn():
    #Ange antalet kort
    kortAntalet=int(input("Ange antalet kort: "))

    #Inmata ordningen korten
    # Korrekta sekvensen
    #[7, 1, 12, 2, 8, 3, 11, 4, 9, 5, 13, 6, 10]

    #Algoritmen nedanför används endast för syfte av att
    #skriva ut rätt ändelser.

    for i in range(1,(kortAntalet+1)):
        if i <3:
            text=input("skriv in " + str(i) + ":a kortet:")
        elif i < 5:
            text=input("skriv in " +str(i) + ":e kortet:")
        elif i < 8 or 11 <= i < 13:
            text=input("skriv in " +str(i) + ":te kortet:")
        elif i < 11 or i==13:
            text=input("skriv in " +str(i) + ":nde kortet:")

        #Efter man har angivit ett tal för kortet så
        # anropar man på enqueue metoden och den läggs
        #sist i kön
        q.enqueue(int(text))
    #funktionen returnerar kortAntalet i syfte till att
    #skicka med information till nästa funktion kortttricker
    return kortAntalet

    #korttricket ska "simulera" att översta kortet läggs längst ned
    #i kortleken och den nästa kortet läggs fram.
def korttricket(kortAntalet):
    for i in range(1,2*(kortAntalet+1)-1):
        if (i%2)==0:
            print(q.dequeue())
            #q.size() för att testa metoden
        else:
            q.enqueue(q.dequeue())


#Startar programmet i huvudprogrammet

if __name__ == "__main__":
    #Skapar en ArrayQ objekt
    q=ArrayQ()
    #anropar funktionen mataIn() som returnerar kortAntalet
    #som blir en in parameter till funktionen korttricket.
    korttricket(mataIn())
