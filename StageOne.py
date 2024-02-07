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

give_val = "k ae t"
phoneme_pattern = give_val.split()  # split phonemes
phonemes_list = pronunciation_dict.values()   # list of phonemes from dictionary

# find when one wildcard at a place
for i in range(len(phoneme_pattern)):
    regex_pattern = ' '. join('.' if j == i else col for j, col in enumerate(phoneme_pattern)) # '.' for 1, or '.*' for multiple
    #print(regex_pattern)
    r = re.compile(regex_pattern)
    matches = [match for match in phonemes_list if r.match(match) and len(match.split()) == len(phoneme_pattern)] # find matches and return the list
    #print(matches)
    for match in matches:
        print(find_word(match))