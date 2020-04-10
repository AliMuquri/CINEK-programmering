##def skapaVert(rensadLäsInfil):
##    for ord  in rensadLäsInfil:
##        graf.läggTillVert(ord)
##    jämföraVert(rensadLäsInfil)
    
#Långsammare metod att urskilja en bokstavsskillnad    
##def jämföraVert(rInfil):
##    for ord1 in rInfil:
##        for ord2 in rInfil:
##            if ord1!=ord2:
##                #Om str är lika stora
##                if abs(len(ord1)-len(ord2))==0:
##                    m=0
##                    for x in graf.hämtaVert(ord1).id:
##                        for y in graf.hämtaVert(ord2).id:
##                            if y==x:
##                                m+=1
##                    if m==2:
##                        graf.läggTillKant(graf.hämtaVert(ord1).id,graf.hämtaVert(ord2).id)
##                    
##    for ord in rInfil:
##        print(ord + "\n")
##        print(graf.hämtaVert(ord))
##        print(" ")
