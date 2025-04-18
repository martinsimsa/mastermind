


# function used for the small case 2,3 mastermind. 
def return_all_partition_tables(len_pegs, len_colours, all_codes, candidates, partition_table_function):
    all_scores = generate_all_scores(len_pegs)
    partition_tables_values = [0]*len(all_codes)
    for i in range(len(all_codes)):
        temp_partition_table, temp_partition = create_partition_tableG(all_codes[i], candidates, len_pegs, len_colours, all_scores)
        partition_tables_values[i] = partition_table_function(temp_partition_table)
    print(partition_tables_values)



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

