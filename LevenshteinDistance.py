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

# For the given word, find the corr. phoentic
def find_phoneme(given_key):
    given_key = given_key.upper()
    if given_key in pronunciation_dict:
        for key, value in pronunciation_dict.items():
            return(pronunciation_dict[given_key])
        
# from the given phoneme, return corr. word
def find_word(given_phoneme):
    if given_phoneme in pronunciation_dict.values():
        for key, value in pronunciation_dict.items():
            if value == given_phoneme:
                #print(key) 
                return key

# Get the beep-1.0 file
current_directory = os.path.dirname(os.path.abspath(__file__))
file_to_access = '\\beep-1.0'
pronunciation_dict = {}

# Open beep-1.0 file
file = open(current_directory + file_to_access, 'r')
lines = file.readlines()
file.close()
    
for line in lines:
    columns = line.split()  # Split the line into columns using space as delimiter
    word = columns[0]   # word - key
    phoneme = ' '.join(columns[1:])   # phoneme - value   
    pronunciation_dict[word] = phoneme # add pair to dict
    
def calcDictDistance(chosen_word, numWords):
    chosen_phoneme = find_phoneme(chosen_word)
    dictPhonemeDist = []
    phonemeIdx = 0
    
    for line in lines: 
        columns = line.split()  # Split the line into columns using space as delimiter
        dict_word = columns[0]   # word - key
        dict_phoneme = ' '.join(columns[1:])   # phoneme - value   
        pronunciation_dict[dict_word] = dict_phoneme # add pair to dict
        
        phonemeDistance = levenshteinDistanceDP(chosen_phoneme, dict_phoneme)
        #if phonemeDistance >= 3:
        #    phonemeDistance = 2
        if phonemeDistance > 0 and phonemeDistance <= 1: # not adding the original word to the list; distance not more than 2
            dictPhonemeDist.append(str(int(phonemeDistance)) + " - " + dict_phoneme + " ~ " + find_word(dict_phoneme))
            phonemeIdx = phonemeIdx + 1

    closestWords = []
    wordDetails = []
    currWordDist = 0
    dictPhonemeDist.sort()
    print(dictPhonemeDist)
    for i in range(numWords):
        currWordDist = dictPhonemeDist[i]
        wordDetails = currWordDist.split("-")
        closestWords.append(wordDetails[1])
    return (f"Top {numWords} alternatives: {closestWords}")
print(calcDictDistance("cat", 3))
