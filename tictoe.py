#Generacja drzewa decyzyjnego z pliku czyli krok numer pierwszy
class Korzen:
    def __init__(self, name):
        self.nazwa = name
        self.dzieci = []

    def add(self, kij):
        self.dzieci.append(kij)

    def dziecko_z_nazwa(self, name):
        wynik: Korzen = None
        for dzieck in self.dzieci:
            if dzieck.nazwa == name:
                wynik = dzieck
        return wynik
    

class Patyk(Korzen): #Że w sensie gałąź. Dziedziczenie z korzenia ma sens tylko obiektowo
    def __init__(self, name, parent):
        self.rodzic = parent
        super().__init__(name)
        parent.add(self)

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
    print("1-0 | 1-1 | 1-2")
    print("---------------")
    print("2-0 | 2-1 | 2-2\033[0m")

ostatni = punkt_startowy
def wykonaj(r, symb):
    global mat
    global m_ruchy
    global ostatni
    global 勝者
    
    ostatni = ostatni.dziecko_z_nazwa(r)
    m_ruchy.remove(r)

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

def minimax(galaz, maxxing):
    if isinstance(galaz, Lisc):
        return galaz.value

    if maxxing:
        wartosc = -99999
        for child in galaz.dzieci:
            wartosc += max(wartosc, minimax(child, False))
            x,y = map(int, galaz.nazwa.split('-'))
            gracza = 0
            if x == 1 == y:
                gracza += 1 if mat[0][0] == gracz else 0
                gracza += 1 if mat[2][2] == gracz else 0
                gracza += 1 if mat[0][2] == gracz else 0
                gracza += 1 if mat[2][0] == gracz else 0
            for n in range(3):
                gracza += 1 if mat[n][y] == gracz else 0
                gracza += 1 if mat[x][n] == gracz else 0
            wartosc += gracza
        return wartosc

    else: 
        wart = 99999
        for child in galaz.dzieci:
            wart -= min(wart, minimax(child, True))
            x,y = map(int, galaz.nazwa.split('-'))
            gracza = 0
            if x == 1 == y:
                gracza -= 1 if mat[0][0] == gracz else 0
                gracza -= 1 if mat[2][2] == gracz else 0
                gracza -= 1 if mat[0][2] == gracz else 0
                gracza -= 1 if mat[2][0] == gracz else 0
            for n in range(3):
                gracza -= 1 if mat[n][y] == gracz else 0
                gracza -= 1 if mat[x][n] == gracz else 0
            wart += gracza
        return wart

while gracz != 'O' and gracz != 'X':
    gracz = input("\033[33mGracz jest kółkiem czy krzyżykiem? [O/X]\033[0m\n>\t").strip().upper()
    
def runda_AI():
    global m_ruchy

    opcje = []
    for mozliwy in ostatni.dzieci:
        opcje.append((mozliwy.nazwa, minimax(mozliwy, True)))
        
    print(opcje)
    ruch = max(opcje, key = lambda x: x[1])[0]
    niegracz = 'O' if gracz == 'X' else 'X'
    wykonaj(ruch, niegracz)


def print_drzew(node, poziom, count):
    lista = []
    for n in node.dzieci:
        lista.append(n.nazwa)
        print(lista)
        if poziom > 1:
            print_drzew(n, poziom - 1, count + 1)

with open("./tictactoe_games.csv", 'r') as plik:
    print("Generowanie drzewa decyzyjnego z pliku...")
    for (i, gra) in enumerate(plik.readlines()):
        gra = gra[:-1]
        if i == 0: 
            continue

        poprzednik: Korzen = punkt_startowy
        giera = gra.split(',')
        for (n, ruch) in enumerate(giera):
            if ruch == '---':
                continue
            if n == 0:
                match ruch:
                    case '-': ostatnik = 0
                    case 'X':
                        ostatnik = 1 if gracz == 'O' else -1
                    case 'O':
                        ostatnik = 1 if gracz == 'X' else -1
                continue

            istniejacy = poprzednik.dziecko_z_nazwa(ruch)
            if istniejacy is not None:
                galaz = istniejacy
            else:
                if n == 9 or giera[n+1] == "---":
                    galaz = Lisc(ruch, poprzednik, ostatnik)
                else:
                    galaz = Patyk(ruch, poprzednik)
            poprzednik = galaz
                

if gracz == 'O':
    wykonaj("0-0", 'X')

#Pętla rozgrywki
while len(m_ruchy) > 0 and 勝者 == '':
    runda_gracza()
    if 勝者 != '' or len(m_ruchy) == 0:
        break
    runda_AI()

if len(m_ruchy) == 0:
    print("Remis")
else:
    print(f"\033[92mZwycięzcą jest {勝者}\033[0m")
