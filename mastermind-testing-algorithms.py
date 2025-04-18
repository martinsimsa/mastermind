import numpy as np
from collections import deque


# two lists - return ohodnoceni
def evaluate_codes(first_code, second_code, len_pegs, len_colours) -> list[int]:
    # counting the number of white and black pegs:
    b:int = 0
    w:int = 0

    # disabling indeces so we dont match one peg with several in the guess 
    first_code_colours = [0]*(len_colours)
    second_code_colours = [0]*(len_colours)
   
    # Check for exact matches and find counts of colours
    for i in range(len_pegs):
        first_code_colours[first_code[i]-1] += 1
        second_code_colours[second_code[i]-1] += 1
        if first_code[i] == second_code[i]:
            b = b+1

    # return n,0 if b = n
    if b == len_pegs:
        return [b,w]
    
    # find the number of white pegs
    w = -b
    for i in range(len_colours):
        w += min(first_code_colours[i],second_code_colours[i])

    return [b,w]


# generates all codes as list
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
               

# generates list of possible scores that can be awarded with the current count of pegs
def generate_all_scores(len_pegs:int):
    all_scores:list[list[int]] = []
    for nb in range(len_pegs+1):
        for nw in range(len_pegs+1-nb):
            if nb == len_pegs - 1 and nw == 1:
                continue
            else:
                all_scores.append([nb,nw])
    return all_scores


# finds maximum of current partition table (Knuth)
def find_max(partition_table):
    return max(partition_table)


# finds the entropy of current partition table (Neuwirth??)
def find_entropy(partition_table):
    code_count = sum([partition_table[i] for i in range(len(partition_table))])
    entropy = 0
    for i in range(len(partition_table)):
        if partition_table[i] != 0:
            entropy += - partition_table[i]/code_count * np.emath.log2(partition_table[i]/code_count)
    return entropy


# counts the number of parts of a partition table (Kooi, 2005)
def find_number_of_parts(partition_table):
    len_parts = 0
    for i in range(len(partition_table)):
        if partition_table[i] != 0:
            len_parts += 1
    return len_parts


# Function for when the strategy is to take code which minimizes valuation
def lower_is_better(first, second):
    if first < second:
        return True
    else:
        return False


# Function for when the strategy is to take code which maximizes valuation
def higher_is_better(first, second):
    if first > second:
        return True
    else:
        return False


# counts the expected number of codes after this guess (Irving 1978-1979)
def find_expected_size(partition_table):
    code_count =  sum([partition_table[i] for i in range(len(partition_table))])
    expectation = 0
    for i in range(len(partition_table)):
        if partition_table[i] != 0:
            expectation += partition_table[i]**2/code_count
    return expectation


# still need to test if it works
def create_next_partition(next_guess, possible_codes, len_pegs, len_colours, all_scores):
    partition_table = [0]*len(all_scores)
    partition_of_codes = [[] for i in range(len(all_scores))]
    #next_guess = transfer_int_to_code(next_guess)

    for code in possible_codes:
        temp_score = evaluate_codes(code, next_guess, len_pegs, len_colours)
        index_of_temp_score = all_scores.index(temp_score)
        partition_table[index_of_temp_score] += 1
        partition_of_codes[index_of_temp_score].append(code)
    return partition_table, partition_of_codes


# finds best next guess from all codes with respect to partition table of possible codes
def find_best_guess(possible_codes, len_pegs, len_colours, all_scores, all_codes, partition_table_function, compare_function, start_code=None, choose_from_candidates=False):
    # set initial value according to what we are looking for in the compare function
    if compare_function == higher_is_better:
        best_partition_table_value = -1
    else:
        best_partition_table_value = len(possible_codes)
    best_partition:list[int] = []
    best_next_guess = -1
    best_partition_with_codes = []
    
    # if i have just one possible code, i return it
    if len(possible_codes) == 1:
        return possible_codes[0], best_partition, best_partition_with_codes
    
    # In the first iteration, if i am choosing from all codes, i choose the start code assigned
    if len(possible_codes) == len_colours**len_pegs:
        temp_partition_table, partition_of_codes = create_next_partition(start_code, possible_codes, len_pegs, len_colours, all_scores)
        temp_partition_table_value = partition_table_function(temp_partition_table)
        
        # values I return
        best_partition = temp_partition_table
        best_next_guess = start_code
        best_partition_with_codes = partition_of_codes

    # useful in certain cases
    if len(possible_codes) == 0:
        return [], [], []
    
    # in general iteration, I am choosing from all codes for the next guess
    else:
        if choose_from_candidates == False:
            for code in all_codes:
                temp_partition_table, partition_of_codes = create_next_partition(code, possible_codes, len_pegs, len_colours, all_scores)
                temp_partition_table_value = partition_table_function(temp_partition_table)
                # compare function returns true if first argument is better than the second one, in this case, we compare temp value to current best value
                if compare_function(temp_partition_table_value, best_partition_table_value):
                    best_partition_table_value = temp_partition_table_value
                    best_partition = temp_partition_table
                    best_next_guess = code
                    best_partition_with_codes = partition_of_codes

                # case when initially partition wasnt with a candidate and we want to use one
                if temp_partition_table_value == best_partition_table_value and (best_next_guess not in possible_codes) and (code in possible_codes):
                    best_partition_table_value = temp_partition_table_value
                    best_partition = temp_partition_table
                    best_next_guess = code
                    best_partition_with_codes = partition_of_codes
                    
        if choose_from_candidates == True:
            for code in possible_codes:
                temp_partition_table, partition_of_codes = create_next_partition(code, possible_codes, len_pegs, len_colours, all_scores)
                temp_partition_table_value = partition_table_function(temp_partition_table)
                # compare function returns true if first argument is better than the second one, in this case, we compare temp value to current best value
                if compare_function(temp_partition_table_value, best_partition_table_value):
                    best_partition_table_value = temp_partition_table_value
                    best_partition = temp_partition_table
                    best_next_guess = code
                    best_partition_with_codes = partition_of_codes

                # case when initially partition wasnt with a candidate and we want to use one
                if temp_partition_table_value == best_partition_table_value and (best_next_guess not in possible_codes) and (code in possible_codes):
                    best_partition_table_value = temp_partition_table_value
                    best_partition = temp_partition_table
                    best_next_guess = code
                    best_partition_with_codes = partition_of_codes
    
    return best_next_guess, best_partition, best_partition_with_codes


# find best guess for each set of candidates and then test all 14 scores to step forward - should be faster than going through all candidates to sort them
def get_results_of_algorithm(len_pegs, len_colours, start_code, partition_table_function, compare_function, choose_from_candidates):
    len_codes = len_colours**len_pegs
    
    all_scores = generate_all_scores(len_pegs)
    all_codes = generate_all_codes(len_pegs, len_colours)

    partition_queue = deque()
    partition_table_queue = deque()
    # chtěl bych do fronty zařadit množinu kandidátů, která reprezentuje stav, počet odehraných pokusů
    # do další iterace zjistím pro každé skore další možnou množinu kandidátů a počet odehraných pokusů zvýším o jeden.

    max_len_guesses = 0
    all_len_guesses = [0]*10

    first_partition_table, first_partition = create_next_partition(start_code, all_codes, len_pegs, len_colours, all_scores)
    for i in range(len(first_partition_table)):
        if first_partition_table[i] == 0:
            continue
        # in case we hit the right code
        if all_scores[i] == [len_pegs,0] and first_partition_table[i] == 1:
            max_len_guesses = 1
            all_len_guesses[1] += 1
        else:
            partition_queue.append([first_partition[i],1])

    
    while partition_queue:
        # hled8m do sirky a tedy pop je na druhe strane nez append
        temp_candidates, temp_len_guesses = partition_queue.popleft()
        # If there is just one candidate left
        if len(temp_candidates) == 1:
            # add the number of tries (temp len tries) to our list and compare with database of len of tries
            max_len_guesses = max(max_len_guesses, temp_len_guesses + 1)
            all_len_guesses[temp_len_guesses + 1] += 1
            if temp_len_guesses + 1 == 6:
                print(temp_candidates)
        else:
            temp_guess, temp_partition_table, temp_partition = find_best_guess(temp_candidates, len_pegs, len_colours, all_scores, all_codes, partition_table_function, compare_function, choose_from_candidates=choose_from_candidates)
        
            for i in range(len(temp_partition_table)):
                if temp_partition_table[i] == 0:
                    continue
                # If we got the right code in this round
                if all_scores[i] == [len_pegs,0] and temp_partition_table[i] == 1:
                    max_len_guesses = max(max_len_guesses, temp_len_guesses + 1)
                    all_len_guesses[temp_len_guesses+1] += 1
                    if temp_len_guesses + 1 == 6:
                        print(temp_partition)

                else:
                    partition_queue.append([temp_partition[i], temp_len_guesses + 1])

    
    # Show results
    if partition_table_function == find_max:
        print('Použitý algoritmus: Min-Max')
    elif partition_table_function == find_entropy:
        print('Použitý algoritmus: Max entropy')
    elif partition_table_function == find_number_of_parts:
        print('Použitý algoritmus: Max parts')
    elif partition_table_function == find_expected_size:
        print('Použitý algoritmus: Expected size')
    print("Maximální počet pokusů je: ", max_len_guesses)
    print("Počty tajných kódů s odpovídajícím počtem potřebných pokusů k prolomení: ", all_len_guesses)
    print("Průměrný počet pokusů je: ", sum([i*all_len_guesses[i] for i in range(len(all_len_guesses))]) / len_codes)


# function that returns valuation of a first guess with a valuation function as a parameter
def get_valuation_of_first_guess(len_pegs, len_colours, start_code, partition_table_function):    
    all_scores = generate_all_scores(len_pegs)
    all_codes = generate_all_codes(len_pegs, len_colours)

    first_partition_table, first_partition = create_next_partition(start_code, all_codes, len_pegs, len_colours, all_scores)
    result = partition_table_function(first_partition_table)
    return result


if __name__ == '__main__':
    len_pegs = 4
    len_colours = 6
    

    # get_results_of_algorithm(len_pegs, len_colours, [1,2,2,2], find_max, lower_is_better, False)


    # prints valuation of certain first guess using certain valuation function
    print(get_valuation_of_first_guess(len_pegs, len_colours, [1,1,2,2], find_number_of_parts))
