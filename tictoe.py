

#Generacja drzewa decyzyjnego z pliku czyli krok numer pierwszy
#W ostateczności rozważenie wszystkich opcji as-is i nawigacja
#po nich jest bardziej działająca
dec = []

with open("./tictactoe_games.csv", 'r') as plik:
    dec = plik.readlines()
    for (i, gra) in enumerate(dec):
        gra = gra[:-1]
        while gra.endswith("---"):
            gra = gra[:-3]

        match gra[0]:
            case 'X': gra += ',1'
            case 'O': gra += ',-1'
            case _: gra += ',0'

        gra = gra[2:]

        dec[i] = gra


#print(dec)

m_ruchy = ["0-0", "0-1", "0-2", "1-0", "1-1", "1-2", "2-0", "2-1", "2-2"]
ruchy = []

def print_ruch():
    print("\033[95mPola:")
    print("0-0 | 0-1 | 0-2")
    print("-----------------")
    print("0-0 | 0-1 | 0-2")
    print("-----------------")
    print("2-0 | 0-1 | 0-2\033[0m")

def print_it():
    mat = [[" ", " ", " "],[" ", " ", " "],[" ", " ", " "]]

    for (i,r) in enumerate(ruchy):
        symb = 'X' if i%2 == 0 else 'O'
        x,y = r.split('-')
        x = int(x); y = int(y)
        mat[x][y] = symb
    print(f" \033[31m{mat[0][0]} | {mat[0][1]} | {mat[0][2]}")
    print("---------")
    print(f" {mat[1][0]} | {mat[1][1]} | {mat[1][2]}")
    print("---------")
    print(f" {mat[2][0]} | {mat[2][1]} | {mat[2][2]}\033[0m")



def wykonaj(r):

    ruchy.append(r)
    m_ruchy.remove(r)


gracz = ''

while gracz != 'o':
    gracz = input("\033[33mGracz jest kółkiem czy krzyżykiem? [O/X]\033[0m\n>\t").strip().lower()
    
if gracz == 'o':
    wykonaj("0-0")
    print_it()
    print_ruch()
    
    r_gracza = ''
    while r_gracza not in m_ruchy:
        r_gracza = input("\033[33mPodaj następny legalny ruch\033[0m\n>\t")
    
    wykonaj(r_gracza)
    print_it()

