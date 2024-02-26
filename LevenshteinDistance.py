import os
import numpy

def levenshteinDistanceDP(token1, token2):
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

    #printDistances(distances, len(token1), len(token2))
    return distances[len(token1)][len(token2)]
#print(levenshteinDistanceDP("m ae m", "m ae k "))

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


def calcDictDistance(chosen_phoneme, pronunciation_dict, dictPhonemeDist, phonemeIdx, dict_phonemes):
    
    """
    for line in lines: 
        columns = line.split()  # Split the line into columns using space as delimiter
        dict_word = columns[0]   # word - key
        dict_phoneme = ' '.join(columns[1:])   # phoneme - value   
        if dict_phoneme in pronunciation_dict:
            pronunciation_dict[dict_phoneme].append(dict_word)  # Append the word to the existing list
        else:
            pronunciation_dict[dict_phoneme] = [dict_word]
            
    """
    for phoneme in dict_phonemes:
        phonemeDistance = levenshteinDistanceDP(chosen_phoneme, phoneme)
        if phonemeDistance > 0 and phonemeDistance <= 1: # not adding the original word to the list; distance not more than 2
            dictPhonemeDist.append(str(int(phonemeDistance)) + " - " + phoneme + " ~ " + ', '.join(find_word(phoneme, pronunciation_dict)))
            phonemeIdx = phonemeIdx + 1
    
    return dictPhonemeDist
    

def select_top_alternatives(numWords, dictPhonemeDist):

    closestWords = []
    wordDetails = []
    currWordDist = 0
    dictPhonemeDist.sort()
    #print(dictPhonemeDist)
    for i in range(numWords):
        currWordDist = dictPhonemeDist[i]
        wordDetails = currWordDist.split("-")
        closestWords.append(wordDetails[1])
    return (f"Top {numWords} alternatives: {closestWords}")


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
    dictPhonemeDist = []
    phonemeIdx = 0
    
    
    for line in lines:
        columns = line.split()  # Split the line into columns using space as delimiter
        word = columns[0]   # word - value
        phoneme = ' '.join(columns[1:])   # phoneme - key  
        phonemes_list.append(phoneme) 
    
        if phoneme in pronunciation_dict:
            pronunciation_dict[phoneme].append(word)  # Append the word to the existing list
        else:
            pronunciation_dict[phoneme] = [word]
    chosen_phoneme = find_phoneme("cat", pronunciation_dict)
    calcDictDistance(chosen_phoneme, pronunciation_dict, dictPhonemeDist, phonemeIdx, phonemes_list)
        
    print(select_top_alternatives(3, dictPhonemeDist))
        
if __name__ == "__main__":
    main()