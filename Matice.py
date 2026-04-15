import math
from Matice_class import Matice

#//////////////////
#OŠETŘOVÁNÍ VSTUPU/
#//////////////////
def index_in_range(dolni_mez: int, horni_mez: int) -> bool:
    """přijímá dvě meze a index, vrací True pokud je index z daného rozsahu"""


#////////////////////////
#KOMUNIKACE S UŽIVATELEM/
#////////////////////////

def prijmi_matici() -> tuple[int, int, list]:  
    """přijímá uživatelský vstup, vrací počet řádků, počet sloupců a samotnou matici typu m X n"""
    velikost: str = str(input("Zadej počet řádků a počet sloupců matice oddělených mezerou ")).split(" ")
    m: int = int(velikost[0]) #počet řádků matice
    n: int = int(velikost[1]) #počet sloupců matice
    matice: list[float] = []

    for i in range(m):
        radek: list[str] = str(input("zadejte hodnoty jednotlivých prvků matice v  řádku ")).split(" ")
        for j in range(n):  
            radek[j] = float(radek[j])
        matice.append(radek)

    return m, n, matice



#////////////////
#INVERZNÍ MATICE/
#////////////////

def najdi_inverzni(matice: Matice) -> Matice: 
    """přijímá regulární čtvercovou matici, vrací inverzní matici. V opačném případě vrací None"""
    m: int = matice.pocet_radku() 
    n: int = matice.pocet_sloupcu()
    matice, jednotkova = preved_do_HST(matice)
    if not je_regularni(matice) or not(m == n): #není regulární nebo jednotková
        print("Tato matice není regulární a čtvercová, nemá inverzní matici")
        return None

    for i in range(n): #vyjedničkuje diagonálu
        pivot: float = 1/matice.hodnota(i, i)
        matice.vynasob_radek(i, pivot)
        jednotkova.vynasob_radek(i, pivot)

    for i in range(n-1, -1, -1):
        for j in range(i-1, -1, -1):
            koef: float = matice.hodnota(j, i)
            print(n, i, j)
            matice.pricti_nasobek_radku(i, j, -koef)
            jednotkova.pricti_nasobek_radku(i, j, -koef)

    return jednotkova



#/////////////////
#ZÁKLADNÍ OPERACE/
#/////////////////

def preved_do_HST(matice: Matice) -> tuple[Matice, Matice]: 
    """příjme matici, vrátí matici v horním stupňovitém tvaru a matici vytvořenou stenýma úpravama z jednotkové"""
    if je_nulova(matice): #pokud je nulová, je již v HST
        return matice, vytvor_jednotkovou(m, n)
    m, n = matice.pocet_radku(), matice.pocet_sloupcu()
    jednotkova = vytvor_jednotkovou(m, n)
    
    r = 0 #posouvá řádek jakmile se najde nenulová hodnota (potřeba pro případ nulového sloupce)
    for i in range(n): # i sleduje sloupce
        for j in range(r, m): # j sleduje řádky
            if matice.hodnota(j, i) != 0:
                matice.prohod_radky(r, j)
                jednotkova.prohod_radky(r, j)
                for k in range(r+1, m): #vynuluje sloupec
                    koef = (matice.hodnota(k, i) / matice.hodnota(r,i))
                    matice.pricti_nasobek_radku(r, k, -koef)
                    jednotkova.pricti_nasobek_radku(r, k, -koef)
                r += 1 
                break
    return matice, jednotkova



def vytvor_jednotkovou(m: int, n: int) -> Matice:
    """Přijímá počet řádků m a počet sloupců n, vrací jednotkovou matici daného typu"""
    pole = []
    for i in range(m):
        radek = []
        for j in range(n):
            radek.append(0)
        if i < n:
            radek[i] = 1
        pole.append(radek)
    matice = Matice(m, n, pole)
    return matice



#//////////////////
#VLASTNOSTI MATICE/
#//////////////////

def je_nulova(matice: Matice) -> bool:
    """příjme matici, vrátí True pokud je nulová, False pokud nenulová"""
    m: int = matice.pocet_radku()
    n: int = matice.pocet_sloupcu()
    for i in range(m):
        for j in range(n):
            if matice.hodnota(i,j) != 0:
                return False
    return True



def je_regularni(matice: Matice) -> bool:
    """příjme matici, vrátí True pokud je regulární, False pokud není"""
    m: int = matice.pocet_radku()
    n: int = matice.pocet_sloupcu()
    for i in range(n):
        if matice.hodnota(i, i) == 0:
            return False
    return True



#////////////
#DETERMINANT/
#////////////

def vsechny_permutace(n: int) -> list[list]:
    """vrátí seznam všech permutací {0, 1, ..., n-1}"""
    permutace = []
    aktualni = []
    for i in range(n):
        aktualni.append(i)
    n -= 1

    while True:
        permutace.append(aktualni.copy()) #uložíme permutaci
        j = n - 1 #najdeme j
        while j >= 0 and aktualni[j] >= aktualni[j+1]:
            j -= 1
        if j < 0:
            return permutace
        l = n #zvětšíme aktualni[j]
        while aktualni[j] >= aktualni[l]:
            l -= 1
        aktualni[j], aktualni[l] = aktualni[l], aktualni[j]
        k = j + 1 #obratíme pořadí aktualni[j+1],...,aktualni[n]
        l = n
        while k < l:
            aktualni[k], aktualni[l] = aktualni[l], aktualni[k]
            k += 1
            l -= 1



def determinant(matice: Matice) -> int: #O(n!)
    """Funkce přijímá libovolnou čtvercovou matici, vrací její determinant"""
    n: int = matice.pocet_sloupcu()
    permutace_n: list[list][int] = vsechny_permutace(n)

    det: int = 0
    for i in range(math.factorial(n)):
        clen = permutace_znamenko(permutace_n[i])
        for j in range(n):
            clen *= matice.hodnota(j, permutace_n[i][j])
        det += clen
    
    return det



def determinant_z_trojuhelnikove(matice: Matice) -> int:
    """přijímá trojúhelníkovou matici, vrací determinant matice"""
    n: int = matice.pocet_sloupcu()

    det = 1
    for i in range(n):
        det *= matice.hodnota(i, i)

    return det



def determinant_z_ERU(matice: Matice) -> int:
    """přijímá čtvercovou matici, vrací determinant matice"""
    det = 1
    if je_nulova(matice): #pokud je nulová, je již v HST
        return 0
    m, n = matice.pocet_radku(), matice.pocet_sloupcu()
    
    r = 0 #posouvá řádek jakmile se najde nenulová hodnota (potřeba pro případ nulového sloupce)
    for i in range(n): # i sleduje sloupce
        for j in range(r, m): # j sleduje řádky
            if matice.hodnota(j, i) != 0:
                matice.prohod_radky(r, j)
                if r != j:
                    det *= -1
                for k in range(r+1, m): #vynuluje sloupec
                    koef = (matice.hodnota(k, i) / matice.hodnota(r,i))
                    matice.pricti_nasobek_radku(r, k, -koef)
                r += 1 
                break

    return (det * determinant_z_trojuhelnikove(matice))



def permutace_znamenko(permutace: list[list]) -> int:
    """přijímá jednu permutaci jako list integerů, vrací znaménko permutace v závislosti na tom, zda je sudá nebo lichá"""
    n = len(permutace)
    inverze = 0
    for i in range(n): #zjistí počet inverzí v permutaci
        for j in range(i, n):
            if permutace[i] > permutace[j]:
                inverze += 1
    
    if (inverze % 2) == 0: #podle sudosti nebo lichosti počtu inverzí rozhodne o znaménku permutace
        return 1
    else:
        return -1



#///////////////////
#CRAMEROVO PRAVIDLO/
#///////////////////

def algebraicky_doplnek(matice: Matice, i_vyskrt: int, j_vyskrt: int) -> float:
    """Přijímá matici a indexy i, j jejího prvku. Vrací algebraický doplněk daného prvku"""
    matice.vyskrtni(i_vyskrt, j_vyskrt)
    det = determinant_z_ERU(matice)
    return ((-1)**(i_vyskrt + j_vyskrt)) * det


def adjungovana(matice: Matice) -> Matice:
    """přijímá matici a vrací k ní matici adjungovanou"""
    velikost = matice.pocet_radku()
    matice_seznam = []
    for i in range(velikost):
        radek = []
        for j in range(velikost):
            radek.append(algebraicky_doplnek(matice, i, j))
        matice_seznam.append(radek)
    matice2 = Matice(velikost, velikost, matice_seznam)


def inverzni_z_adjungované(matice: Matice) -> Matice:
    """přijímá regulární čtvercovou matici, vrací matici invezní k matici původní vypočítanou pomocí adjungované"""
    adj = adjungovana(matice)
    det = determinant_z_ERU(matice)
    return (adj.vynasob_matici(1/det))




#////////////////
#GLOBÁLNÍ VÝSTUP/
#////////////////

"""m, n, pseudomatice = prijmi_matici()
matice = Matice(m, n, pseudomatice)
matice.vypis()
jednotkova = vytvor_jednotkovou(matice.pocet_radku(), matice.pocet_sloupcu())
jednotkova.vypis()
inverzni = najdi_inverzni(matice)
inverzni.vypis()"""

"""vsechny_permutace = vsechny_permutace(3)
for i in vsechny_permutace:
    print(i)
permutace1 = [4, 3, 2, 1]
print(permutace_znamenko(permutace1))"""

print("Zadejte čtvercovou matici ")
m, n, pseudomatice = prijmi_matici()
matice = Matice(m, n, pseudomatice)
matice.vypis()
inverzni = najdi_inverzni(matice)
print("(zjištěno pomocí řádkových úprav) determinant matice je: " + determinant_z_ERU(matice))
print("inverzni matice: ")
print(inverzni)
print("(zjištěno z definice): determinant matice je: " + determinant(matice))