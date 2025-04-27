# Technická dokumentace
Tohle je technická dokumentace programu Mastermind - testování algoritmů. Byla vytvořena jako příloha k bakalářské práci Logik - algoritmy a strategie. 

## Obsah
Dokumentace obsahuje popisy jednotlivých funkcí a jejich propojení. 
- [Process](#installation)
- [Proměnné](#proměnné)
- [Funkce](#funkce)

## Proměnné
len_pegs - označuje počet pozic, v bakalářské práci tuto hodnotu značíme písmenem $n$.

len_colours - určuje počet barev (v práci jako $k$).

all_scores - seznam všech ohodnocení v $H_{n,k}$

all_codes - seznam všech kódů $H_{n,k}$

start_code - volba prvního pokusu, aby algoritmus nemusel procházet všechny kódy

possible_codes - Množina kandidátů aktuálního stavu.

partition - Množina potomků aktuální množiny kandidátů

partition_table - Velikosti množin potomků množiny kandidátů

secret_code - tajný kód

partition_table_function - proměnná uchovávající aktuálně používanou valuaci (find_max, find_entropy, find_number_of_parts)

compare_function - proměnná uchovávající aktuálně používanou strategii (higher_is_better, lower_is_better)

choose_from_candidates - proměnná, která udává, zda algoritmus vybírá kódy pro další pokusy pouze z množiny kandidátů (True), anebo z celého prostoru kódů (False)

partition_table_value - uchovává hodnotu valuace pro danou množinu kandidátů a kód.


## Funkce

#### evaluate_codes
Funkce evaluate_codes na vstupu dostane dva kódy a počet pozic a barev. Vrátí ohodnocení těchto dvou kódů. Nejprve spočítá počet černých kolíčků a počty výskytů barev v obou kódech. Následně vypočítá počet bílých kolíčků podle definice ohodnocení. 

#### generate_all_codes
Funkce generate_all_codes vygeneruje seznam všech kódů podle zadaného počtu pozic a počtu barev. Prochází všechna čísla od nuly do $k^n - 1$ a každé číslo konvertuje do kódu, který v lexikografickém pořadí odpovídá danému číslu. 

#### generate_all_scores
Tato funkce vygeneruje seznam všech možných ohodnocení pro zadaný počet pozic len_pegs. Nezohledňuje počet barev, a tedy pro dvě barvy generuje i ohodnocení, která mají lichý počet bílých kolíčků. Díky použitým valuacím a strategiím to ale na algoritmech nic nezmění.

#### find_max
Funkce pro zadané velikosti $|K_{u,r}|$ vrátí maximální hodnotu. 

#### find_entropy
Funkce pro zadané velikosti $|K_{u,r}|$ vrátí entropii tohoto rozdělení. Entropie je před vrácením výsledku zaokrouhlena na 7 desetinných míst, protože při různém pořadí výpočtu entropie se tento součet zaokrouhluje jinak a nevracel by rovnosti pro stejné rozdělení potomků.

#### find_number_of_parts
Funkce pro zadané velikosti $|K_{u,r}|$ vrátí počet neprázdných potomků.

#### lower_is_better
Tato funkce slouží na místo strategie. Porovnává hodnoty valuací a vrací pravdivostní hodnoty, zda je první množina menší než druhá. Ve výsledku napomáhá k nalezení minimální hodnoty valuace.

#### higher_is_better
Tato funkce slouží na místo strategie. Porovnává hodnoty valuací a vrací pravdivostní hodnoty, zda je první množina větší než druhá.Ve výsledku napomáhá k nalezení maximální hodnoty valuace.

#### create_next_partition
Tato funkce bere jako argumenty množinu kandidátů $K$ (possible codes) a další pokus $u$. Vrátí počty prvků v potomcích $K_{u,r}$ pro všechna ohodnocení $r \in S_{n,k}$.

#### find_best_guess
find_best_guess(possible_codes, len_pegs, len_colours, all_scores, all_codes, partition_table_function, compare_function, start_code=None, choose_from_candidates=False)

Tato funkce pro aktuální stav a zvolenou valuaci a strategii vrátí odpovídající další pokus. Vychází z proměnné possible_codes - množiny kandidátů. Projde celý prostor kódů (případně pouze množinu kandidátů) a pro každý kód (code) nalezne potomky množiny kandidátů vzhledem k tomuto kódu (temp_partition) a jejich velikosti (temp_partition_table). O to se stará funkce create_next_partition. Dále nalezne valuaci aktuálního kódu (temp_partition_table_value) a porovná ji s aktuální nejlepší hodnotou z hlediska zvolené strategie (compare_function). Ve chvíli, kdy je aktuální hodnota valuace menší, respektive větší (podle zvolené strategie) než průběžná nejlepší hodnota valuace (best_partition_table_value), program aktualizuje nejlepší hodnoty valuace, potomků a velikostí potomků. Pokud se valuace aktuálního kódu rovná průběžné nejlepší hodnotě valuace, program zkontroluje, jestli byl průběžně nejlepší kód kandidát. Pokud nebyl a aktuální kód je kandidátem, algoritmus aktualizuje nejlepší hodnoty valuace, potomků a velikostí potomků. 

Díky tomu, že algoritmy vybírají lexikograficky nejmenší kódy z množiny kódů s nejlepší valuací (případně průniku této množiny s množinou kandidátů), tak stačí uchovávat pouze první kód s nejlepší hodnotou valuace. Případně stačí kontrolovat, zda náleží do množiny kandidátů.

Ve chvíli, kdy program projde všechny kódy, ze kterých vybírá, vrátí zvolený nejlepší kód pro tento stav (best_next_guess). Společně s ním vrací i proměnné best_partition_table a best_partition. 

#### get_results_of_algorithm
Toto je hlavní funkce, která testuje algoritmy. Prochází stavový prostor a pro každý stav nalezne další pokus. Počty pokusů přičítá v případě, kdy zkoumá potomka vzhledem k ohodnocení $(n ,0)$.

#### solve_one_game
Tato funkce je implementací algoritmu $1$ v bakalářské práci. Na vstupu vezme počet pozic a barev, tajný kód, valuaci, strategii, případný pevně stanovený první pokus a True/False hodnotu, jestli se další pokus vybírá pouze z kandidátů. 

Pokud další pokus dostal maximální ohodnocení, shoduje se s tajným kódem a hra končí. 


#### get_valuation_of_first_guess
Tato funkce vrátí hodnotu valuace pro nějaký první pokus a zadanou valuaci. 

## main_function










