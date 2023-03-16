import random

# define letter groupings
vowels = ['a', 'e', 'i', 'o', 'u', 'y']

diphthongs = ['ae', 'ai', 'au', 'ay', 'ea', 'ee', 'ei', 'eo', 'eu', 'ey', 'ia', 'ie', 'io', 'oa', 'oe', 'oi', 'oo', 'ou', 'oy']

consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z']

beginning_clusters = ['bl', 'br', 'ch', 'cl', 'cr', 'dr', 'fl', 'fr', 'gl', 'gr', 'gw', 'kl', 'ph', 'pl', 'pr', 'qu', 'rh', 'sc', 'sh', 'sk', 'sl', 'sm', 'sn', 'sp', 'st', 'sw', 'th', 'tr', 'tw', 'wh', 'wr', 'zh', 'scr', 'shr', 'sph', 'spl', 'spr', 'squ', 'str', 'thr']

ending_clusters = ['ch', 'ck', 'ft', 'ld', 'lt', 'nd', 'ng', 'nk', 'nt', 'ph', 'pt', 'rd', 'rk', 'sh', 'sk', 'sp', 'st', 'th', 'dd', 'ff', 'gg', 'll', 'mm', 'pp', 'rr', 'ss', 'tt', 'zz', 'rth', 'tch']

# function to define how syllables are generated
def rangen_syllable(beg_cons_prob=0, beg_cluster_prob=0, vowel_prob=0, end_cons_prob=0, end_cluster_prob=0):
    syllable = ''
    # generate the first part of the syllable
    if random.random() < beg_cons_prob: # if set to 1, a consonant will always generate instead of a cluster or nothing
        consonant = random.choice(consonants)
        syllable += consonant
    else:
        if random.random() < beg_cluster_prob:  # if set to 1, a cluster will always generate instead of nothing
            beginning_cluster = random.choice(beginning_clusters)
            syllable += beginning_cluster
    # generate the middle part of the syllable
    if random.random() < vowel_prob:    # if set to 1, a vowel will always generate instead of a diphthong
        vowel = random.choice(vowels)
        syllable += vowel
    else:
        diphthong = random.choice(diphthongs)
        syllable += diphthong
    # generate the last part of the syllable
    if random.random() < end_cons_prob: # if set to 1, a consonant will always generate instead of a cluster or nothing
        consonant = random.choice(consonants)
        syllable += consonant
    else:
        if random.random() < end_cluster_prob:  # if set to 1, a cluster will always generate instead of nothing
            ending_cluster = random.choice(ending_clusters)
            syllable += ending_cluster
    return syllable

# function to generate a name based on the syllable generation function
def rangen_word(name_splitter=False, splitter_char='', beg_cons_prob=0, beg_cluster_prob=0, vowel_prob=0, end_cons_prob=0, end_cluster_prob=0):
    name = ''
    while True:
        num_syllables = random.choices([1, 2, 3, 4], weights=[1, 4, 4, 2])[0]   # this makes names with more than one syllable favored, favoring two and three.
        syllables = [rangen_syllable(beg_cons_prob, beg_cluster_prob, vowel_prob, end_cons_prob, end_cluster_prob) for _ in range(num_syllables)]
        name = ''.join(syllables)
        # check if a single letter repeats itself too many times and regenrate the name if so
        for i, letter in enumerate(name):
            if i > 1 and letter == name[i-1] and letter == name[i-2]:
                name = ''
                break
        # check if the name contains at least one consonant or cluster so a name that is only vowels isn't generated
        if any(c in consonants or c in beginning_clusters or c in ending_clusters for c in name):
            break
    # insert an apostrophe between syllables if there are more than a certain number of total letters generated
    if len(name) > 10 and name_splitter:
        i = random.randint(1, len(syllables) - 1)
        syllables.insert(i, splitter_char)
        name = ''.join(syllables)
    return name