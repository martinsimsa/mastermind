import numpy as np
from collections import deque
### Possible improvements ###
# add function that compares partition tables using a pointer to a comparing function
# Use Hamming code for 7,2 Mastermind???

#class State:
 #   def __init__(self, rounds, ):
  #      self.name = name
   #     self.age = age





# two lists - return ohodnoceni
def evaluate_guess_as_list(secret_code, guess, len_pegs):
    # counting the number of white and black pegs:
    b:int = 0
    w:int = 0

    # disabling indeces so we dont match one peg with several in the guess 
    gind = [1]*len_pegs
    scind = [1]*len_pegs
   
    # Check for exact matches
    for i in range(len_pegs):
        if secret_code[i] == guess[i]:
            b = b+1
            gind[i] = 0
            scind[i] = 0
    if b == len_pegs:
        return [b,w]
   
    # check for 'white' matches - right color on wrong position
    for i in range(len_pegs):
        if gind[i]:
            for j in range(len_pegs):
                if i==j:
                    continue
                elif scind[j]:
                    if guess[i] == secret_code[j]:
                        w = w+1
                        scind[j] = 0
                        break
    return [b,w]


# generates all codes as list
def generate_codes_repeated(len_pegs, len_colours):
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
def create_list_of_scores(len_pegs:int):
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
    real_score = evaluate_guess_as_list(secret_code, next_guess, len_pegs)
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
def find_best_guess_minmax(possible_codes, len_pegs, len_colours, all_scores, all_codes, start_code=None):
    min_of_max_partition = len(possible_codes)
    best_partition:list[int] = []
    best_next_guess = -1
    best_partition_with_codes = []
    
    # if i have just one possible code, i return it
    if len(possible_codes) == 1:
        return possible_codes[0], best_partition, best_partition_with_codes
    
    # In the first iteration, if i am choosing from all codes, i choose only those that are increasing (first half)
    if len(possible_codes) == len_colours**len_pegs:
        temp_partition_table, partition_of_codes = create_partition_tableG(start_code, possible_codes, len_pegs, len_colours, all_scores)
        temp_max_partition = max(temp_partition_table)
        
        # values I return
        best_partition = temp_partition_table
        best_next_guess = start_code
        best_partition_with_codes = partition_of_codes

    # in general iteration, I am choosing from all codes for the next guess
    if len(possible_codes) == 0:
        return [], [], []
    

    else:
        best_next_guess_is_candidate = False
        for code in all_codes:
            temp_partition_table, partition_of_codes = create_partition_tableG(code, possible_codes, len_pegs, len_colours, all_scores)
            temp_max_partition = max(temp_partition_table)
            if temp_max_partition < min_of_max_partition:
                min_of_max_partition = temp_max_partition
                best_partition = temp_partition_table
                best_next_guess = code
                best_partition_with_codes = partition_of_codes
                # add revision if code is a candidate because we want to use them first
                if best_next_guess in possible_codes:
                    best_next_guess_is_candidate = True
                else:
                    best_next_guess_is_candidate = False

            # case when initially partition wasnt with a candidate and we want to use one
            if temp_max_partition == min_of_max_partition and (best_next_guess not in possible_codes) and (code in possible_codes):
                min_of_max_partition = temp_max_partition
                best_partition = temp_partition_table
                best_next_guess = code
                best_partition_with_codes = partition_of_codes
    
    return best_next_guess, best_partition, best_partition_with_codes


# finds best next guess from all codes with respect to partition table of possible codes
def find_best_guess_minmax_46_set_start(possible_codes, len_pegs, len_colours, all_scores):
    min_of_max_partition = len(possible_codes)
    best_partition:list[int] = []
    best_next_guess = -1
    best_partition_with_codes = []
    all_codes = generate_codes_repeated(len_pegs, len_colours)
    
    # if i have just one possible code, i return it
    if len(possible_codes) == 1:
        return possible_codes[0], best_partition, best_partition_with_codes
    
    # In the first iteration, if i am choosing from all codes, i choose 1122 - number 7
    if len(possible_codes) == len_colours**len_pegs:
        temp_partition_table, partition_of_codes = create_partition_tableG([1,1,2,2], possible_codes, len_pegs, len_colours, all_scores)
        best_partition = temp_partition_table
        best_next_guess = [1,1,2,2]
        best_partition_with_codes = partition_of_codes

    # in general iteration, I am choosing from all codes in possible codes for the next guess
    else:
        best_next_guess_is_candidate = False
        for code in all_codes:
            temp_partition_table, partition_of_codes = create_partition_tableG(code, possible_codes, len_pegs, len_colours, all_scores)
            temp_max_partition = max(temp_partition_table)
            if temp_max_partition < min_of_max_partition:
                min_of_max_partition = temp_max_partition
                best_partition = temp_partition_table
                best_next_guess = code
                best_partition_with_codes = partition_of_codes
                if best_next_guess in possible_codes:
                    best_next_guess_is_candidate = True
                else:
                    best_next_guess_is_candidate = False
            if temp_max_partition == min_of_max_partition and (best_next_guess not in possible_codes and code in possible_codes):
                min_of_max_partition = temp_max_partition
                best_partition = temp_partition_table
                best_next_guess = code
                best_partition_with_codes = partition_of_codes
    
    return best_next_guess, best_partition, best_partition_with_codes



# finds the entropy of current partition table
def find_entropy(partition_table, code_count, base):
    entropy = 0
    for i in range(len(partition_table)):
        if partition_table[i] != 0:
            entropy += - partition_table[i]/code_count * np.emath.logn(base, partition_table[i]/code_count)
    return entropy


# counts the number of parts of a partition table (Kooi, 2005)
def count_parts(partition_table):
    len_parts = 0
    for i in range(len(partition_table)):
        if partition_table[i] != 0:
            len_parts += 1
    return len_parts


# counts the expected number of codes after this guess (Irving 1978-1979)
def find_expected_size(partition_table, code_count):
    expectation = 0
    for i in range(len(partition_table)):
        if partition_table[i] != 0:
            expectation += partition_table[i]**2/code_count
    return expectation


# finds best next guess from all codes with respect to partition table of possible codes
def find_best_guess_entropy(possible_codes, len_pegs, len_colours, all_scores, base):
    highest_entropy = 0
    best_partition:list[int] = []
    best_next_guess = -1
    best_partition_with_codes = []
    
    # if i have just one possible code, i return it
    if len(possible_codes) == 1:
        return possible_codes[0], best_partition, best_partition_with_codes
    
    # In the first iteration, if i am choosing from all codes, i choose only those that are increasing (first half)
    if len(possible_codes) == len_colours**len_pegs:
        for number in range(int(len_colours**len_pegs / len_colours)):
            temp_partition_table, partition_of_codes = create_partition_tableG(number, possible_codes, len_pegs, len_colours, all_scores)
            temp_entropy = find_entropy(temp_partition_table, len(possible_codes), base)
            if temp_entropy > highest_entropy:
                highest_entropy = temp_entropy
                best_partition = temp_partition_table
                best_next_guess = number
                best_partition_with_codes = partition_of_codes

    # in general iteration, I am choosing from all codes in possible codes for the next guess
    else:
        for number in possible_codes:
            temp_partition_table, partition_of_codes = create_partition_tableG(number, possible_codes, len_pegs, len_colours, all_scores)
            temp_entropy = find_entropy(temp_partition_table, len(possible_codes), base)
            if temp_entropy > highest_entropy:
                highest_entropy = temp_entropy
                best_partition = temp_partition_table
                best_next_guess = number
                best_partition_with_codes = partition_of_codes
    
    return best_next_guess, best_partition, best_partition_with_codes



# finds the index of a score from the number of black and white pegs
def find_score_from_bw(b,w, all_scores):
    for i in range(len(all_scores)):
        if b == all_scores[i][0]:
            if w == all_scores[i][1]:
                return i


def play_minmaxG_set_code(len_pegs, len_colours, secret_code, all_codes, start_code):
    all_scores = create_list_of_scores(len_pegs)
    code_guessed = False
    possible_codes = all_codes
    len_guesses = 0
    while not code_guessed:
        next_guess, next_partition, best_partition_with_codes = find_best_guess_minmax(possible_codes, len_pegs, len_colours, all_scores, all_codes, start_code)
        b,w = evaluate_guess_as_list(secret_code, next_guess, len_pegs)
        len_guesses +=1
        if b == len_pegs:
            #print(''.join([str(i) for i in transfer_int_to_codeG(next_guess, len_colours, len_pegs)]), ''.join([str(i) for i in transfer_int_to_codeG(secret_code, len_colours, len_pegs)]), len_guesses)
            code_guessed = True
        else:
            next_score = find_score_from_bw(b,w, all_scores)
            possible_codes = best_partition_with_codes[next_score]
            #print(''.join([str(i) for i in transfer_int_to_codeG(next_guess, len_colours, len_pegs)]), b,w)
    return len_guesses


def play_minmax_46_set_code_set_start(len_pegs, len_colours, secret_code):
    all_scores = create_list_of_scores(len_pegs)
    code_guessed = False
    possible_codes = generate_codes_repeated(len_pegs, len_colours)
    len_guesses = 0

    while not code_guessed:
        next_guess, next_partition, best_partition_with_codes = find_best_guess_minmax_46_set_start(possible_codes, len_pegs, len_colours, all_scores)
        b,w = evaluate_guess_as_list(secret_code, next_guess, len_pegs)
        len_guesses +=1
        if b == len_pegs:
            print(''.join([str(i) for i in next_guess]), ''.join([str(i) for i in secret_code]), len_guesses)
            code_guessed = True
        else:
            next_score = find_score_from_bw(b,w, all_scores)
            possible_codes = best_partition_with_codes[next_score]
            print(''.join([str(i) for i in next_guess]), b,w)
    return len_guesses


def test_all_secret_codes_minmax_46_set_start(len_pegs,len_colours):
    all_len_guesses = []
    max_len_guesses = 0
    len_max_len_guesses = 0
    for i in range(len_colours**len_pegs):
        temp_len_guesses = play_minmax_46_set_code_set_start(len_pegs,len_colours,i)
        all_len_guesses.append(temp_len_guesses)
        if max_len_guesses < temp_len_guesses:
            max_len_guesses = temp_len_guesses
            len_max_len_guesses = 0
        if max_len_guesses == temp_len_guesses:
            len_max_len_guesses += 1
    average_len_guesses = np.average(all_len_guesses)
    print('average number of guesses is:', average_len_guesses)
    print('maximal number of guesses is:', max_len_guesses, 'with the count of:', len_max_len_guesses)


def test_all_secret_codes_minmax_list(len_pegs,len_colours, start_code):
    all_len_guesses = []
    max_len_guesses = 0
    len_max_len_guesses = 0
    all_codes = generate_codes_repeated(len_pegs, len_colours)
    for code in all_codes:
        temp_len_guesses = play_minmaxG_set_code(len_pegs,len_colours,code, all_codes, start_code)
        all_len_guesses.append(temp_len_guesses)
        if max_len_guesses < temp_len_guesses:
            max_len_guesses = temp_len_guesses
            len_max_len_guesses = 0
        if max_len_guesses == temp_len_guesses:
            len_max_len_guesses += 1
    average_len_guesses = np.average(all_len_guesses)
    print('average number of guesses is:', average_len_guesses)
    print('maximal number of guesses is:', max_len_guesses, 'with the count of:', len_max_len_guesses)



# function that plays one set with the minmax algorithm
def play_entropy(len_pegs, len_colours):
    all_scores = create_list_of_scores(len_pegs)
    secret_code = np.random.randint(0,len_colours**len_pegs)
    code_guessed = False
    possible_codes = [i for i in range(len_colours**len_pegs)]
    len_guesses = 0
    while not code_guessed:
        next_guess, next_partition, best_partition_with_codes = find_best_guess_entropy(possible_codes, len_pegs, len_colours, all_scores)
        b,w = evaluate_guessG(secret_code, next_guess, len_pegs, len_colours)
        len_guesses +=1
        if b == len_pegs:
            print(''.join([str(i) for i in transfer_int_to_codeG(next_guess, len_colours, len_pegs)]), ''.join([str(i) for i in transfer_int_to_codeG(secret_code, len_colours, len_pegs)]), len_guesses)
            code_guessed = True
        else:
            next_score = find_score_from_bw(b,w, all_scores)
            possible_codes = best_partition_with_codes[next_score]
            print(''.join([str(i) for i in transfer_int_to_codeG(next_guess, len_colours, len_pegs)]), b,w)


def play_entropy_set_code(len_pegs, len_colours, secret_code, base):
    all_scores = create_list_of_scores(len_pegs)
    code_guessed = False
    possible_codes = [i for i in range(len_colours**len_pegs)]
    len_guesses = 0
    while not code_guessed:
        next_guess, next_partition, best_partition_with_codes = find_best_guess_entropy(possible_codes, len_pegs, len_colours, all_scores, base)
        b,w = evaluate_guessG(secret_code, next_guess, len_pegs, len_colours)
        len_guesses +=1
        if b == len_pegs:
            #print(''.join([str(i) for i in transfer_int_to_codeG(next_guess, len_colours, len_pegs)]), ''.join([str(i) for i in transfer_int_to_codeG(secret_code, len_colours, len_pegs)]), len_guesses)
            code_guessed = True
            if next_guess != secret_code:
                print('secret code is different')
                print(secret_code, next_guess)
        else:
            next_score = find_score_from_bw(b,w, all_scores)
            possible_codes = best_partition_with_codes[next_score]
            #print(''.join([str(i) for i in transfer_int_to_codeG(next_guess, len_colours, len_pegs)]), b,w)
    return len_guesses

# base for the base of the logarithm
def test_all_secret_codes_entropy(len_pegs,len_colours, base):
    all_len_guesses = []
    max_len_guesses = 0
    len_max_len_guesses = 0
    for i in range(len_colours**len_pegs):
        temp_len_guesses = play_entropy_set_code(len_pegs,len_colours,i, base)
        all_len_guesses.append(temp_len_guesses)
        if max_len_guesses < temp_len_guesses:
            max_len_guesses = temp_len_guesses
            len_max_len_guesses = 0
        if max_len_guesses == temp_len_guesses:
            len_max_len_guesses += 1
        if max_len_guesses >= 6:
            print('chyba, neco bylo na 6 pokusu')
    average_len_guesses = np.average(all_len_guesses)
    print('average number of guesses is:', average_len_guesses)
    print('maximal number of guesses is:', max_len_guesses, 'with the count of:', len_max_len_guesses)


def first_round(len_pegs, len_colours):
    len_codes = len_colours**len_pegs

    start_codes = [0]*5

    start_codes[0] = [1,1,1,1]
    start_codes[1] = [1,1,1,2]
    start_codes[2] = [1,1,2,2]
    start_codes[3] = [1,1,2,3]
    start_codes[4] = [1,2,3,4]
    
    all_scores = create_list_of_scores(len_pegs)
    all_codes = generate_codes_repeated(len_pegs, len_colours)
    max_candidates = [0]*5
    partition_entropy = [0]*5
    expected_num_of_candidates = [0]*5
    num_of_parts = [0]*5
    for i in range(5):
        result = create_partition_tableG(start_codes[i], all_codes, len_pegs, len_colours, all_scores)
        partition_table = result[0]
        max_candidates[i] = max(partition_table)
        partition_entropy[i] = find_entropy(partition_table, len_codes)
        expected_num_of_candidates[i] = find_expected_size(partition_table, len_codes)
        num_of_parts[i] = count_parts(partition_table)
    
    print(max_candidates)
    print(partition_entropy)
    print(expected_num_of_candidates)
    print(num_of_parts)


# evaluate partition tables for second round - I would have to find best code for each possibility of ohodnoceni after the first round

def second_round(len_pegs, len_colours, start_code):
    len_codes = len_colours**len_pegs
    
    all_scores = create_list_of_scores(len_pegs)
    all_codes = generate_codes_repeated(len_pegs, len_colours)
    #max_candidates = [0]*2
    #partition_entropy = [0]*2
    #expected_num_of_candidates = [0]*2
    #num_of_parts = [0]*2


    first_partition_table, first_partition = create_partition_tableG(start_code, all_codes, len_pegs, len_colours, all_scores)
    second_guesses = [0]*len(all_scores)
    second_partition_tables = []
    second_partitions = []

    for score in range(len(all_scores)):
        second_guesses[score], temp_partition_table, temp_partition = find_best_guess_minmax(first_partition[score], len_pegs, len_colours, all_scores, all_codes)
        second_partition_tables.append(temp_partition_table)
        second_partitions.append(temp_partition)
    
    print(first_partition_table)
    print(second_guesses)
    print(second_partition_tables)



def three_rounds(len_pegs, len_colours, start_code):
    len_codes = len_colours**len_pegs
    
    all_scores = create_list_of_scores(len_pegs)
    all_codes = generate_codes_repeated(len_pegs, len_colours)
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

        # if there are no candidates in the partition
        if len(second_partitions) == 1:
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


# find best guess for each set of candidates and then test all 14 scores to step forward - should be faster than going through all candidates to sort them
def solve_using_partition_table(len_pegs, len_colours, start_code):
    len_codes = len_colours**len_pegs
    
    all_scores = create_list_of_scores(len_pegs)
    all_codes = generate_codes_repeated(len_pegs, len_colours)

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
        if all_scores[i] == [4,0] and first_partition_table[i] == 1:
            max_len_guesses = 1
            all_len_guesses[1] += 1
        else:
            partition_queue.append([first_partition[i],1])

    
    while partition_queue:
        # hled8m do sirky a tedy pop je na druhe strane nez append
        temp_candidates, temp_len_guesses = partition_queue.pop()
        # If there is just one candidate left
        if len(temp_candidates) == 1:
            # add the number of tries (temp len tries) to our list and compare with database of len of tries
            max_len_guesses = max(max_len_guesses, temp_len_guesses + 1)
            all_len_guesses[temp_len_guesses + 1] += 1
            if temp_len_guesses + 1 == 6:
                print(temp_candidates)
        else:
            temp_guess, temp_partition_table, temp_partition = find_best_guess_minmax(temp_candidates, len_pegs, len_colours, all_scores, all_codes)
        
            for i in range(len(temp_partition_table)):
                if temp_partition_table[i] == 0:
                    continue
                # If we got the right code in this round
                if all_scores[i] == [4,0] and temp_partition_table[i] == 1:
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
    # find_best_guess([i for i in range(6**4)])
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
    #three_rounds(len_pegs, len_colours, [1,1,2,3])
    solve_using_partition_table(len_pegs, len_colours, [1,1,2,3])
    #play_minmax_46_set_code_set_start(len_pegs, len_colours, [5,2,3,2])

    