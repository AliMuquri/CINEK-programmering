from grafFilen import Graf

Ord=["tre", "öre", "tri", "tro", "trå" ,"trä"]

graf=Graf()

for ord1 in Ord:
    print(graf.läggTillVert(ord1))

for ord1 in Ord:
    for ord2 in Ord:
        if ord1!=ord2 and abs(len(ord1)-len(ord2))<=1:
            m=0
            for x in graf.hämtaVert(ord1).id:
                for y in graf.hämtaVert(ord2).id:
                    if y==x:
                        m+=1
            if m==2:
                graf.läggTillKant(graf.hämtaVert(ord1).id,graf.hämtaVert(ord2).id)
                
                                    
for ord1 in Ord:
    print(graf.hämtaVert(ord1))
    
