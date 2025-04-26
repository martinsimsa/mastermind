# Technická dokumentace
Tohle je technická dokumentace programu Mastermind - testování algoritmů

## Obsah
Dokumentace obsahuje popisy jednotlivých funkcí a jejich propojení. 
- [Process](#installation)
- [Functions](#functions)
- [main_function](#main_function)
- [Global variables]

## Funkce

#### evaluate_codes
Funkce evaluate_codes na vstupu dostane dva kódy a počet pozic a barev. Vrátí ohodnocení těchto dvou kódů. Nejprve spočítá počet černých kolíčků a pčty výskytů barev v obou kódech. Následně vypočítá počet bílých kolíčků podle definice ohodnocení. 

#### generate_all_codes
Funkce generate_all_codes vygeneruje seznam všech kódů podle zadaného počtu pozic a počtu barev. Prochází všechna čísla od nuly do k^n - 1 a každé číslo konvertuje do kódu, který v lexikografickém pořadí odpovídá danému číslu. 

#### generate_all_scores
Tato funkce vygeneruje seznam všech možných ohodnocení pro zadaný počet pozic len_pegs. Nezohledňuje počet barev, a tedy pro dvě barvy generuje i ohodnocení, která mají lichý počet bílých kolíčků. Díky použitým valuacím a strategiím to ale na algoritmech nic nezmění.

#### find_max
Funkce pro zadané velikosti |K_{u,r}| vrátí maximální hodnotu. 

#### find_entropy
Funkce pro zadané velikosti |K_{u,r}| vrátí entropii tohoto rozdělení. Entropie je před vrácením výsledku zaokrouhlena na 7 desetinných míst, protože při různém pořadí výpočtu entropie se tento součet zaokrouhluje jinak a nevracel by rovnosti pro stejné rozdělení potomků.

#### find_number_of_parts
Funkce pro zadané velikosti |K_{u,r}| vrátí počet neprázdných potomků.

#### lower_is_better
Tato funkce slouží na místo strategie. Porovnává hodnoty valuací a vrací pravdivostní hodnoty, zda je první množina menší než druhá. Ve výsledku napomáhá k nalezení minimální hodnoty valuace.

#### higher_is_better
Tato funkce slouží na místo strategie. Porovnává hodnoty valuací a vrací pravdivostní hodnoty, zda je první množina větší než druhá.Ve výsledku napomáhá k nalezení maximální hodnoty valuace.

------------------------------------------------------------ Find expected size - doplnit nebo vymazat ---- ------------------------------------------------------

#### create_next_partition
Tato funkce bere jako argumenty množinu kandidátů K (possible codes) a další pokus u. Vrátí počty prvků v potomcích K_{u,r} pro všechna ohodnocení r.

#### find_best_guess
Tato funkce pro aktuální stav a zvolenou valuaci a strategii vrátí odpovídající další pokus. 

#### get_results_of_algorithm
Toto je hlavní funkce, která testuje algoritmy. Prochází stavový prostor a pro každý stav nalezne další pokus. Počty pokusů přičítá v případě, kdy zkoumá potomka s ohodnocením (len_pegs,0)


#### solve_one_game
Tato funkce je implementací algoritmu 1 v bakalářské práci. Na vstupu vezme počet pozic a barev, tajný kód, valuaci, strategii, případný pevně stanovený první pokus a True/False hodnotu, jestli se další pokus vybírá pouze z kandidátů. 

Z důvodu zrychlení algoritmu je průběžný nejlepší další pokus uchováván v průběhu prohledávání všech kódů jako dalšího pokračování. Díky tomu, že další pokus je vybírán jako lexikograficky nejmenší kód, který minimalizuje/maximalizuje valuaci, stačí si uchovávat vždy aktuální nejlepší hodnotu a fakt, jestli je aktuálně nejlepší kód kandidátem. 

Pokud další pokus dostal maximální ohodnocení, shoduje se s tajným kódem a hra končí. 


#### get_valuation_of_first_guess
Tato funkce vrátí hodnotu valuace pro nějaký první pokus a zadanou valuaci. 

## main_function





## globální proměnné
len_pegs - tato proměnná označuje počet pozic, v práci tuto hodnotu značíme písmenem n.
len_colours - tato hodnota určuje počet barev (v práci jako k).
all_scores - seznam všech ohodnocení v H_{n,k}
all_codes - seznam všech kódů H_{n,k}
start_code - volba prvního pokusu, aby algoritmus nemusel procházet všechny kódy
possible_codes - Množina kandidátů aktuálního stavu.






