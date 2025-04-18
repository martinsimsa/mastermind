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
                

# checks if a possible code (next_guess) belongs in the partition table to this score
def check_code_scoreG(next_guess, next_score, secret_code, len_pegs, len_colours):
    real_score = evaluate_codes(secret_code, next_guess, len_pegs)
    if real_score == next_score:
        return True
    else:
        return False


# searching from the list of all feasible codes, not all the codes
def create_partition_tableG(next_guess, possible_codes, len_pegs, len_colours, all_scores):
    partition_table = [0]*len(all_scores)
    partition_of_codes = []
    #next_guess = transfer_int_to_code(next_guess)

    # add function to return all possible scores for current game
    for score in range(len(all_scores)):
        partition_of_codes.append([])
        # Count the number of codes from current list of possible codes that would work with this score
        for code in possible_codes:
            #secret_code = transfer_int_to_code(code)
            if check_code_scoreG(next_guess, all_scores[score], code, len_pegs, len_colours):
                partition_table[score] += 1
                partition_of_codes[score].extend([code])
    return partition_table, partition_of_codes


# finds best next guess from all codes with respect to partition table of possible codes
def find_best_guess_with_function(possible_codes, len_pegs, len_colours, all_scores, all_codes, partition_table_function, compare_function, start_code=None, choose_from_candidates=False):
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
        temp_partition_table, partition_of_codes = create_partition_tableG(start_code, possible_codes, len_pegs, len_colours, all_scores)
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
                temp_partition_table, partition_of_codes = create_partition_tableG(code, possible_codes, len_pegs, len_colours, all_scores)
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
                temp_partition_table, partition_of_codes = create_partition_tableG(code, possible_codes, len_pegs, len_colours, all_scores)
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
def count_parts(partition_table):
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


def first_round(len_pegs, len_colours):
    len_codes = len_colours**len_pegs

    start_codes = [0]*5

    """start_codes[0] = [1,1,1,1]
    start_codes[1] = [1,1,1,2]
    start_codes[2] = [1,1,2,2]
    start_codes[3] = [1,1,2,3]
    start_codes[4] = [1,2,3,4]"""
    start_codes[0] = [1,1]
    start_codes[1] = [1,2]
    start_codes[2] = [2,1]
    start_codes[3] = [2,2]
    start_codes[4] = [2,2]
    
    all_scores = generate_all_scores(len_pegs)
    all_codes = generate_all_codes(len_pegs, len_colours)
    max_candidates = [0]*5
    partition_entropy = [0]*5
    expected_num_of_candidates = [0]*5
    num_of_parts = [0]*5
    for i in range(5):
        result = create_partition_tableG(start_codes[i], all_codes, len_pegs, len_colours, all_scores)
        partition_table = result[0]
        max_candidates[i] = max(partition_table)
        print(partition_table)
        #partition_entropy[i] = find_entropy(partition_table, len_codes)
        #expected_num_of_candidates[i] = find_expected_size(partition_table, len_codes)
        #num_of_parts[i] = count_parts(partition_table)
    
    print(max_candidates)
    #print(partition_entropy)
    #print(expected_num_of_candidates)
    #print(num_of_parts)


# evaluate partition tables for second round - I would have to find best code for each possibility of ohodnoceni after the first round
def second_round(len_pegs, len_colours, start_code):
    len_codes = len_colours**len_pegs
    
    all_scores = generate_all_scores(len_pegs)
    all_codes = generate_all_codes(len_pegs, len_colours)
    #max_candidates = [0]*2
    #partition_entropy = [0]*2
    #expected_num_of_candidates = [0]*2
    #num_of_parts = [0]*2


    first_partition_table, first_partition = create_partition_tableG(start_code, all_codes, len_pegs, len_colours, all_scores)
    second_guesses = [0]*len(all_scores)
    second_partition_tables = []
    second_partitions = []

    for score in range(len(all_scores)):
        #prints all partition tables
        return_all_partition_tables(len_pegs, len_colours, all_codes, first_partition[score], find_max)
        second_guesses[score], temp_partition_table, temp_partition = find_best_guess_minmax(first_partition[score], len_pegs, len_colours, all_scores, all_codes)
        second_partition_tables.append(temp_partition_table)
        second_partitions.append(temp_partition)
    
    print(first_partition_table)
    print(second_guesses)
    print(second_partition_tables)
    #print('the sum of maximal values in second partition tables is:', sum([max(second_partition_tables[i]) for i in range(len(second_partition_tables))]))
    #print('the expected maximal value in the second partition table is:', sum([max(second_partition_tables[i])*first_partition[i]/len_codes for i in range(len(second_partition_tables))]))


def three_rounds(len_pegs, len_colours, start_code):
    len_codes = len_colours**len_pegs
    
    all_scores = generate_all_scores(len_pegs)
    all_codes = generate_all_codes(len_pegs, len_colours)
    #max_candidates = [0]*2
    #partition_entropy = [0]*2
    #expected_num_of_candidates = [0]*2
    #num_of_parts = [0]*2


    first_partition_table, first_partition = create_partition_tableG(start_code, all_codes, len_pegs, len_colours, all_scores)
    second_guesses = [0]*len(all_scores)
    second_partition_tables = []
    second_partitions = []

    third_guesses = [[0 for i in range(len(all_scores))] for j in range(len(all_scores))]
    third_partition_tables = []
    third_partitions = []

    for score in range(len(all_scores)):
        second_guesses[score], temp_partition_table, temp_partition = find_best_guess_minmax(first_partition[score], len_pegs, len_colours, all_scores, all_codes)
        second_partition_tables.append(temp_partition_table)
        second_partitions.append(temp_partition)

        # partition tables for third round
        third_partition_tables.append([])
        third_partitions.append([])

        # if there are no candidates in the partition - partition table for this score is just []
        if len(second_partitions[score]) == 0:
            third_guesses[score] = []
            third_partition_tables[score].append([])
            third_partitions[score].append([])
        else:
            for score2 in range(len(all_scores)):
                if len(second_partitions[score]) == 0:
                    third_guesses[score][score2] = []
                    third_partition_tables[score].append([])
                    third_partitions[score].append([])
                    continue
                third_guesses[score][score2], temp_partition_table, temp_partition = find_best_guess_minmax(second_partitions[score][score2], len_pegs, len_colours, all_scores, all_codes)
                third_partition_tables[score].append(temp_partition_table)
                third_partitions[score].append(temp_partition)
    
    

    print(first_partition_table)
    print(second_guesses)
    print(second_partition_tables)


    print(third_guesses)
    print(third_partition_tables)


# function used for the small case 2,3 mastermind. 
def return_all_partition_tables(len_pegs, len_colours, all_codes, candidates, partition_table_function):
    all_scores = generate_all_scores(len_pegs)
    partition_tables_values = [0]*len(all_codes)
    for i in range(len(all_codes)):
        temp_partition_table, temp_partition = create_partition_tableG(all_codes[i], candidates, len_pegs, len_colours, all_scores)
        partition_tables_values[i] = partition_table_function(temp_partition_table)
    print(partition_tables_values)


# find best guess for each set of candidates and then test all 14 scores to step forward - should be faster than going through all candidates to sort them
def solve_using_partition_table_with_function_pointer(len_pegs, len_colours, start_code, partition_table_function, compare_function, choose_from_candidates):
    len_codes = len_colours**len_pegs
    
    all_scores = generate_all_scores(len_pegs)
    all_codes = generate_all_codes(len_pegs, len_colours)

    partition_queue = deque()
    partition_table_queue = deque()
    # chtěl bych do fronty zařadit množinu kandidátů, která reprezentuje stav, počet odehraných pokusů
    # do další iterace zjistím pro každé skore další možnou množinu kandidátů a počet odehraných pokusů zvýším o jeden.

    max_len_guesses = 0
    all_len_guesses = [0]*10

    first_partition_table, first_partition = create_partition_tableG(start_code, all_codes, len_pegs, len_colours, all_scores)
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
            temp_guess, temp_partition_table, temp_partition = find_best_guess_with_function(temp_candidates, len_pegs, len_colours, all_scores, all_codes, partition_table_function, compare_function, choose_from_candidates=choose_from_candidates)
        
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


    print(max_len_guesses)
    print(all_len_guesses)
    print(sum([i*all_len_guesses[i] for i in range(len(all_len_guesses))]) / len_codes)


if __name__ == '__main__':
    len_pegs = 4
    len_colours = 6
    #print(all_scores)
    #print(len(all_scores))
    #play_minmaxG(len_pegs, len_colours)
    #test_all_secret_codes_minmax_list(len_pegs, len_colours, [1,1,2,2])
    #test_all_secret_codes_minmax_46_set_start(len_pegs, len_colours)
    #play_entropy(len_pegs, len_colours)
    #base = 4
    #test_all_secret_codes_entropy(len_pegs, len_colours, 2)
    #print(''.join([str(i) for i in [1,1,2,1]]))
    #three_rounds(len_pegs, len_colours, [1,1,1,1])
    #solve_using_partition_table(len_pegs, len_colours, [1,1,2,3])
    #first_round(len_pegs,len_colours)
    #second_round(len_pegs,len_colours,[1,1])
    #print([1,1,1,2])
    #solve_using_partition_table_with_function_pointer(len_pegs, len_colours, [1,1,1,2], count_parts, higher_is_better)
    #print([1,1,1,1])
    #solve_using_partition_table_with_function_pointer(len_pegs, len_colours, [1,1,1,1], count_parts, higher_is_better)
    #play_minmax_46_set_code_set_start(len_pegs, len_colours, [5,2,3,2])
    #return_all_partition_tables(len_pegs, len_colours, generate_all_codes(len_pegs, len_colours), [[2,3],[3,2]], find_max)
    
    

    # solve_using_partition_table_with_function_pointer(len_pegs, len_colours, [1,1,1,1,1,1,2,2,2,2], find_max, lower_is_better, False)

    #first_round(len_pegs, len_colours)
    
    """all_codes = generate_all_codes(len_pegs, len_colours)
    all_scores = generate_all_scores(len_pegs)
    result = find_best_guess_minmax_old_version(all_codes, len_pegs, len_colours, all_scores, all_codes)
    print(result)"""
    
    """print([1,1,1,2])
    solve_using_partition_table_with_function_pointer(len_pegs, len_colours, [1,1,1,2], find_expected_size, lower_is_better)
    print([1,1,2,2])
    solve_using_partition_table_with_function_pointer(len_pegs, len_colours, [1,1,2,2], find_expected_size, lower_is_better)
    print([1,1,2,3])
    solve_using_partition_table_with_function_pointer(len_pegs, len_colours, [1,1,2,3], find_expected_size, lower_is_better)
    print([1,2,3,4])
    solve_using_partition_table_with_function_pointer(len_pegs, len_colours, [1,2,3,4], find_expected_size, lower_is_better)"""
    

