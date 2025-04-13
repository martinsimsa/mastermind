
# Mastermind testovani
Mastermind testování je program, jehož hlavním cílem je testování jednokrokových algoritmů řešící hru [n,k]-Mastermind.

## Table of contents
- [Contains](#contains)
- [Documentation](#documentation)
- [Installation](#installation)
- [Usage](#usage)
- [Discussion](#discussion)
- [License](#license)
- [Information](Information)
- [Sources](Sources)

## Obsah projektu
- Mastermind-testing.py
- README.md
- technical-docs.txt
- CITATION.cff

## Dokumentace
Technickou dokumentaci lze nalézt v souboru technical-docs.txt

## Instalace
1. Naklonujte repozitář

Clone with HTTPS:
https://github.com/martinsimsa/mastermind.git

GitHub CLI:
gh repo clone martinsimsa/mastermind

2. Nainstalujte použité knihovny
a) Program běží v jazyce Python
- https://www.python.org/downloads/
- případně lze využít nějaký online python compiler

b) Část deque z knihovny collections
- součástí standardního balíčku pythonu

c) Numpy
- https://numpy.org/install/


## Použití

### Prerequisites
1. In your .omap file, add precisely one start triangle (code 701) and one finish double circle (706). If desired, add at most one midpoint circle (703). [1]


### Steps
1. Open solution in Visual Studio (Route_calculator/Route_calculator.sln), run Route_calculator/Route_calculator/main.cpp file or run Route_calculator/x64/Debug/Route_calculator.exe.


## Discussion
The finding of the fastest route is optimal only in the 2D grid with 8-neighborhood. In real life, it can be possible, that the best route would go through different areas.



## License
This program is open to free use for all parties. No citation needed and there are no copyrights. It uses tinyxml2 [2] and boost library [3]. Here are their licenses:


TinyXML-2 is released under the zlib license:

This software is provided 'as-is', without any express or implied warranty. In no event will the authors be held liable for any damages arising from the use of this software.

Permission is granted to anyone to use this software for any purpose, including commercial applications, and to alter it and redistribute it freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not claim that you wrote the original software. If you use this software in a product, an acknowledgment in the product documentation would be appreciated but is not required.
2. Altered source versions must be plainly marked as such, and must not be misrepresented as being the original software.
3. This notice may not be removed or altered from any source distribution.



## Information
Martin Šimša, MFF CUNI, 3. roč., Matematika pro informační technologie (MITP)
LS 2024/2025, Bakalářská práce na téma Logik - algoritmy a strategie
simsa.martin@email.cz, martin.simsa926@student.cuni.cz
Supervisor: doc. Mgr. Pavel Růžička, Ph.D.


## Sources
[1] https://orienteering.sport/iof/mapping/
