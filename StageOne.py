"""
TODO: 
1. Get the phonetic parts only
   Get the word parts only
   For the given word, find the corr. phoentic
   For the given phonetic, find the corr. word
"""

dict = {}

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
        dict[word] = phoneme
print(dict)
#file.close()

given_key = "A"
if given_key in dict:
    print(dict[given_key])
    
give_val = "ay k ax"
if give_val in dict.values():
    for key, value in dict.items():
        if value == give_val:
            print(key) 
############################################
"""
TODO:
2. Filter the beep list, choose the meaningful and unique words only
3. Find similar words (e.g using regex)
"""
