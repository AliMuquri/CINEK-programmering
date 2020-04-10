class låtar:
    def __init__(self,artistnamn):
        self.artistnamn=artistnamn

    def __It__(self,artist):
        if self.artistnamn.lower()>artist.artistnamn.lower():
            return True
        elif self.artistnamn.lower()<artist.artistnamn.lower():
            return False
        else:
            print("LIKA")
    def __str__(self):
        return self.artistnamn

if __name__ == "__main__":
    o1=låtar("Petter")
    o2=låtar("Ali")
    print(o1.__It__(o2))
