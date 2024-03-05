#import os
import json
from find_mismatch import extract_audio_script
from find_alternatives import extract_dictionary, calc_dict_distance, find_word

def extract_single_words(audio_prompt_sentences, unique_words_list = []):
    for sentence in audio_prompt_sentences:
        sentence = sentence.split()
        for indiv_word in sentence:
            indiv_word = indiv_word.strip("'").upper()
            if indiv_word not in unique_words_list:
                unique_words_list.append(indiv_word)
    unique_words_list.sort()
    
    # Store unique words to text file
    # current_directory = os.path.dirname(os.path.abspath(__file__))
    # text_file = open(f"{current_directory}\\text_files\\unique_words.txt", 'w')
    # for word in unique_words_list:
    #     text_file.write(str(word) + '\n')

    return unique_words_list

# Put JSON file in desired format
def format_json(dict):
    pairs = []
    for k, v in dict.items():
        pairs.append(f'  "{k}": {json.dumps(v, separators=(",", ":"))}')
    return '{\n' + ',\n'.join(pairs) + '\n}'

# Dictionary of words
def parse_to_json(unique_words_list, pronunciation_dict, phonemes_list):
    word_dict = {}
    
    # parse alternatives to each key
    lvt_dist = 1 # levenshtein distance
    phoneme_idx = 0
    
    for i in range(len(unique_words_list)):
        try:
            dict_phoneme_dists = []  # list of alternative phonemes with corr. distances
            formatted_list = [] # store formatted alternative phonemes, i.e. 'd ah v' -> ['d', 'ah', 'v']
            alternative_phonemes = (calc_dict_distance(unique_words_list[i], pronunciation_dict, lvt_dist, dict_phoneme_dists, phoneme_idx, phonemes_list))
            for phoneme in alternative_phonemes:
            #     splitted_phoneme = phoneme.split()
            #     #[indiv_phoneme.upper() for indiv_phoneme in splitted_phoneme]  # make phonemes in uppercase
                formatted_list.append([phoneme])
            word_dict[unique_words_list[i]] = formatted_list   # parse keys to JSON file
            print('word number ', i+1, 'th')
        except TypeError:
            print('word number ', i+1, 'th')
            word_dict[unique_words_list[i]] =[]
        
    # Define json file path
    file_path = 'words_to_alternative_phonemes.json'
    
    # Read existing JSON content
    try:
        with open(file_path, 'r') as json_file:
            existing_data = json.load(json_file)
    except Exception:
        existing_data = {}  # If file doesn't exist, initialize with empty dictionary

    # Update existing data with new data
    existing_data.update(word_dict)
    
    # Write the dictionary to a JSON files
    with open(file_path, 'w') as json_file:
        json_file.write(format_json(existing_data))

# Retrieve unique alternative phonemes used for the script words
def retrieve_alt_phonemes(unique_phonemes = set()):
    # Read the JSON file
    with open('words_to_alternative_phonemes.json', 'r') as f:
        data = json.load(f)
    for v in data.values():
        for elem in v:
            unique_phonemes.update(elem)
    unique_phonemes_list = list(unique_phonemes)
    unique_phonemes_list.sort()
    print(f"There are {len(unique_phonemes_list)} phonemes")
    return unique_phonemes_list

def bind_phonemes_words(phonemes_list, pronunciation_dict, phoneme_words_dict={}):
    for i in range(len(phonemes_list)   ):
            corr_words = find_word(phonemes_list[i], pronunciation_dict)
            phoneme_words_dict[phonemes_list[i]] = [[corr_word] for corr_word in corr_words]
            print(f"On {i+1}th phoneme")
    return phoneme_words_dict    

def parse_phonemes_words_dict(phoneme_words_dict):
    # Define json file path
    file_path = 'phonemes_to_corr_words.json'
    # Read existing JSON content
    try:
        with open(file_path, 'r') as json_file:
            existing_data = json.load(json_file)
    except Exception:
        existing_data = {}  # If file doesn't exist, initialize with empty dictionary

    # Update existing data with new data
    existing_data.update(phoneme_words_dict)
    
    # Write the dictionary to a JSON files
    with open(file_path, 'w') as json_file:
        json_file.write(format_json(existing_data))
        
def main():
    #######
    # Find unique words in the audio script
    audio_prompt_sentences = []
    extract_audio_script(audio_prompt_sentences)
    unique_words_list = extract_single_words(audio_prompt_sentences)
    print(f"There are {len(unique_words_list)} unique words in clarity_master.json script.")

    pronunciation_dict, phonemes_list = extract_dictionary(file_to_access='\\dictionaries\\beep-2.0')
    #######
    # Parse unique words to JSON file
    #parse_to_json(unique_words_list, pronunciation_dict, phonemes_list)
    
    ######
    # Retrieve unique phonemes from JSON file
    #print(retrieve_alt_phonemes())
    unique_phoneme_list = retrieve_alt_phonemes()
    phoneme_words_dict = bind_phonemes_words(unique_phoneme_list, pronunciation_dict)
    parse_phonemes_words_dict(phoneme_words_dict)
    
    
if __name__ == "__main__":
    main()
    
    
"""
def count_appearances(audio_prompt_sentences, indiv_words_list = []):
    counter = 0
    for sentence in audio_prompt_sentences:
        sentence = sentence.split()
        for indiv_word in sentence:
            indiv_word = indiv_word.strip("'").upper()
            indiv_words_list.append(indiv_word)
    
    non_dupe = list(set(indiv_words_list))
    non_dupe.sort()
    for i in range(len(non_dupe)):
        counter += indiv_words_list.count(non_dupe[i])
    print(counter)
"""


