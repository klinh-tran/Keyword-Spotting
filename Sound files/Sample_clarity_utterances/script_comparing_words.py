import os
import string
from datetime import datetime

current_directory = os.path.dirname(os.path.abspath(__file__))

######
# DEAL WITH DICTIONARY
dict_file_directory = '\\beep-1.0'
pronunciation_dict = {}
dict_file = open(os.getcwd() + dict_file_directory, 'r')

dict_words = []
for line in dict_file:
    # Split the line into columns using space as delimiter
        columns = line.split()
    
    # Get the word content
        word = columns[0]   # key
        dict_words.append(word)
    # Get the phonemes only
        phoneme = ' '.join(columns[1:])   # value   
        
        pronunciation_dict[word] = phoneme
dict_file.close()

######
# DEAL WITH AUDIO FILE
audio_script_file = '\\clarity_master.json'
audio_file = open(current_directory + audio_script_file, 'r')

audio_prompt_sentences = []

translator = str.maketrans('', '', string.punctuation.replace("'", "").replace("-", "")) # filter punctuation

for line in audio_file:
    line = line.strip()
    if line.startswith('{'):
        # Initialize a variable to store the prompt sentence
        prompt_sentence = None
        
        # Keep reading lines until the end of the paragraph (denoted by a '}')
        while '}' not in line:
            # Check if the line contains the "prompt" field
            if '"prompt"' in line:
                # Extract the prompt sentence from the line
                prompt_sentence = line.split('"prompt": ')[-1].strip('"')
                prompt_sentence = prompt_sentence.replace('\\u2018', '').replace('\\u2019', '').strip('"')
                prompt_sentence = prompt_sentence.translate(translator)
                if prompt_sentence.startswith("'"):
                        prompt_sentence = prompt_sentence[1:]
                if prompt_sentence.endswith("'"):
                    prompt_sentence = prompt_sentence[:-1]
            # Read the next line
            line = next(audio_file).strip()
        
        # Print the extracted prompt sentence
        if prompt_sentence:
            audio_prompt_sentences.append(prompt_sentence)
audio_file.close()

######
# Create text file to store mismatch words
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"file_{timestamp}.txt"
result_file = open(filename, 'w')

# compare and write mismatch words to the text file
for sentence in audio_prompt_sentences:
    #print(sentence)
    sentence = sentence.split()

    for indiv_word in sentence:
        if indiv_word.upper() not in dict_words:
            result_file.write(str(indiv_word.upper()) + '\n')
            #result_file.flush()
            #print(indiv_word)
