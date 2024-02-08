"""
TODO: 
1. Get the phonetic parts only
   Get the word parts only
   For the given word, find the corr. phoentic
   For the given phonetic, find the corr. word
"""

pronunciation_dict = {}

# Open the file
with open('beep-1.0', 'r') as file:
    # Read each line in the file
    for line in file:
        # Split the line into columns using space as delimiter
        columns = line.split()
        
        # Get the word content
        word = columns[0]   # key
        
        # Get the phonemes only
        phoneme = ' '.join(columns[1:])   # value   
        #print(word, phoneme)
        #print(phoneme)
        pronunciation_dict[word] = phoneme
#print(pronunciation_dict)

######
def test():
    given_key = "A"
    if given_key in pronunciation_dict:
        for key, value in pronunciation_dict.items():
            #print(pronunciation_dict[given_key])
            return(pronunciation_dict[given_key])

#######
# from the given phoneme, return corr. word
def find_word(given_phoneme):
    if given_phoneme in pronunciation_dict.values():
        for key, value in pronunciation_dict.items():
            if value == given_phoneme:
                #print(key) 
                return key

############################################
"""
TODO:
2. Filter the beep list, choose the meaningful and unique words only
"""
############################################
"""
TODO:
3. Find similar words (e.g using regex)
"""
import re

phonemes_list = pronunciation_dict.values()   # list of phonemes from dictionary
# Subsitutions - filter to match length of words as well
def substitution(given_val):
    phoneme_pattern = given_val.split()  # split selected phoneme
    print('Original:', given_val, find_word(given_val))
    for i in range(len(phoneme_pattern)):
        regex_pattern = ' '. join('.' if j == i else col for j, col in enumerate(phoneme_pattern)) # '.' for 1, or '.*' for multiple
        #print(regex_pattern)
        r = re.compile(regex_pattern)
        matches = [match for match in phonemes_list if r.match(match) and len(match.split()) == len(phoneme_pattern)] # find matches and return the list
        #print(matches)
        for match in matches:
            print(regex_pattern, '->',match, find_word(match))
#substitution("k ae t")

# Deletion - filter to match length of words as well
test_val = "m ae t"

def deletion(given_val):
    phoneme_pattern = given_val.split()  # split selected phoneme
    print('Original:', given_val, find_word(given_val))
    for i in range(len(phoneme_pattern)):
        regex_pattern = ' '. join('' if j == i else col for j, col in enumerate(phoneme_pattern)) 
        r = re.compile(regex_pattern)
        matches = [match for match in phonemes_list if r.match(match) and len(match.split()) == len(phoneme_pattern)] # find matches and return the list
        for match in matches:
                print(regex_pattern, '->', match, find_word(match))
deletion("m ae t")

# QUESTION: what is the difference between of deletion and substitution? example where these 2 will be different?