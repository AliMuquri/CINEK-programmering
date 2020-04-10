import pygame
import math
import random
import sys
import time
from pygame.locals import*

#sFaktor används för att förstora grafiken i spelet
#Hastighet används för att bestämma rörelsehastigheten för spelaren
sFaktor=25
Hastighet=5

##Klassen Hinder ärver sprite klassen från modulen Sprite. Sprite klassen har fördefinerade
##variablar och metoder som nu kan användas i Hinder.
##Jag kallar på sprite klassens konstruktor pygame.sprite.Sprite.__init__(self)
##i Hinder klassens kosntruktor. Så varje objekt av Hinder blir en objekt("Sprite") av klassen
##sprite(Som är den första klassen i modulen Sprite).
##Jag ärver ned Hinder till klasserna Doktorn/Daleks. Det medför att de
##också bli Sprites och får samma konstruktor som Hinder.
##Hinder konstruktorn har färg och hinderKoordinat som parametrar.
##Två av klass variablarna jag använder är self.image och self.rect.
##image håller en bild till spriten. Jag använder metoden pygame.surface
##för att skapa en grafiskt bild till self.image och fill() för att ge den färg.
##Sist så skapar jag en rektangel med rect där jag placerar self.image och ger den
##samma dimension med metoden self.image.get_rect(). 
##Sist i konstruktorn ger jag koordinater till rektangeln.
##Jag använder sFaktor för att förstora allt grafiskt proportionellit.
##Det betyder även var koordinaterna hamnar ändras proportionellit.

class Hinder(pygame.sprite.Sprite):
    
    def __init__(self, färg, hinderKoordinat):

        pygame.sprite.Sprite.__init__(self)
        
        self.hinderKoordinat=hinderKoordinat
        
        self.image=pygame.Surface([1*sFaktor,1*sFaktor])

        self.image.fill(färg)
        
        self.rect=self.image.get_rect()

        self.rect.x=self.hinderKoordinat[1]*sFaktor

        self.rect.y=self.hinderKoordinat[0]*sFaktor



##I klassen Doktorn så finns det en konstruktor. Trots att den ärver ned en konstruktor från Hinder.
##Vi kallar på fadder konstruktorn med Super()i Doktorns egna konstruktor. Detta görs för vi vill ha en
##partikulär instansvariabel self.startTid till Doktorn. I metoden förändring så används self.startTid
##tillsammans med lokala variablarna intervall och slutTid för att ge en 10 sekunders fördröjning mellan
##användningen av teleportering. Klassen har två klass variablar xFörändring, yFörändring. De används
##tills skapa rörelse till spelaren när han använder piltangenterna eller s-tangent för att teleportera.
##Metoden förändring har(utöver self) tre parametrar xHastighetsvärde,yHastighetsvärde, och banaInläsning.
##När metod kallas i main() så skickar den med positiva eller negativa hastighsvärden i 2D som tilldelas
##till xHastighetsvärde och yHastighetsvärde. Ifall s-tangenten används så tilldelas None till
##xHastighetsvärde,yHastighetsvärde och metoden exekverar en if-sats. Inom den generas slumpmässigt en self.x-och
##-yFörändring inom banans ramar(vilket erhålls från banaInläsning).
##Om xHastigetsvärde och yHastighetsvärde kommer med givna värden så tilldelas de till self.x-och yFörändring.

class Doktorn(Hinder):
    
    xFörändring=int()
    yFörändring=int()

    def __init__(self, färg, hinderKoordinat):
        
        self.startTid=None
        
        super().__init__(färg, hinderKoordinat)
        
    def förändring(self, xHastighetsvärde, yHastighetsvärde, banaInläsning, spelDisplay):
        
        #ScrewDriver teleport
        if xHastighetsvärde==None and yHastighetsvärde == None:
            bredd, höjd = bildaBreddochHöjd(banaInläsning)
            svart=(0,0,0)

            intervall=10
            if self.startTid!=None:
                slutTid=time.time()
                intervall=slutTid-self.startTid
            
            if intervall>=10:
                self.startTid=time.time()
                xHastighetsvärde=random.randrange(-self.rect.x,bredd*sFaktor-self.rect.x)
                yHastighetsvärde=random.randrange(-self.rect.y,höjd*sFaktor-self.rect.y)
                
                self.xFörändring=xHastighetsvärde
                self.yFörändring=yHastighetsvärde
                
                text=("ScrewDriver Teleport")
                meddelandeDisplay(text,40, bredd, höjd, spelDisplay, svart)
                pygame.display.update()
                time.sleep(0.5)
                
            else:
                timer=str(int(round(10-intervall)))

                text=("ScrewDriver Teleport kan upprepas om "+ timer + " sekunder")
                meddelandeDisplay(text,30, bredd, höjd, spelDisplay, svart)
                pygame.display.flip()
                time.sleep(0.5)
                pass
            
        else:
            self.xFörändring=xHastighetsvärde
            self.yFörändring=yHastighetsvärde
            
##metoden rörelse används för att tillämpa self.x och y förändringarna till
##koordinater av doktorn self.rect.x och self.rect.y.  Metoden använder en
##sprite metod pygame.sprite.spritecollide() för att upptäcka kollisioner mellan sprites 
##Då kontrolleras self(spriten ifråga) mot en grupp av sprites, därmed använder man den första
##parametern hinderSprites. Det är en spriteklassgrupp som håller alla sprites av en typ. Algoritmen
##nedan stället om koordinaterna för self efter riktningen som den rörde sig ifall kollision upptäcks.
##Den andra parametern dubbelRörelse används för att förhindra att addera värden till koordinaterna
##dubbelt så mycket p.g.a. att man kallar på rörelse metoden en gång till i samma loop. Det gör man
## för attanvända kollision algoritmerna igen för när doktorn går på skrot. 

##Jag har tagit iden från http://programarcadegames.com/python_examples/show_file.php?file=move_with_walls_example.py
    def rörelse(self, hinderSprites, dubbelRörelse):
        
        if dubbelRörelse==False:

            self.rect.x += self.xFörändring

        else:
            self.rect.x += 0
           
        kollisionLista = pygame.sprite.spritecollide(self, hinderSprites, False)
        
        for kollision in kollisionLista:
          
            if self.xFörändring > 0:

                self.rect.right = kollision.rect.left

            elif self.xFörändring < 0:
                
                self.rect.left = kollision.rect.right
                    
        if dubbelRörelse==False:

            self.rect.y += self.yFörändring

        else:
            
            self.rect.y += 0
            
        kollisionLista = pygame.sprite.spritecollide(self, hinderSprites, False)

        for kollision in kollisionLista:
            
            if self.yFörändring > 0:
            
                self.rect.bottom = kollision.rect.top
            
            elif self.yFörändring < 0:
                
                self.rect.top = kollision.rect.bottom
                


##Klassen Daleks ärver ned allt från samtliga klasser. Den har en klassvariabel skrot som verifierar
##om daleksen lever eller är skrot. Det bestämmer om x-och yförändring får en hastighets eller inte.
##I metoden rörmotspelare används en vektoriserad rörelse som beräknar den kortaste fågelvägen, distansen,
##mot spelaren och flyttar daleken närmare doktorn med en given Hastighet.
##Det är därför den har parametern doktorSpelare. Metoden använder sig av metoden math.hypot för att räkna distansen.
##Den innehåller också en if-sats för att förhindra noll-division om distansen skulle vara för kort. Observera! Att här
##ges bara förändring till Daleks koordinaterna men själva tillämpandet görs i metoden rörelse ovanför.

class Daleks(Doktorn):
        
    skrot=False

    def rörmotSpelare(self, doktorSpelare):

        if self.skrot==False:
            
            
          
            Hastighet=2
            
            dx, dy = self.rect.x - doktorSpelare.rect.x, self.rect.y - doktorSpelare.rect.y

            distans=math.hypot(dx,dy)

            if distans==0:
                distans=1

            dx, dy = dx/distans, dy/distans


            self.xFörändring= -dx*Hastighet
            
            self.yFörändring= -dy*Hastighet

            
        else:
            
            self.xFörändring=0

            self.yFörändring=0

##Den här klassen används för att bevara den filbana som ges i start så den kan lättare
##laddas upp igen vid omstart.Konstruktorn sparar filen och geBana metoden ger den filbanan
        
class TemporärBana():
    def __init__(self, filBana):
        self.filBana=filBana
    def geBana(self):
        return self.filBana
    
## Funktionen välja bana används i två sammanhang. Vid start och omstart. I main() kallas
##funktion med parametern None. Det betyder att bana har ännu inte givit alltså start. Det exekverar den första
##if-satsen annars så går den till nästa med else.
##Funktionen har en lista banaInläsning som sparar den inlästa banan så att varje element är en rad.
##Den har också en boolen variabel felfri som ändras om fel upptäcks med filen
##Utöver den finns det en try-exception som ska fånga felen om filen inte kan hittas
##Resten av funktion består av algoritmer som bestämmer om banan har fel antal rader, fel bredd på radderna eller
##fel tecken. I for satserna hittar vi fel algoritmen. Varje gång en fel är upptäckt ställs felfri till false.
##Så länge felfri är True så fortsätter satserna.
##banaInläsning, filbana och och startText returners i den här metoden. De två sista parametrarna
## tas med för omstarten. filbana innehåller namnet på banan som ska öppnas och startText innehåller
## en boolean som anger om instruktioner i början ska visas eller skippas.

def väljaBana(bana):
    banaInläsning=list()
    felfri=False
    startText=True
    while not felfri:
        felfri=True
        try:
            if  bana== None:
                filBana=input("Ange filnamn på din spelbana. Avsluta med format .txt: ")
                filBanaÖppna=open(filBana, "r", encoding='latin-1')
                banaInläsning=filBanaÖppna.readlines()
                filBanaÖppna.close()
                k=0
            else:
                filBana=bana
                filBanaÖppna=open(filBana, "r", encoding='latin-1')
                banaInläsning=filBanaÖppna.readlines()
                filBanaÖppna.close()
                startText=False
                k=0
            for radText in banaInläsning:
                banaInläsning[k]=radText.strip('\n').strip('').upper()
                k+=1
            for i in range(len(banaInläsning)-1):
                if len(banaInläsning[i])!=len(banaInläsning[len(banaInläsning)-1]):
                    print("Labyrintfel!: Bredden av raderna är olika")
                    felfri=False
            if felfri==False:
                pass
            else: 
                for i in range(k):
                    if felfri==True:
                        for m in range(len(banaInläsning[i])):
                            if felfri==True and banaInläsning[i][m]=='*' or banaInläsning[i][m]=='A' or banaInläsning[i][m]=='D' or banaInläsning[i][m]=='#' or banaInläsning[i][m]=='.':
                                pass
                            else:
                                print("Labyrintfel!: Okänt tecken")
                                print(banaInläsning[i][m])
                                felfri=False
                                break
                    else:
                        print("Gör om filen, endast .,*, #, A, D tecken får finnas med")
                        break
        except FileNotFoundError:
            print("Filen kan inte hittas! \nKontrollera att du har skrvit in rätt filnamn eller format")
            felfri=False
            
    return banaInläsning, filBana, startText

#Funktionen beräknar längden på axlarna tilll skärmen och returnerar dem. 
def bildaBreddochHöjd(banaInläsning):
    bredd=len(banaInläsning[0])
    höjd=len(banaInläsning)
    
    return bredd, höjd

#En funktion som sållar genom listan med banaInläsning och söker efter givet 'sök-tecken'
#Och skickar tillbaka koordinaterna av det eftersökta tecknet i en lista.
def hittaInitialPosition(banaInläsning,sök):
    ramX=len(banaInläsning[0])
    ramY=len(banaInläsning)
    koordinater=list()

    for y in range(ramY):
        for x in range(ramX):
            if banaInläsning[y][x] == sök:
                koordinater.append([y,x])
    return koordinater

## Jag har tagit det har avsnittet för meddelande på ytan från https://pythonprogramming.net/displaying-text-pygame-screen/

#Skapar en objekt-yta som innehåller meddelandet. Returnerar den objekt-ytan och dess
#rektangulära dimensioner.
def meddelandeObject(text, font, färg):
    TextSurface=font.render(text, True,färg)
    return TextSurface, TextSurface.get_rect()

#Ett funktion som tar emot en text, storlek på texten, bredd och höjd till rutan, grafiska skärmytan
#som meddalandet ska ritas på och en färg till texten.
#fonten freesanbold.ttf är det enda medföljda fonten som är tillänglig att använda
#metoden pygame.font.Font() används till bestämma fonten stil och storlek
##TextSurf och TextRect kommer från meddalandeObjekt och de innhåller en textyta objekt
##och dimensionerna av ytan.
#spelDisplay.blit() ritar över ytan med det andra ytan från meddelandeObjekt
def meddelandeDisplay(text,storlek, bredd, höjd, spelDisplay, färg):
    meddelandeFont=pygame.font.Font('freesansbold.ttf',storlek)
    TextSurf, TextRect= meddelandeObject(text, meddelandeFont, färg)
    TextRect.center=(bredd*sFaktor/2, höjd*sFaktor/2)
    spelDisplay.blit(TextSurf, TextRect)

#Main loopen                                                
def main(inBana):
    
    #Färg koder
    mörkblå=(0,0,139)
    svart=(0,0,0)
    vit=(255,255,255)
    silver=(192,192,192)
    
    #Funktion där man väljer spelbana och bildar tecken lista av innehållet.
    banaInläsning, bana, startText=väljaBana(inBana)
    
    #Hittar alla koordinater(KOO) för spelare, fiender, och hinder.
    doktorKOOLista=hittaInitialPosition(banaInläsning,'D')
    daleksKOOLista=hittaInitialPosition(banaInläsning,'A')
    hinderKOOLista=hittaInitialPosition(banaInläsning,'*')
    
    #Definerar sprite grupper.
    alla_sprites=pygame.sprite.Group()
    hinderSprites=pygame.sprite.Group()
    daleksSprites=pygame.sprite.Group()
    skrothögSprites=pygame.sprite.Group()
    rörandeSprites=pygame.sprite.Group()
        
    #Skapar instansobjekt/sprite-listor
    doktorSpelare=Doktorn(mörkblå, doktorKOOLista[0])
    daleks=list()
    hinder=list()
    for i in range(len(daleksKOOLista)):
        daleks.append(Daleks(silver, daleksKOOLista[i]))
    for i in range (len(hinderKOOLista)):
        hinder.append(Hinder(svart, hinderKOOLista[i]))
        
    #Lägger till instansobjekt-listorna/sprites till sprite grupper(andra klassen i modulen sprite)
    alla_sprites.add(doktorSpelare)
    rörandeSprites.add(doktorSpelare)
    
    for hinderobjekt in hinder:
        hinderSprites.add(hinderobjekt)
        alla_sprites.add(hinderobjekt)
        
    for dalekobjekt in daleks:
        daleksSprites.add(dalekobjekt)
        rörandeSprites.add(dalekobjekt)
        alla_sprites.add(dalekobjekt)


    #Pygame initialiseras, skapar en ruta, grafisk skärm med bredd och höjd och väljer
    #bakgrundsfärg, ger titel till skärmrutan
    pygame.init()
    bredd, höjd=bildaBreddochHöjd(banaInläsning)
    spelDisplay = pygame.display.set_mode((bredd*sFaktor, höjd*sFaktor)) 
    pygame.display.set_caption("Doktor vs Dalek")
    

    #Skapar en clock instans, väljer frekvensen.

    clock = pygame.time.Clock()
    FPS=int()
    FPS=60

    #Gör så att alla input från musen blockas
    pygame.mouse.set_visible(True)
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
    pygame.event.set_blocked(pygame.MOUSEBUTTONUP)


    Avslutaspel=False
    gameOver=False
    vinst=False
    skrot=False
    
    #Spelloop fortsätter tills man väljer att avsluta spelet(Avslutaspel=True)
    while not Avslutaspel:
        if startText==True:
            speltext=list()            
            speltext.append("Välkommen till Doktor vs Daleks! Tryck på en tangent för att fortsätta!")
            speltext.append("Hur spelar man: du styr den blåa rektangeln(Doktorn) med pil-tangenterna. Tryck på en tangent för att fortsätta!")
            speltext.append("för varje rörelse du gör så rör sig de gråa rektanglarna (Daleksen) mot doktorn. Tryck på en tangent för att fortsätta!")
            speltext.append("Spelregler: Du får inte krocka med levande Daleks och två daleks får inte krocka... Tryck på en tangent för att fortsätta!")
            speltext.append("med varandra. När två Daleks krockar så blir det kvar en skrothög. Tryck på en tangent för att fortsätta!")
            speltext.append("Doktorn kan komma i kontakt med skrothög men men det får inte Daleksen. Tryck på en tangent för att fortsätta!")
            speltext.append("Du vinner spelet om du får alla Daleks att krocka med varandra eller en skrothög. Tryck på en tangent för att fortsätta!")
            speltext.append("Tryck på en tanget för att börja spelet! Lycka till!")
            for text in speltext:
                invänta =True
                while invänta:
                    spelDisplay.fill(vit)
                    meddelandeDisplay(text,20, bredd, höjd, spelDisplay, svart)
                    pygame.display.update()
                    
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            invänta=False
            startText=False
            
            
        #När man förlorar får man välja om man vill fortsätta
        #Eller avsluta
        while gameOver == True or vinst==True:
            if vinst==True:
                text=("Vinst! Tryck på o för att spela om eller a för att avsluta")
            else:
                text=("Game Over! Tryck på o för att spela om eller a för att avsluta")
            
            spelDisplay.fill(vit)
            meddelandeDisplay(text,30, bredd, höjd, spelDisplay, svart)
            pygame.display.update()
              
            for event in pygame.event.get():
        
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_a:

                        Avslutaspel = True

                        gameOver =  False

                        vinst= False

                    elif event.key == pygame.K_o:

                    #Stänger gamla rutan
                        pygame.quit()
                        
                        main(bana)
        
        
        #pygame.event.get() metoden hämtar en lista av "events" händelser (inputs)
        #event.type använder man för att specifiera vilket typ av händelse man letar efter
        #Spelet använder tangenter för att styra och teleportera. Så vi är intresserade av
        #pygame.KEYDOWN and pygame.KEYUP , alltså när man trycker och släpper en tangent.
        #Och vi är också väldigt intresserade av event.key där vi vill specifiera
        #Våra styrtangenter till.Bara på specifica tangentern så kommer vi utföra något.
        #När någon av pil tangenterna hålls ned så kallar vi på förändrings metoden för
        #doktorn. Beroende på vilken knapp det är så skickas olika parametrar med.

        #Om man väljer att trycka på att avsluta på skärmen (pygame.QUIT()
        #Så vet den att den ska avsluta spelet
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:  
                Avslutaspel = True
                
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_LEFT:
                    doktorSpelare.förändring(-Hastighet,0,None,spelDisplay)
                elif event.key == pygame.K_RIGHT:
                    doktorSpelare.förändring(Hastighet,0,None,spelDisplay)
                elif event.key == pygame.K_UP:
                    doktorSpelare.förändring(0,-Hastighet,None,spelDisplay)
                elif event.key == pygame.K_DOWN:
                    doktorSpelare.förändring(0,Hastighet,None,spelDisplay)
                elif event.key== pygame.K_s:
                    doktorSpelare.förändring(None,None, banaInläsning,spelDisplay)

            #Stoppar spelaren när han släpper tangenten
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    doktorSpelare.förändring(0,0,None, spelDisplay)
                   

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    doktorSpelare.förändring(0,0,None, spelDisplay)
                  

            if event.type == pygame.KEYUP:
                if event.key== pygame.K_s:
                    doktorSpelare.förändring(0,0,None,spelDisplay)

        #pygame.key.get_pressed() Kollar om något tangent hålls ned och returnerar boolean värden
        # If satsen kollar om någon av dessa tangenter är någon av de nedtrycka tangenterna.
        #Därmed kan endast piltangenterna påverka Daleks rörelse.
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]==True or keys[pygame.K_RIGHT]==True or keys[pygame.K_UP]==True or keys[pygame.K_DOWN]==True:
            for dalek in daleks:
                dalek.rörmotSpelare(doktorSpelare)
                dalek.rörelse(hinderSprites,False)

                #Kollar om doktor kollideraar med någon dalek/skrotifierad dalek
                #Vid upptäckt av en kollision avgörs om det är skrothög av dalek eller
                #levande fiende och isåfall gameOver=True
                dalekLista=pygame.sprite.spritecollide(doktorSpelare, daleksSprites, False)
                for dalek in dalekLista:
                    if dalek.skrot==False:
                        gameOver=True
                    else:
                        pass
                            
                #Kollar om en dalek kolliderar med de andra daleksen.(dalek!=kollision förhindrar
                #att kolla om daleken kolliderar med sig själv. Vilket spatiellt mässigt alla dalek
                #gör. De daleks som kolliderar med daleken som det jämförs med hamnar i kollision lista.
                #Daleksen tas bort får svart färg och skrot blir True vilket markerar att den som
                #imobil skrothög. Därmed tas bort från rörandeSprites och läggs till skrothögSprites.
                #Anledningen till det är att man måste fortfarande använde de spritesen till kollisions
                #Ändamål. Vilket du kan ses i nästa for-loop. 
                #När samtliga daleks är borta från rörandeSprites så vinner man spelet via vinst=True.
                #OBS! Den sista rörandeSpriten är Doktorn.
                for dalek in daleksSprites:
                    kollision = pygame.sprite.spritecollideany(dalek, daleksSprites)
                    if kollision and dalek !=kollision:
                        dalek.skrot=True
                        dalek.image.fill(svart)
                        kollision.skrot=True
                        kollision.image.fill(svart)
                        skrothögSprites.add(dalek)
                        skrothögSprites.add(kollision)
                        rörandeSprites.remove(dalek)
                        rörandeSprites.remove(kollision)
                        daleksSprites.remove(dalek)
                        daleksSprites.remove(kollision)
                        if len(rörandeSprites)==1:
                            vinst=True
                            
                #Kollar om daleks kolliderar med skrothögar. Ifall sant så försvinner bara Daleken
                #Ur spelet men skrothögen föreblir.
                for dalek in daleksSprites:
                    kollision = pygame.sprite.spritecollideany(dalek, skrothögSprites)
                    if kollision and dalek!=kollision:
                        daleksSprites.remove(dalek)
                        rörandeSprites.remove(dalek)
                        alla_sprites.remove(dalek)
                        if len(rörandeSprites)==1:
                            vinst=True
        
                                                
        #Det här är huvudloopens skärmyta. Bakgrundet på spelet blir vit.           
        spelDisplay.fill(vit)

        #Kallar på rörelse metoden för att kontrollera gränserna mellan doktorn och hinder och doktorn och skrothögar.
        doktorSpelare.rörelse(hinderSprites, False)
        doktorSpelare.rörelse(skrothögSprites, True)

        
        #Ritar alla sprites på skärmen
        alla_sprites.draw(spelDisplay)
        
        #Ställer in Frekvensen av skärmuppdatering
        clock.tick(FPS)

        #Uppdaterar hela ytan på skärmen vid varje loop
        pygame.display.flip()
        
    #När man väljer a för avsluta så hoppar den ut spel-loopen och fortsätter efter main(None)
    pygame.quit()


#Nedanför visas först main(None) där programmet börjar och quit() där programmet avslutas.
#None parametern används i main(), för i main() kallas väljabana(None) där den anger att programmet
#Startar för första gången och ingen bana har valts
main(None)
quit()

