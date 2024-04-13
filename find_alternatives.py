import os
import numpy

def levenshtein_distance_DP(token1, token2):
    token1 = token1.split()
    token2 = token2.split()
    distances = numpy.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2
        
    a = 0
    b = 0
    c = 0
    
    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if (token1[t1-1] == token2[t2-1]):
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]
                
                if (a <= b and a <= c):
                    distances[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1

    return distances[len(token1)][len(token2)]

def find_phoneme(given_word, pronunciation_dict):
    '''
    For the given word, find the corr. phoneme
    If the given word is not found in the dictionary, return None
    '''
    for phonemes, words in pronunciation_dict.items():
        if given_word.upper() in words:
            return phonemes
    return None 
        
def find_word(given_phoneme, pronunciation_dict):
    '''
    For the given phoneme, find the corr. words
    If the given phoneme is not found in the dictionary, return None
    '''
    for phonemes in pronunciation_dict.items():
        if given_phoneme in phonemes:
            return pronunciation_dict[given_phoneme]
    return None

def calc_dict_distance(chosen_word, pronunciation_dict, lvt_dist, alt_phonemes_list, phoneme_idx, dict_phonemes):
    '''
    Return the list of alternative phonemes of distance 1 to the chosen word
    If the chosen word is not found in the dictionary, return None
    '''
    chosen_phoneme = find_phoneme(chosen_word, pronunciation_dict)
    
    if chosen_phoneme != None:
        for phoneme in dict_phonemes:
            # filter to compare phonemes with the distance = 1
            if (len(phoneme.split()) >= (len(chosen_phoneme.split())-lvt_dist)) and (len(phoneme.split()) <= (len(chosen_phoneme.split())+lvt_dist)):
                phoneme_distance = levenshtein_distance_DP(chosen_phoneme, phoneme)
                if phoneme_distance >= 0 and phoneme_distance <= lvt_dist: # distance is not more than 2
                    if (phoneme not in alt_phonemes_list) and (find_word(phoneme, pronunciation_dict) != chosen_word.upper().split()):  # avoid duplicates of original word
                        #dict_phoneme_dists.append(str(int(phoneme_distance)) + " - " + phoneme + " ~ " + ', '.join(find_word(phoneme, pronunciation_dict)))
                        alt_phonemes_list.append(phoneme)
                        phoneme_idx = phoneme_idx + 1
        alt_phonemes_list.sort()
        return alt_phonemes_list
    return None

def select_top_alternatives(num_words, alt_phonemes_list):
    '''
    Select N top alternative phonemes
    '''
    closest_words = []
    #word_details = []
    if (num_words <= len(alt_phonemes_list)):
        for i in range(num_words):
            # word_details = dict_phoneme_dists[i].split("-")
            closest_words.append(alt_phonemes_list[i])
        #return (f"Top {num_words} alternatives: {closest_words}")
        return closest_words
    else:
        for i in range(len(alt_phonemes_list)):
            #word_details = dict_phoneme_dists[i].split("-")
            closest_words.append(alt_phonemes_list[i])
        #return (f"There are {len(dict_phoneme_dists)} alternative(s) in total: {closest_words}")
        return closest_words

def extract_dictionary(file_to_access):
    '''
    Access dictionary
    Store phonemes (key) and corresponding words (value) in a dictionary variable
    Return phonemes-words pair dictionary, and the list of phonemes only
    '''
    pronunciation_dict = {}

    # Open beep-2.0 file
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file = open(current_directory + file_to_access, 'r')
    lines = file.readlines()
    file.close()
    
    phonemes_list = []  # list of all phonemes in dictionary
    
    # extract dictionary
    for line in lines:
        columns = line.split()
        dict_word = columns[0]   # value
        dict_phoneme = ' '.join(columns[1:])   # key  
        phonemes_list.append(dict_phoneme) 
    
        if dict_phoneme in pronunciation_dict:
            pronunciation_dict[dict_phoneme].append(dict_word)  # Append the word to the existing list
        else:
            pronunciation_dict[dict_phoneme] = [dict_word]
    return pronunciation_dict, phonemes_list
            
def main():
    alt_phonemes_list = []  # list of alternative phonemes with corr. distances
    lvt_dist = 1 # levenshtein distance
    phoneme_idx = 0
    pronunciation_dict, phonemes_list = extract_dictionary(file_to_access='\\dictionaries\\beep-2.0')
    
    x = calc_dict_distance("cat", pronunciation_dict, lvt_dist, alt_phonemes_list, phoneme_idx, phonemes_list)
    print(x)
    print(select_top_alternatives(3, alt_phonemes_list))
        
if __name__ == "__main__":
    main()