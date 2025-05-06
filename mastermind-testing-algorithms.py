import numpy as np
from collections import deque


# Vrati ohodnoceni dvou kodu
def evaluate_codes(first_code, second_code, len_pegs, len_colours):
    b = 0
    w = 0
    first_code_colours = [0]*(len_colours)
    second_code_colours = [0]*(len_colours)
    # Nalezne pocet cernych kolicku a vyskyty barev v obou kodech
    for i in range(len_pegs):
        first_code_colours[first_code[i]-1] += 1
        second_code_colours[second_code[i]-1] += 1
        if first_code[i] == second_code[i]:
            b = b+1
    if b == len_pegs:
        return [b,w]
    # nalezne pocet bilych kolicku
    w = -b
    for i in range(len_colours):
        w += min(first_code_colours[i],second_code_colours[i])
    return [b,w]


# Generuje cely prostor kodu
def generate_all_codes(len_pegs, len_colours):
    len_possible_codes = len_colours**len_pegs
    possible_codes = []
    for number in range(len_possible_codes):
        code = [0]*len_pegs
        for j in range(len_pegs):
            next_digit = int(number % len_colours)
            if len_colours != 2:
                code[len_pegs-1-j] = next_digit
            else:
                code[len_pegs-1-j] = next_digit
            number -= next_digit
            number = int(number/len_colours)
        possible_codes.append([i+1 for i in code])
    return possible_codes
               

# Generuje vsechna ohodnoceni pro dany pocet pozic
def generate_all_scores(len_pegs:int):
    all_scores:list[list[int]] = []
    for nb in range(len_pegs+1):
        for nw in range(len_pegs+1-nb):
            if nb == len_pegs - 1 and nw == 1:
                continue
            else:
                all_scores.append([nb,nw])
    return all_scores


# Nalezne maximalni pocet prvku potomka (Knuth)
def find_max(partition_table):
    return max(partition_table)


# Nalezne entropii potomku (Neuwirth)
def find_entropy(partition_table):
    code_count = sum([partition_table[i] for i in range(len(partition_table))])
    entropy = 0
    for i in range(len(partition_table)):
        if partition_table[i] != 0:
            entropy += partition_table[i]/code_count * np.emath.logn(2,code_count/partition_table[i])
    return np.round(entropy, 7)


# Nalezne pocet neprazdnych potomku (Kooi)
def find_number_of_parts(partition_table):
    len_parts = 0
    for i in range(len(partition_table)):
        if partition_table[i] != 0:
            len_parts += 1
    return len_parts


# Funkce pro strategii minimum, vraci True, kdyz je prvni hodnota mensi nez druha
def lower_is_better(first, second):
    if first < second:
        return True
    else:
        return False


# Funkce pro strategii maximum, vraci True, kdyz je prvni hodnota vetsi nez druha
def higher_is_better(first, second):
    if first > second:
        return True
    else:
        return False


# Pro danou mnozinu kandidatu vraci potomky vzhledem k danemu kodu a jejich velikosti
def create_next_partition(next_guess, possible_codes, len_pegs, len_colours, all_scores):
    partition_table = [0]*len(all_scores)
    partition = [[] for i in range(len(all_scores))]
    for code in possible_codes:
        temp_score = evaluate_codes(code, next_guess, len_pegs, len_colours)
        index_of_temp_score = all_scores.index(temp_score)
        partition_table[index_of_temp_score] += 1
        partition[index_of_temp_score].append(code)
    return partition_table, partition


# Nalezne nejlepsi pokus pro dany stav, valuaci a strategii, vraci tento pokus, velikosti mnozin potomku a mnoziny potomku
def find_best_guess(possible_codes, len_pegs, len_colours, all_scores, all_codes, partition_table_function, compare_function, start_code=None, choose_from_candidates=False):
    # Nastavi mez pro velikost valuace podle zvolene strategie
    if compare_function == higher_is_better:
        best_partition_table_value = -1
    else:
        best_partition_table_value = len(possible_codes)
    best_partition_table:list[int] = []
    best_next_guess = -1
    best_partition = []
    # Pokud je mnozina kandidatu jednoprvkova, vraci jediny kod
    if len(possible_codes) == 1:
        return possible_codes[0], best_partition_table, best_partition
    # Overeni krajniho pripadu
    elif len(possible_codes) == 0:
        return [], [], []
    # Vyber prvniho tahu, v pripade, ze je urceny prvni tah, algoritmus jej vybere
    elif len(possible_codes) == len_colours**len_pegs and start_code != None:
        temp_partition_table, temp_partition = create_next_partition(start_code, possible_codes, len_pegs, len_colours, all_scores)
        temp_partition_table_value = partition_table_function(temp_partition_table)
        # Zapsani do hodnot na vystupu
        best_partition_table = temp_partition_table
        best_next_guess = start_code
        best_partition = temp_partition
    # V pripade vyberu pouze z kandidatu
    elif choose_from_candidates == True:
        for code in possible_codes:
            temp_partition_table, temp_partition = create_next_partition(code, possible_codes, len_pegs, len_colours, all_scores)
            temp_partition_table_value = partition_table_function(temp_partition_table)
            # v kazde iteraci porovnavame valuaci s aktualni nejlepsi hodnotou, protoze vybirame kod s nejvyssi nebo nejnizsi valuaci
            if compare_function(temp_partition_table_value, best_partition_table_value):
                best_partition_table_value = temp_partition_table_value
                best_partition_table = temp_partition_table
                best_next_guess = code
                best_partition = temp_partition
    # V obecnem pripade vybirame dalsi kod z celeho prostoru kodu
    else:
        for code in all_codes:
            temp_partition_table, temp_partition = create_next_partition(code, possible_codes, len_pegs, len_colours, all_scores)
            temp_partition_table_value = partition_table_function(temp_partition_table)
            if compare_function(temp_partition_table_value, best_partition_table_value):
                best_partition_table_value = temp_partition_table_value
                best_partition_table = temp_partition_table
                best_next_guess = code
                best_partition = temp_partition
            # V pripade, ze vice kodu nabyva nejlepsi strategie chceme prednostne vybrat kod z mnoziny kandidatu
            if temp_partition_table_value == best_partition_table_value and (best_next_guess not in possible_codes) and (code in possible_codes):
                best_partition_table_value = temp_partition_table_value
                best_partition_table = temp_partition_table
                best_next_guess = code
                best_partition = temp_partition
    
    return best_next_guess, best_partition_table, best_partition


# Vraci vysledky algoritmu, pro kazdy stav hleda nejlepsi dalsi pokus a tim prochazi strom daneho algoritmu
def get_results_of_algorithm(len_pegs, len_colours, start_code, partition_table_function, compare_function, choose_from_candidates):
    len_codes = len_colours**len_pegs
    all_scores = generate_all_scores(len_pegs)
    all_codes = generate_all_codes(len_pegs, len_colours)
    partition_queue = deque()
    max_len_guesses = 0
    # uchovava pocty tajnych kodu s odpovidajicimi pocty pokusu na prolomeni
    all_len_guesses = [0]*15
    # prvni pokus
    first_partition_table, first_partition = create_next_partition(start_code, all_codes, len_pegs, len_colours, all_scores)
    for i in range(len(first_partition_table)):
        if first_partition_table[i] == 0:
            continue
        # v pripade, kdy je prvni pokus tajnym kodem
        if all_scores[i] == [len_pegs,0] and first_partition_table[i] == 1:
            max_len_guesses = 1
            all_len_guesses[1] += 1
        else:
            # Pridani dalsiho stavu (mnoziny kandidatu do fronty)
            partition_queue.append([first_partition[i],1])

    # dokud fronta neni prazdna - porad chybeji nejake koncove stavy ve stromu algoritmu
    while partition_queue:
        temp_candidates, temp_len_guesses = partition_queue.popleft()
        # Pokud zbyva pouze jeden kandidat, algoritmus jej vzdy zvoli
        if len(temp_candidates) == 1:
            max_len_guesses = max(max_len_guesses, temp_len_guesses + 1)
            all_len_guesses[temp_len_guesses + 1] += 1
        # Jinak algoritmus pro dany stav nalezne nejlepsi dalsi pokus a prida potomky mnoziny kandidatu do fronty
        else:
            temp_guess, temp_partition_table, temp_partition = find_best_guess(temp_candidates, len_pegs, len_colours, all_scores, all_codes, partition_table_function, compare_function, choose_from_candidates=choose_from_candidates)
            for i in range(len(temp_partition_table)):
                if temp_partition_table[i] == 0:
                    continue
                if all_scores[i] == [len_pegs,0] and temp_partition_table[i] == 1:
                    max_len_guesses = max(max_len_guesses, temp_len_guesses + 1)
                    all_len_guesses[temp_len_guesses+1] += 1
                else:
                    partition_queue.append([temp_partition[i], temp_len_guesses + 1])

    # Zobrazi vysledky
    if partition_table_function == find_max:
        print('Použitý algoritmus: Min-Max')
    elif partition_table_function == find_entropy:
        print('Použitý algoritmus: Max entropy')
    elif partition_table_function == find_number_of_parts:
        print('Použitý algoritmus: Max parts')
    print("První pokus byl:", start_code)
    print("Maximální počet pokusů je: ", max_len_guesses)
    print("Průměrný počet pokusů je: ", sum([i*all_len_guesses[i] for i in range(len(all_len_guesses))]) / len_codes)
    print("Počty tajných kódů s odpovídajícím počtem potřebných pokusů k prolomení: ", all_len_guesses)
    

# Spusti algoritmus zadany valuaci a strategii s nejakym tajnym kodem, v bakalarske praci odpovida funkci Solve v Algoritmu 1
def solve_one_game(len_pegs, len_colours, secret_code, partition_table_function, compare_function, start_code, choose_from_candidates):
    all_codes = generate_all_codes(len_pegs, len_colours)
    all_scores = generate_all_scores(len_pegs)
    possible_codes = all_codes
    len_guesses = 0
    score = [0,0]
    # Dokud neni tajny kod uhodnut
    while score != [len_pegs,0]:
        len_guesses +=1
        next_guess, next_partition_table, best_partition = find_best_guess(possible_codes, len_pegs, len_colours, all_scores, all_codes, partition_table_function, compare_function, start_code, choose_from_candidates)
        b,w = evaluate_codes(secret_code, next_guess, len_pegs, len_colours)
        print(next_guess, b, w)
        score = [b,w]
        # pokud hra neni dohrana, je aktualizovana mnozina kandidatu po tomto kole hry
        if score != [len_pegs,0]:
            score_index = all_scores.index([b,w])
            possible_codes = best_partition[score_index]
    return len_guesses


# Vraci hodnotu valuace v prvnim tahu, pro nejaky kod - start_code, slouzi k urceni prvniho tahu algoritmu
def get_valuation_of_first_guess(len_pegs, len_colours, start_code, partition_table_function):    
    all_scores = generate_all_scores(len_pegs)
    all_codes = generate_all_codes(len_pegs, len_colours)
    first_partition_table, first_partition = create_next_partition(start_code, all_codes, len_pegs, len_colours, all_scores)
    result = partition_table_function(first_partition_table)

    if partition_table_function == find_max:
        print('Valuace maximum pro kód ', start_code," je: ", result)
    elif partition_table_function == find_entropy:
        print('Valuace entropie potomků pro kód ', start_code," je: ", result)
    elif partition_table_function == find_number_of_parts:
        print('Valuace počet potomků pro kód ', start_code," je: ", result)
    return None


if __name__ == '__main__':
    # počet pozic
    len_pegs = 4
    # počet barev
    len_colours = 6
    
    # Testuje algoritmy s pevně daným prvním pokusem

    get_results_of_algorithm(len_pegs, len_colours, [1,1,2,2], find_max, lower_is_better, False)
    #get_results_of_algorithm(len_pegs, len_colours, [1,2,3,4], find_entropy, higher_is_better, False)
    #get_results_of_algorithm(len_pegs, len_colours, [1,1,2,3], find_number_of_parts, higher_is_better, False)
    # get_results_of_algorithm(len_pegs, len_colours, [6,6,5,5], find_max, lower_is_better, False)
    # get_results_of_algorithm(len_pegs, len_colours, [1,2,3,4], find_entropy, higher_is_better, True)
    # get_results_of_algorithm(len_pegs, len_colours, [6,6,5,4], find_number_of_parts, higher_is_better, False)


    # Spustí algoritmus pro daný tajný kód

    #solve_one_game(len_pegs, len_colours, [5,4,6,3], find_max, lower_is_better, [1,1,2,2], False)
    #solve_one_game(len_pegs, len_colours, [5,1,6,2], find_entropy, higher_is_better, [1,1,2,2], False)
    #solve_one_game(len_pegs, len_colours, [5,2,6,3], find_number_of_parts, higher_is_better, [1,1,2,2], False)


    # Vrátí valuaci prvního pokusu

    #get_valuation_of_first_guess(len_pegs, len_colours, [1,1,2,2], find_max)
    #get_valuation_of_first_guess(len_pegs, len_colours, [1,2,3,4], find_entropy)
    #get_valuation_of_first_guess(len_pegs, len_colours, [1,1,2,3], find_number_of_parts)

    
