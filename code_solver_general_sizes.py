import numpy as np

# Possible improvements
# - switch from code as an integer to code as a list - it might be better visually, there might be some disadvantages also




def evaluate_guessG(secret_number:int, guess_number:int, len_pegs, len_colours):
    secret_code = transfer_int_to_codeG(secret_number, len_colours, len_pegs)
    guess = transfer_int_to_codeG(guess_number, len_colours, len_pegs)


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
               

def get_guess():
    strin = input("Type guess: ")
    guess = [int(strin[i]) for i in range(4)]
    return guess

def create_list_of_scores(len_pegs:int):
    all_scores:list[list[int]] = []
    for nb in range(len_pegs+1):
        for nw in range(len_pegs+1-nb):
            if nb == len_pegs - 1 and nw == 1:
                continue
            else:
                all_scores.append([nb,nw])
    return all_scores
                


def check_code_scoreG(next_guess, next_score, secret_code, len_pegs, len_colours):
    real_score = evaluate_guessG(secret_code, next_guess, len_pegs, len_colours)
    if real_score == next_score:
        return True
    else:
        return False


def transfer_int_to_codeG(number, len_colours, len_pegs):
    code = [0]*len_pegs
    for i in range(len_pegs):
        next_digit = int(number % len_colours)
        code[len_pegs-1-i] = next_digit
        number -= next_digit
        number = int(number/len_colours)
    return [code[i] + 1 for i in range(len(code))]


# searching from the list of all feasible codes, not all the codes
def create_partition_tableG(next_guess:int, possible_codes, len_pegs, len_colours, all_scores):
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

def find_best_guessG(possible_codes, len_pegs, len_colours, all_scores):
    min_of_max_partition = len(possible_codes)
    best_partition:list[int] = []
    best_next_guess = -1
    best_partition_with_codes = []
    if len(possible_codes) == 1:
        return possible_codes[0], best_partition, best_partition_with_codes
    if len(possible_codes) == len_colours**len_pegs:
        for number in range(32):
            temp_partition_table, partition_of_codes = create_partition_tableG(number, possible_codes, len_pegs, len_colours, all_scores)
            temp_max_partition = max(temp_partition_table)
            if temp_max_partition < min_of_max_partition:
                min_of_max_partition = temp_max_partition
                best_partition = temp_partition_table
                best_next_guess = number
                best_partition_with_codes = partition_of_codes
    else:
        for number in possible_codes:
            temp_partition_table, partition_of_codes = create_partition_tableG(number, possible_codes, len_pegs, len_colours, all_scores)
            temp_max_partition = max(temp_partition_table)
            if temp_max_partition < min_of_max_partition:
                min_of_max_partition = temp_max_partition
                best_partition = temp_partition_table
                best_next_guess = number
                best_partition_with_codes = partition_of_codes
    
    return best_next_guess, best_partition, best_partition_with_codes

def find_score_from_bw(b,w, all_scores):
    for i in range(len(all_scores)):
        if b == all_scores[i][0]:
            if w == all_scores[i][1]:
                return i


def play_minmaxG(len_pegs, len_colours):
    all_scores = create_list_of_scores(len_pegs)
    secret_code = np.random.randint(0,len_colours**len_pegs)
    code_guessed = False
    possible_codes = [i for i in range(len_colours**len_pegs)]
    len_guesses = 0
    while not code_guessed:
        next_guess, next_partition, best_partition_with_codes = find_best_guessG(possible_codes, len_pegs, len_colours, all_scores)
        b,w = evaluate_guessG(secret_code, next_guess, len_pegs, len_colours)
        len_guesses +=1
        if b == len_pegs:
            print(''.join([str(i) for i in transfer_int_to_codeG(next_guess, len_colours, len_pegs)]), ''.join([str(i) for i in transfer_int_to_codeG(secret_code, len_colours, len_pegs)]), len_guesses)
            code_guessed = True
        else:
            next_score = find_score_from_bw(b,w, all_scores)
            possible_codes = best_partition_with_codes[next_score]
            print(''.join([str(i) for i in transfer_int_to_codeG(next_guess, len_colours, len_pegs)]), b,w)
            

def play_minmaxG_set_code(len_pegs, len_colours, secret_code):
    all_scores = create_list_of_scores(len_pegs)
    code_guessed = False
    possible_codes = [i for i in range(len_colours**len_pegs)]
    len_guesses = 0
    while not code_guessed:
        next_guess, next_partition, best_partition_with_codes = find_best_guessG(possible_codes, len_pegs, len_colours, all_scores)
        b,w = evaluate_guessG(secret_code, next_guess, len_pegs, len_colours)
        len_guesses +=1
        if b == len_pegs:
            #print(''.join([str(i) for i in transfer_int_to_codeG(next_guess, len_colours, len_pegs)]), ''.join([str(i) for i in transfer_int_to_codeG(secret_code, len_colours, len_pegs)]), len_guesses)
            code_guessed = True
        else:
            next_score = find_score_from_bw(b,w, all_scores)
            possible_codes = best_partition_with_codes[next_score]
            #print(''.join([str(i) for i in transfer_int_to_codeG(next_guess, len_colours, len_pegs)]), b,w)
    return len_guesses



def test_all_secret_codes_minmax(len_pegs,len_colours):
    all_len_guesses = []
    max_len_guesses = 0
    len_max_len_guesses = 0
    for i in range(len_colours**len_pegs):
        temp_len_guesses = play_minmaxG_set_code(len_pegs,len_colours,i)
        all_len_guesses.append(temp_len_guesses)
        if max_len_guesses < temp_len_guesses:
            max_len_guesses = temp_len_guesses
            len_max_len_guesses = 0
        if max_len_guesses == temp_len_guesses:
            len_max_len_guesses += 1
    average_len_guesses = np.average(all_len_guesses)
    print('average number of guesses is:', average_len_guesses)
    print('maximal number of guesses is:', max_len_guesses, 'with the count of:', len_max_len_guesses)




def find_partition_table(history, possible_scores):
    # searching through all codes, we dont have to play feasible codes only
    return 0


if __name__ == '__main__':
    # find_best_guess([i for i in range(6**4)])
    len_pegs = 6
    len_colours = 2
    #print(all_scores)
    #print(len(all_scores))
    #play_minmaxG(len_pegs, len_colours)
    test_all_secret_codes_minmax(len_pegs, len_colours)
    #print(''.join([str(i) for i in [1,1,2,1]]))


