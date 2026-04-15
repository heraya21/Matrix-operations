import math

#/////////////
#Třída matice/
#/////////////

class Matice:
    """Třída reprezentuje matici typu m X n"""
    def __init__(self, m: int, n: int, matice: list) -> None:
        self.__m, self.__n, self.__matice = m, n, matice


    def prohod_radky(self, radek1: int, radek2: int) -> None:
        """prohodí radek1 s radek2 v matici"""
        self.__matice[radek1], self.__matice[radek2] = self.__matice[radek2], self.__matice[radek1]


    def vynasob_radek(self, radek: int, alpha: float) -> None:
        """vynásobí radek číslem alpha, pokud alpha je nenulové"""
        if alpha == 0:
            print("násobení nulovým číslem není povoleno")
            return
        for i in range(self.__n):
            self.__matice[radek][i] *= alpha
    

    def pricti_nasobek_radku(self, radek1: int, radek2: int, alpha: float) -> None:
        """přičte alpha-násobek radek1 k radek2"""
        for i in range(self.__n):
            self.__matice[radek2][i] += (self.__matice[radek1][i] * alpha)


    def vynasob_matici(self, alpha: float):
        """vynásobí všechny řádky matice stejným číslem alfa"""
        for i in range(self.__m):
            self.vynasob_radek(i, alpha)


    def pocet_radku(self) -> int:
        """vrátí počet řádků matice"""
        return self.__m
    
    
    def pocet_sloupcu(self) -> int:
        """vrátí počet sloupců matice"""
        return self.__n
    

    def vyskrtni(self, i_vyskrt: int, j_vyskrt: int):
        """vyškrtne i-tý řádek a j-tý sloupec matice"""
        self.__matice.pop(i_vyskrt) #vyskrtne i-tý řádek
        self.__m -= 1
        for i in range(self.__m):
            self.__matice[i].pop(j_vyskrt) #vyškrtne j-tý sloupec


    def nahrad_sloupec(self, j_nahrad: int, b: Matice):
        """nahradí j-tý sloupec matice vektorem b"""
        

    def vypis(self) -> None:
        """vypíše matici po řádcích"""
        nejvice_cislic: int = len(str(self.__matice[0][0])) 
        for i in range(self.__m): #cyklus zjišťuje, kolik místa může zabrat prvek matice pro následné hezké zobrazení
            for j in range(self.__n):
                if len(str(self.__matice[i][j])) > nejvice_cislic:
                    nejvice_cislic = len(str(self.__matice[i][j]))

        for i in range(self.__m):
            for j in range(self.__n): #vypíše před každým prvkem potřebné množství mezer pro správné zarovnání pod sebe
                print(" " * (nejvice_cislic - len(str(self.__matice[i][j]))) + str(self.__matice[i][j]), end=" ")
            print()
        print()


    def __str__(self) -> str:
        vypis: str = ""
        for i in range(self.__m):
            for j in range(self.__n):
                vypis += str(self.__matice[i][j]) + " "

        return vypis
    

    def hodnota(self, radek: int, sloupec: int) -> float:
        """vrátí hodnotu matice v řádku radek sloupci sloupec"""
        return self.__matice[radek][sloupec]


