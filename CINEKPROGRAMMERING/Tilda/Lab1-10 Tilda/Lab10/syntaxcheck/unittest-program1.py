import unittest
import sys
from syntexcheck import readFormel


# Importerar modulen unittest och metoden readFormel från modulen
# syntextcheck.


# Subklassen SyntaxText ärver verktyg/metoder från unittest.TestCase
# Vi vill komma åt metoden assertEqual(x,y, msg) som tar två parametrar för test
# och jämför om de är lika. Den sista parametern msg ska bestämmas om
# man vill en särskilt meddelande ska ges om testet misslyckas.

class SyntaxTest(unittest.TestCase):
    # molekyler=["H2","cr12","Cr0", "Pb1", "Mn4"]

    # Nedanför testas alla möjliga Exception meddelande i testprogramm
    # Alla molekyler valda kommer ge utslag för det specifika exception
    def testSyntaxKorrekt(self):
        file = open("SampleOutput1.txt", 'r', encoding="utf-8")
        for line in sys.stdin:
            if line[0] == "#":
                break
            molecule = line.strip("\n")
            Output = file.readline().strip("\n")
        self.assertEqual(readFormel(molecule), Output)

        file.close()


# Startar programmet. Om vi gör det här programmet som main så
# tilldelar python den här filen i sin inbyggda variabel __name__ == '__main_'
if __name__ == '__main__':
    unittest.main()
