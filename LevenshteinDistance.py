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

# For the given word, find the corr. phoneme
def find_phoneme(given_word, pronunciation_dict):
    for phonemes, words in pronunciation_dict.items():
        if given_word.upper() in words:
            return phonemes
    return None 
        
# from the given phoneme, return corr. words
def find_word(given_phoneme, pronunciation_dict):
    for phonemes, words in pronunciation_dict.items():
        if given_phoneme in phonemes:
            return pronunciation_dict[given_phoneme]
    return None

def calc_dict_distance(chosen_word, pronunciation_dict, lvt_dist, dict_phoneme_dists, phoneme_idx, dict_phonemes):
    chosen_phoneme = find_phoneme(chosen_word, pronunciation_dict)
    alternative_phonemes = []
    
    if chosen_phoneme != None:
        for phoneme in dict_phonemes:
            # filter to compare phonemes with the distance = 1
            if (len(phoneme.split()) >= (len(chosen_phoneme.split())-lvt_dist)) and (len(phoneme.split()) <= (len(chosen_phoneme.split())+lvt_dist)):
                phoneme_distance = levenshtein_distance_DP(chosen_phoneme, phoneme)
                if phoneme_distance >= 0 and phoneme_distance <= lvt_dist: # distance is not more than 2
                    if (phoneme not in alternative_phonemes) and (find_word(phoneme, pronunciation_dict) != chosen_word.upper().split()):  # avoid duplicates of phonemes or original word
                        alternative_phonemes.append(phoneme)
                        dict_phoneme_dists.append(str(int(phoneme_distance)) + " - " + phoneme + " ~ " + ', '.join(find_word(phoneme, pronunciation_dict)))
                        phoneme_idx = phoneme_idx + 1
        
        return dict_phoneme_dists

def select_top_alternatives(num_words, dict_phoneme_dists):
    closest_words = []
    word_details = []
    dict_phoneme_dists.sort()
    #print(dict_phoneme_dist)
    if (num_words <= len(dict_phoneme_dists)):
        for i in range(num_words):
            word_details = dict_phoneme_dists[i].split("-")
            closest_words.append(word_details[1])
        return (f"Top {num_words} alternatives: {closest_words}")
    else:
        for i in range(len(dict_phoneme_dists)):
            word_details = dict_phoneme_dists[i].split("-")
            closest_words.append(word_details[1])
        return (f"There are {len(dict_phoneme_dists)} alternative(s) in total: {closest_words}")

def main():
    # Get the beep-1.0 file
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_to_access = '\\beep-1.0'
    pronunciation_dict = {}

    # Open beep-1.0 file
    file = open(current_directory + file_to_access, 'r')
    lines = file.readlines()
    file.close()
    
    phonemes_list = []
    dict_phoneme_dists = []
    lvt_dist = 1 # levenshtein distance
    phoneme_idx = 0
    
    for line in lines:
        columns = line.split()  # Split the line into columns using space as delimiter
        dict_word = columns[0]   # word - value
        dict_phoneme = ' '.join(columns[1:])   # phoneme - key  
        phonemes_list.append(dict_phoneme) 
    
        if dict_phoneme in pronunciation_dict:
            pronunciation_dict[dict_phoneme].append(dict_word)  # Append the word to the existing list
        else:
            pronunciation_dict[dict_phoneme] = [dict_word]
            
    calc_dict_distance("easter", pronunciation_dict, lvt_dist, dict_phoneme_dists, phoneme_idx, phonemes_list)
    print(select_top_alternatives(3, dict_phoneme_dists))
        
if __name__ == "__main__":
    main()