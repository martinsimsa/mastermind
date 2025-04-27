
# Mastermind - testování algoritmů
Mastermind testování algoritmů je program, jehož hlavním cílem je testování jednokrokových algoritmů řešící hru [n,k]-Mastermind. V této dokumentaci používám značení ze své bakalářské práce s názvem Logik - algoritmy a strategie dostupné z https://github.com/martinsimsa/Bachelor-thesis-Mastermind.git. 


## Obsah
- [Soubory](#soubory)
- [Dokumentace](#dokumentace)
- [Instalace](#installation)
- [Použití](#použití)
- [Licence](#licence)
- [Kontakt](#kontakt)
- [Zdroje](#zdroje)

## Soubory
- Mastermind-testing.py
- README.md
- technical-docs.txt
- CITATION.cff

Hlavní soubor je Mastermind-testing.py. 

## Dokumentace
Technickou dokumentaci lze nalézt v souboru technical-docs.txt

## Instalace
1. Naklonujte repozitář, případně zkopírujte zdrojový kód ze souboru Mastermind-testing.py.

Clone with HTTPS:
https://github.com/martinsimsa/mastermind.git

GitHub CLI:
gh repo clone martinsimsa/mastermind

2. Nainstalujte použité knihovny

Python
- https://www.python.org/downloads/
- případně lze využít nějaký online python compiler
    - např. https://www.online-python.com/

Deque z knihovny collections
- součástí standardního balíčku pythonu

Numpy
- https://numpy.org/install/


## Použití

### Funkce get_results_of_algorithm()
Tato funkce slouží k analýze algoritmu složeného z valuace a strategie. Tvar volání funkce je následující:

get_results_of_algorithm(n, k, první tah, valuace, strategie, výběr z kandidátů)
- n - počet pozic
- k - počet barev
- první tah - pevně zvolený první tah, např pro n = 4, k = 6 [1,1,2,3]
- valuace - použitá valuace
- strategie - použitá strategie
- výběr z kandidátů - True - algoritmus vybírá pouze z kandidátů, False - algoritmus vybírá ze všech kódů.


Přípustné kombinace valuace a strategie jsou:
- find_max, lower_is_better - algoritmus Min-max
- find_entropy, higher_is_better - algoritmus Max entropy
- find_number_of_parts, higher_is_better - algoritmus Most parts.

Příklad použití:
- get_results_of_algorithm(4, 6, [1,1,2,2], find_entropy, higher_is_better, False)

### Funkce solve_one_game()
Funkce solve_one_game slouží ke spuštění daného algoritmu pro jeden pevně určený tajný kód. Tvar volání funkce je následující:

solve_one_game(n, k, tajný kód, valuace, strategie, první tah, výběr z kandidátů)
- n - počet pozic
- k - počet barev
- tajný kód - tajný kód ve tvaru seznamu, např pro n = 4, k = 6 [5,1,6,3]
- valuace - použitá valuace
- strategie - použitá strategie
- první tah - pevně zvolený první tah, např pro n = 4, k = 6 [1,1,2,3]
- výběr z kandidátů - True - algoritmus vybírá pouze z kandidátů, False - algoritmus vybírá ze všech kódů.

Přípustné kombinace valuace a strategie jsou stejné jako výše:
- find_max, lower_is_better - algoritmus Min-max
- find_entropy, higher_is_better - algoritmus Max entropy
- find_number_of_parts, higher_is_better - algoritmus Most parts

Příklad použití:
- solve_one_game(4, 6, [5,1,6,3], find_max, lower_is_better, [1,1,2,2], False)


## Licence
This program is open to free use for all parties. No citation needed and there are no copyrights. It uses tinyxml2 [2] and boost library 



## Kontakt
Martin Šimša, MFF CUNI, 3. roč., Matematika pro informační technologie (MITP)
LS 2024/2025, Bakalářská práce na téma Logik - algoritmy a strategie
simsa.martin@email.cz, martin.simsa926@student.cuni.cz
Supervisor: doc. Mgr. Pavel Růžička, Ph.D.


## Sources
[1] https://orienteering.sport/iof/mapping/
