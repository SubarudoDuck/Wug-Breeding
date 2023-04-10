characteristics = ["intelligence", "beauty", "strength", "speed"]
superwug_genome = [1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
gene_zones      = [2, 1, 2, 3, 3, 1, 3, 3, 0, 0, 2, 2, 0, 1, 0, 1]

def decode(genome):
    '''Takes the genome (list), sorts the genes according to the gene zone,
    returns a dictionary of characteristics and its corresponding combination
    of genes'''
    # set up the charateristic dictionary
    features = {}
    for char_key in characteristics:
        if char_key not in features:
            features[char_key] = ""
    # allocate the genes to the corresponding charateristics
    for index in range(0, len(genome)):
        char = characteristics[gene_zones[index]]
        features[char] += str(genome[index])
    return features

def compare(trial, basis):
    '''Takes two genomes (lists), compares the characteristics of the wug and
    the superwug, returns a list of booleans to indicate which characteristic
    is superior'''
    # compare the characteristics of the wug in question and the superwug
    super_or_not = []
    for char_key in characteristics:
        # insert False if the feature is different, True otherwise
        if trial[char_key] == basis[char_key]:
            super_or_not.append(True)
        else:
            super_or_not.append(False)
    return super_or_not

def genome2features(genome):
    '''Takes a genome (list), returns whether each characteristic of the wug is
    superior(list of booleans), with True meaning Superior and False meaning 
    Normal'''
    # decode each wug and compare them to the superwug's characteristics
    superwug = decode(superwug_genome)
    wug_try = decode(genome)
    return compare(wug_try, superwug)

def report_population(population):
    '''Takes a list of wugs (tuples), sorts and counts the wugs sharing the
    same characteristics, returns a list of unique wugs (tuples) and the number
    of each type in the population'''
    gen_dict = {}
    unique = []
    for genome in population:
        # decode every wug's genome and turn it into a tuple
        feature = genome2features(genome[0])
        feature.append(genome[1])
        gen_key = tuple(feature)
        # find unique sets of features and count the number of times they
        # appear in the population
        if gen_key not in unique:
            unique.append(gen_key)
        if gen_key not in gen_dict:
            gen_dict[gen_key] = 1
        else:
            gen_dict[gen_key] += 1
    # sort each unique set of features by count and reverse the list (put it in
    # descending order)
    pop_count = []
    for ukey in unique:
        pop_count.append((ukey, gen_dict[ukey]))
    pop_count.sort()
    return pop_count[::-1]

def rank(wug):
    '''Takes a wug (tuple), counts the number of superior features its genome 
    has, return the count (integer)'''
    # get the genome's features
    features = genome2features(wug[0])
    rank = 0
    # count the number of superior features in the genome
    for feature in features:
        if feature:
            rank += 1
    return rank

def insert_ranked(population, new_wug, limit):
    '''Takes the population (list of tuples), a new wug (tuple), and a limit
    (integer), inserts the new wug and sorts the population according to rank,
    deletes the last wug if population count exceeds limit, returns nothing,
    but modifies population (list)'''
    # add the new wug to the population and sort according to rank
    population.append(new_wug)
    population.sort(reverse=True, key=lambda wug: (rank(wug), wug))
    # if the population exceeds the limit, remove the final (extra) wug
    if len(population) > limit:
        population.pop(-1)
        
def proliferate(population, limit=64):
    '''Takes a population of wugs (list of tuples) and its limit size
    (integer), create 16 new wugs each with a single gene modified from the
    original wugs and add them to the population, returns nothing, but 
    modifies population (list)'''
    # create 16 new wugs, each with one gene changed in a distinct position,
    # put them in a temporary list
    new_genes_list = []
    for genes in population:
        for i in range(0, 16):
            new_gene = genes[0].copy()
            # change the gene from 0 to 1 or from 1 to 0
            if new_gene[i] == 0:
                new_gene[i] = 1
            else:
                new_gene[i] = 0
            new_genes_list.append((new_gene, genes[1]))
    # insert the new genes back into the population
    for new in new_genes_list:
        insert_ranked(population, new, limit)
        
def check_gender(hermaphrodite, gender):
    '''Takes the hermaphrodite value (boolean), the gender of the first wug
    (string), finds the genders suited to the given gender according to the
    hermaphrodite value, returns the list of suited genders'''
    suit = []
    # if hermaphrodite is False, the suited gender is opposite
    if not hermaphrodite:
        if gender == "M":
            suit.append("F")
        else:
            suit.append("M")
    # else, both genders count
    else:
        suit.append("M")
        suit.append("F")
    return suit

def check_suit(wug1, wug2, coincidence_bonus):
    '''Takes two wugs (tuples) and the coincidence bonus value (integer), 
    calculates the suitability score, returns the score (integer)'''
    suitability = 0
    coin = 0
    # decode the features of the two wugs
    features1 = genome2features(wug1[0])
    features2 = genome2features(wug2[0])
    # find the number of coinciding features between the two wugs
    for index in range(0, len(features1)):
        if features1[index] == features2[index]:
            coin += 1
    # calculate the suitability score using the given formula
    suitability += rank(wug1) + rank(wug2) + coin * coincidence_bonus
    return suitability

def children(population, wug1, wug2, limit):
    '''Takes the population (list of tuples), two wugs (tuples) and a limit
    (integer), makes a basic offspring genome with half of each parents' 
    genomes, create and insert 16 wugs with one gene modified and 2 wugs with
    the basic genome, returns the list sorted by rank (insert_ranked)'''
    # create the basic genome
    basic_genome = wug1[0][:8] + wug2[0][8:]
    # create the 16 offspring
    kids = []
    kids.append((basic_genome, "M"))
    proliferate(kids, limit)
    kids.remove((basic_genome, "M"))
    # the first 8 offspring are male
    for i in range(0, 8):
        kids[i] = (kids[i][0], "M")
    # the final 8 offspring are female
    for j in range(8, 16):
        kids[j] = (kids[j][0], "F")
    # insert the last two wugs, first one being male and second one female
    kids.append((basic_genome, "M"))
    kids.append((basic_genome, "F"))
    # insert all eighteen children to the population, sorted by rank
    for kid in kids:
        insert_ranked(population, kid, limit)

def breed(population, limit=64, hermaphrodite=False, coincidence_bonus=0):
    '''Takes the population (list of wugs), the limit (integer), hermaphrodite
    value (boolean) and the coincidence bonus value (integer), find suitable
    pairs of wug parents and create offspring from them, returns nothing, but
    modifies the population'''
    # the original wugs are chosen as parents
    parents = population.copy()
    while parents:
        wug1 = parents[0]
        # find the wug with the highest suitability score (most suitable) for
        # the chosen wug
        for wug_try in parents:
            if wug_try != wug1:
                maxsuit = -10000
                if wug_try[1] in check_gender(hermaphrodite, wug1[1]):
                    if check_suit(wug1, wug_try, coincidence_bonus) > maxsuit:
                        maxsuit = check_suit(wug1, wug_try, coincidence_bonus)
                        wug_parents = (wug1, wug_try)
        # create offspring based on this pair of wugs, with the male wug always
        # being the first parent
        if wug_parents[0][1] == "M":
            children(population, wug_parents[0], wug_parents[1], limit)
        else:
            children(population, wug_parents[1], wug_parents[0], limit)
        # remove the chosen parents, as they cannot breed any more
        for wug in wug_parents:
            parents.remove(wug)