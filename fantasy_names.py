import random, os

vowels = ['a', 'e', 'i', 'o', 'u', 'y']
diphthongs = ['ae', 'ai', 'au', 'ea', 'ee', 'ei', 'eo', 'eu', 'ia', 'ie', 'io', 'oa', 'oi', 'oo', 'ou']
consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z']
beginning_clusters = ['bl', 'br', 'ch', 'cl', 'cr', 'dr', 'fl', 'fr', 'gl', 'gr', 'gw', 'kl', 'ph', 'pl', 'pr', 'qu', 'rh', 'sc', 'sh', 'sk', 'sl', 'sm', 'sn', 'sp', 'st', 'sw', 'th', 'tr', 'tw', 'wh', 'wr', 'zh', 'scr', 'shr', 'sph', 'spl', 'spr', 'squ', 'str', 'thr']
ending_clusters = ['ch', 'ck', 'ft', 'ld', 'lt', 'nd', 'ng', 'nk', 'nt', 'ph', 'pt', 'rd', 'rk', 'sh', 'sk', 'sp', 'st', 'th', 'dd', 'ff', 'gg', 'll', 'mm', 'pp', 'rr', 'ss', 'tt', 'zz', 'rth', 'tch']

def generate_syllable():
    syllable = ''
    prev_char = ''
    # generate the first part of the syllable
    if random.random() < 0.15:
        # generate a beginning cluster
        beginning_cluster = random.choice(beginning_clusters)
        if len(syllable) > 0 and prev_char == syllable[-1]:
            beginning_cluster = random.choice([b for b in beginning_clusters if b[0] != prev_char])
        syllable += beginning_cluster
        prev_char = beginning_cluster[-1]
    else:
        # generate a consonant or no consonant
        if random.random() < 0.8:
            consonant = random.choice(consonants)
            if len(syllable) > 0 and prev_char == syllable[-1]:
                consonant = random.choice([c for c in consonants if c != prev_char])
            syllable += consonant
            prev_char = consonant
    # generate the middle part of the syllable
    if random.random() < 0.7:
        # genearate a vowel
        vowel = random.choice(vowels)
        if len(syllable) > 0 and prev_char == syllable[-1]:
            vowel = random.choice([v for v in vowels if v != prev_char])
        syllable += vowel
        prev_char = vowel
    else:
        # generate a diphthong
        diphthong = random.choice(diphthongs)
        if len(syllable) > 0 and prev_char == syllable[-1]:
            diphthong = random.choice([d for d in diphthongs if d[0] != prev_char])
        syllable += diphthong
        prev_char = diphthong[-1]
    # generate the last part of the syllable
    if random.random() < 0.15:
        # generate an ending cluster
        ending_cluster = random.choice(ending_clusters)
        if len(syllable) > 0 and prev_char == syllable[-1]:
            ending_cluster = random.choice([e for e in ending_clusters if e[0] != prev_char])
        syllable += ending_cluster
        prev_char = ending_cluster[-1]
    else:
        # generate a consonant or no consonant
        if random.random() < 0.5:
            consonant = random.choice(consonants)
            if len(syllable) > 0 and prev_char == syllable[-1]:
                consonant = random.choice([c for c in consonants if c != prev_char])
            syllable += consonant
            prev_char = consonant
    return syllable

def generate_name():
    name = ''
    # keep generating a name until it has at least one consonant or cluster
    while not any(c in consonants or c in beginning_clusters or c in ending_clusters for c in name):
        num_syllables = random.randint(1, 4)
        syllables = [generate_syllable() for _ in range(num_syllables)]
        name = ''.join(syllables)
        # insert a space between two syllables if there are more than a certain number of total letters generated
        if len(''.join(syllables)) > 10:
            i = random.randint(1, len(syllables) - 1)
            syllables.insert(i, ' ')
        name = ''.join(syllables)
    return name.title()

while True:
    print("Here are 10 randomly generated fantasy names:\n")
    
    for i in range(10):
        print(generate_name())
        
    user_input = input("\nPress 'Enter' to generate a new list or type 'n' to quit: ")
    if user_input.lower() == 'n':
        break
    os.system('cls' if os.name == 'nt' else 'clear')
