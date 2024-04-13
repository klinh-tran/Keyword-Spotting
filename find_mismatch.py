import os
from datetime import datetime

current_directory = os.path.dirname(os.path.abspath(__file__))

######
def extract_dictionary(dict_words):
    '''
    Deal with dictionary
    '''
    dict_file_directory = '\\dictionaries\\beep-2.0'
    pronunciation_dict = {}
    dict_file = open(os.getcwd() + dict_file_directory, 'r')

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
def extract_dot_sentences(audio_prompt_sentences):
    '''Deal with audio file
    
    Collect all sentences followed by "dot" in "Sound files\Sample_clarity_utterances\clarity_master.json"
    '''
    audio_script_file = '\\updated_clarity_master.json'
    audio_file = open(current_directory + audio_script_file, 'r')

    for line in audio_file:
        line = line.strip()
        if line.startswith('{'):
            dot_sentence = None  # Initialize a variable to store the dot sentence
            
            while '}' not in line:
                # Check and extract "dot" lines, remove unnecessary punctuations " and \
                if '"dot"' in line:
                    dot_sentence = line.split('"dot": ')[-1].strip('"')
                    dot_sentence = dot_sentence.replace('\\', '')
                # Read the next line
                line = next(audio_file).strip()
            
            # Store extracted dot sentence
            if dot_sentence:
                audio_prompt_sentences.append(dot_sentence)
    audio_file.close()

######
def main():
    '''
    Store mismatch words in a text file
    '''
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"file_{timestamp}.txt"
    result_file = open(f"{current_directory}\\text_files\\{filename}", 'w')
    
    dict_words = []
    extract_dictionary(dict_words)
    
    audio_prompt_sentences = []
    extract_dot_sentences(audio_prompt_sentences)
    
    # Compare and write mismatch words to the text file
    for sentence in audio_prompt_sentences:
        sentence = sentence.split()

        for indiv_word in sentence:
            indiv_word = indiv_word.strip("'").upper() # remove remaining ' and put uppercase to match dictionary
            if indiv_word not in dict_words:
                result_file.write(str(indiv_word) + '\n')

if __name__ == "__main__":
    main()