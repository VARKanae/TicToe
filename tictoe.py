#Generacja drzewa decyzyjnego z pliku czyli krok numer pierwszy
class Korzen:
    def __init__(self, name):
        self.nazwa = name
        self.dzieci = []

    def add(self, kij):
        self.dzieci.append(kij)

    def dziecko_z_nazwa(self, name):
        for dzieck in self.dzieci:
            if dzieck.nazwa == name:
                return dzieck

class Patyk(Korzen): #Że w sensie gałąź. Dziedziczenie z korzenia ma sens tylko obiektowo
    def __init__(self, name, parent):
        self.rodzic = parent
        super().__init__(name)
        super().add(self)

class Lisc(Patyk):
    def __init__(self, name, parent, heur):
        self.value = heur
        super().__init__(name, parent)


punkt_startowy = Korzen("Start")    
gracz = ''

m_ruchy = ["0-0", "0-1", "0-2", "1-0", "1-1", "1-2", "2-0", "2-1", "2-2"]
mat = [[" ", " ", " "],[" ", " ", " "],[" ", " ", " "]]
勝者 = ''

def print_ruch():
    print("\033[95mPola:")
    print("0-0 | 0-1 | 0-2")
    print("---------------")
    print("0-0 | 0-1 | 0-2")
    print("---------------")
    print("2-0 | 0-1 | 0-2\033[0m")

ostatni = punkt_startowy
def wykonaj(r, symb):
    global mat
    global m_ruchy
    global ostatni
    
    ostatni = ostatni.dziecko_z_nazwa(r)

    x,y = r.split('-')
    x = int(x); y = int(y)
    mat[x][y] = symb

    print(f" \033[31m{mat[0][0]} | {mat[0][1]} | {mat[0][2]}")
    print("-----------")
    print(f" {mat[1][0]} | {mat[1][1]} | {mat[1][2]}")
    print("-----------")
    print(f" {mat[2][0]} | {mat[2][1]} | {mat[2][2]}\033[0m")

    #Sprawdzenie warunku wygranej:
    #skos
    if mat[0][0] == mat[1][1] == mat[2][2] != " " or mat[0][2] == mat[1][1] == mat[2][0] != " ":
        勝者 = "gracz" if mat[1][1] == gracz else "AI"
    #pozostałe
    for n in range(3):
        if mat[0][n] == mat[1][n] == mat[2][n] != " " or mat[n][0] == mat[n][1] == mat[n][2] != " ":
            勝者 = "gracz" if mat[n][n] == gracz else "AI"


def runda_gracza():
    global m_ruchy
    print_ruch()
    
    r_gracza = ''
    while r_gracza not in m_ruchy:
        r_gracza = input("\033[33mPodaj następny legalny ruch\033[0m\n>\t")
    
    wykonaj(r_gracza, gracz)


while gracz != 'O' and gracz != 'X':
    gracz = input("\033[33mGracz jest kółkiem czy krzyżykiem? [O/X]\033[0m\n>\t").strip().upper()
    
if gracz == 'O':
    wykonaj("0-0", 'X')
    

#Po zdefiniowaniu gracza, budujemy drzewo.
utworzone_lvl = [0, [], [], [],[], [], [],[], [], []]

with open("./tictactoe_games.csv", 'r') as plik:
    for (i, gra) in enumerate(plik.readlines()):
        if i == 0: 
            continue

        poprzednik: Korzen = punkt_startowy
        for (n, ruch) in enumerate(gra.split(',')):

            if ruch == '---':
                break

            if n == 0:
                match ruch:
                    case '-': ostatnik = 0
                    case 'X':
                        ostatnik = 1 if gracz == 'O' else -1
                    case 'O':
                        ostatnik = 1 if gracz == 'X' else -1
                continue

            galaz = Patyk(ruch, poprzednik) if n != 9 else Lisc(ruch, poprzednik, ostatnik)
            poprzednik = galaz
                

#Pętla rozgrywki
while len(m_ruchy) > 0 and 勝者 == '':
    runda_gracza()
    runda_AI()

if len(m_ruchy) == 0:
    print("Remis")
