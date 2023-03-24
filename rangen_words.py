import random, json, os

# class object to use for easy character set indexing
class CharSet:
    pass

# function to load the character set
def load_charset(load_set=None):
    charset = CharSet()
    charset_file = 'rangen_charsets.json'
    default_set = {
        # if building your own character sets for a json file, each of these dictionaries need to be wrapped in, for example: 'CharSetName': { }
        'vowels': ['a', 'e', 'i', 'o', 'u', 'y'],
        'diphthongs': ['ae', 'ai', 'au', 'ay', 'ea', 'ee', 'ei', 'eo', 'eu', 'ey', 'ia', 'ie', 'io', 'oa', 'oe', 'oi', 'oo', 'ou', 'oy', 'ua', 'ue', 'ui'],
        'consonants': ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z'],
        'beginning_clusters': ['bl', 'br', 'ch', 'cl', 'cr', 'dr', 'fl', 'fr', 'gl', 'gr', 'gw', 'kl', 'ph', 'pl', 'pr', 'qu', 'rh', 'sc', 'sh', 'sk', 'sl', 'sm', 'sn', 'sp', 'st', 'sw', 'th', 'tr', 'tw', 'wh', 'wr', 'zh', 'scr', 'shr', 'sph', 'spl', 'spr', 'squ', 'str', 'thr'],
        'ending_clusters': ['ch', 'ck', 'ct', 'dd', 'ff', 'ft', 'gg', 'ld', 'lf', 'lk', 'll', 'lm', 'lt', 'mm', 'mp', 'nd', 'ng', 'nk', 'nt', 'ph', 'pp', 'pt', 'rd', 'rk', 'rr', 'sh', 'sk', 'sp', 'ss', 'st', 'th', 'tt', 'zz', 'rth', 'tch']
    }
    # load json file with custom character sets if it exists
    if os.path.exists(charset_file):
        try:
            with open(charset_file, 'r') as f:
                char_file = json.load(f)
                # load the character set that is passed through load_set
                if load_set in char_file:
                    char_set = char_file[load_set]
                # load the default character set if the json file exists but None is still passed in load_set
                elif load_set == None:
                    char_set = default_set  
                # error handling to load the default character set if the charset file exists but the value passed through load_set doesn't exist
                else:
                    print(f'Error: Could not find a character set named "{load_set}" in the charset file. Default character set will be loaded.')
                    char_set = default_set
        # error handling to load the default character set if the json file is corrupt
        except json.JSONDecodeError:
            print('Error: The charset file is corrupt. Default character set will be loaded.')
            char_set = default_set
    # load the default character set if there is no json file
    else:
        char_set = default_set    
    for key, value in char_set.items():
        setattr(charset, key, value)
    return charset

# function to define how syllables are generated
def rangen_syllable(load_set=None, beg_cons_prob=0, beg_cluster_prob=0, vowel_prob=0, end_cons_prob=0, end_cluster_prob=0):
    char_set = load_charset(load_set)
    syllable = ''
    # generate the first part of the syllable
    if random.random() < beg_cons_prob: # if set to 1, a consonant will always generate instead of a cluster or nothing
        consonant = random.choice(char_set.consonants)
        syllable += consonant
    else:
        if random.random() < beg_cluster_prob:  # if set to 1, a cluster will always generate instead of nothing
            beginning_cluster = random.choice(char_set.beginning_clusters)
            syllable += beginning_cluster
    # generate the middle part of the syllable
    if random.random() < vowel_prob:    # if set to 1, a vowel will always generate instead of a diphthong
        vowel = random.choice(char_set.vowels)
        syllable += vowel
    else:
        diphthong = random.choice(char_set.diphthongs)
        syllable += diphthong
    # generate the last part of the syllable
    if random.random() < end_cons_prob: # if set to 1, a consonant will always generate instead of a cluster or nothing
        consonant = random.choice(char_set.consonants)
        syllable += consonant
    else:
        if random.random() < end_cluster_prob:  # if set to 1, a cluster will always generate instead of nothing
            ending_cluster = random.choice(char_set.ending_clusters)
            syllable += ending_cluster
    return syllable

# function to generate a word based on the syllable generation function
def rangen_word(load_set=None, beg_cons_prob=0, beg_cluster_prob=0, vowel_prob=0, end_cons_prob=0, end_cluster_prob=0, max_syllables=0, word_split=False, split_char='', word_long=0):
    char_set = load_charset(load_set)
    word = ''
    while True:
        num_syllables = random.randint(1, int(max_syllables))
        syllables = [rangen_syllable(load_set, beg_cons_prob, beg_cluster_prob, vowel_prob, end_cons_prob, end_cluster_prob) for _ in range(num_syllables)]
        word = ''.join(syllables)
        # check if a single letter repeats itself too many times and regenerate the word if so
        for i, letter in enumerate(word):
            if i > 1 and letter == word[i-1] and letter == word[i-2]:
                word = ''
                break
        # check if all the consonant probabilities were set to 0 which would cause an infinite loop, so instead it just prints empty names
        if beg_cons_prob == 0 and beg_cluster_prob == 0 and end_cons_prob == 0 and end_cluster_prob == 0:
            word = ''
            break
        # check to only print words that contain at least one consonant. if there are no consonants then an empty name will print
        if any(c in char_set.consonants or c in char_set.beginning_clusters or c in char_set.ending_clusters for c in word):
            break
    # insert a character between syllables if there are more than a certain number of total letters generated
    if len(word) >= word_long and word_split and len(syllables) > 1:
        i = random.randint(1, len(syllables) - 1)
        syllables.insert(i, split_char)
        word = ''.join(syllables)
    return word

# debug testing since the script is intended to be imported into other projects. using some preset values and default character set.
if __name__ == "__main__":
    word = rangen_word(load_set=None, beg_cons_prob=0.8, beg_cluster_prob=0.2, vowel_prob=0.75, end_cons_prob=0.6, end_cluster_prob=0.15, max_syllables=4, word_split=False, split_char='', word_long=10)
    print(word)