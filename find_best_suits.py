import json
import os
from find_alternatives import extract_dictionary, find_word, find_phoneme
from find_mismatch import extract_dot_sentences
import torch
from lm_scorer.models.auto import AutoLMScorer as LMScorer
import spacy
import nltk
from nltk.stem import PorterStemmer
from language_tool_python import LanguageTool
from dictionaries.consonant_vowel_distance import phoneme_distance_dict


def extract_content_words(sentence):
    ''' 
    Remove stop words in the sentence
    Return list of content words of a sentence
    '''
    doc = nlp(sentence)
    filtered_words = [token.text for token in doc if ((not token.is_stop) and (not token.pos_ in ['PROPN', 'PRON']))]  # eliminate stop words and pronounces in sentences
    return filtered_words    
    
def update_json_file(file_path, data_to_update):  
    try:
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
    except Exception as e:
        print(e)
        existing_data = []
        
    existing_data.append(data_to_update)
    
    # Write the updated list back to the file
    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)

def phoneme_score(origin, alternative):
    diff = 0
    if (len(origin.split()) == len(alternative.split())):
        try:
            for i in range(len(origin.split())):
                diff += phoneme_distance_dict[origin.split()[i]][alternative.split()[i]]
        except Exception as e:
            print('Error calc phoneme difference: ', e)
    else:
        try:
            unique_chars = [char for char in origin.split() if char not in alternative.split()]
            unique_chars += [char for char in alternative.split() if char not in origin.split()]
            for elem in unique_chars:
                diff+=phoneme_distance_dict[elem]['']
        except Exception as e:
            print('Error calc phoneme difference: ', e)

    return round(diff,2)
    
def normalized_phoneme_score(score, min, max):
    try:
        if (max-min) !=0:
            return round(((score-min)/(max-min)),2)
        else: return round(score,2)
    except Exception as e:
        print('Error when norm-ing phoneme score:', e)

def main(sentences, word_alt_phonemes_dict):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    print('There are', len(sentences), 'sentences')
    lm_weight = 0.7
    phoneme_weight = 0.3
    
    for i in range(len(sentences)): # get individual sentence
        # print(sentences[i])
        content_words = []
        # Gather all prompts' content words
        for word in sentences[i].split(): # split sentence into words
            if (word in extract_content_words(sentences[i])):  # get content words of each sentence only
                # content_word = word
                content_words.append(word)
        
        # Map alternative words to each content word
        temp_score_dict = {}  # {content_word:{alternative1:phoneme_distance1, alternative2:phoneme_distance2,...},...}
        for content_word in content_words:
            content_word_pronunciation = find_phoneme(content_word, pronunciation_dict)
            alt_word_phoneme_score_dict = {}
            # alternatives_to_scores_dict.setdefault(content_word, [])
            for phoneme in word_alt_phonemes_dict[content_word.upper()]:  # distance-1 phonemes of each content word
                phoneme_distance = phoneme_score(content_word_pronunciation, phoneme[0])  # phoneme difference between content word and the candidate
                for alt_word in find_word(phoneme[0], pronunciation_dict):
                    alt_word_phoneme_score_dict[alt_word] = phoneme_distance
            temp_score_dict[content_word] = alt_word_phoneme_score_dict
        # print(temp_score_dict)
        # print('next')
        
        origin_alternatives_to_scores_dict = {}
        # Replace each content word by the alternative words -> modified sentences
        for key_elem, elem in temp_score_dict.items():
            alternatives_to_scores_dict = {}
            for key,value in elem.items():
                # Retrieve lemma form for comparison
                key_lemma = [token.lemma_ for token in nlp(key.lower())][0]
                key_elem_lemma = [token.lemma_ for token in nlp(key_elem)][0]

                ''' Replace each content word by the alternative words '''
                if (key.lower() not in sentences[i].split() 
                    and key.lower().isalnum()    # Contain alphanumeric symbols only (a-z in this given maerials) - reject if contain symbols
                    and key_lemma != key_elem_lemma
                    and key.lower() != key_elem+'er'
                    and key.lower() != key_elem+'r'):
                    modified_words = [key.lower() if (key_elem==word) else word for word in sentences[i].split()]  # replace chosen word by candidate words
                    modified_sentence = " ".join(modified_words)  # new sentence with candidate words
                    alternatives_to_scores_dict[modified_sentence] = value
            origin_alternatives_to_scores_dict[key_elem] = alternatives_to_scores_dict
            
        # Rank each new sentence for each content word's position
        word_new_sentences_scores = {}
        new_dict={}

        for key, values in origin_alternatives_to_scores_dict.items():
            if values:
                modified_sentence_score_dict = {}
                max_phoneme_score = max(values.values())
                min_phoneme_score = min(values.values())

                for new_sentence, phoneme_diff in values.items():
                    norm_phoneme_score = normalized_phoneme_score(phoneme_diff, min_phoneme_score, max_phoneme_score)
                    weighted_phoneme_score = phoneme_weight*norm_phoneme_score  # if norm_phoneme_score!=0 else 0
                    lm_score = scorer.sentence_score(new_sentence, log=True, reduce=reduce_option)
                    
                    # score = scorer.sentence_score(new_sentence, log=True, reduce=reduce_option)*1.1 - phoneme_diff*0.1 #more weighing on meaning, then about phonetic similarity
                    score = lm_score*lm_weight - weighted_phoneme_score
                    modified_sentence_score_dict[new_sentence] = score
                modified_sentence_score_dict = sorted(modified_sentence_score_dict.items(), key=lambda x:x[1], reverse=True) # sort based on score, descending order
                # print(modified_sentence_score_dict)
            # Select top 10 results per content word
            word_new_sentences_scores[key] = dict(modified_sentence_score_dict[:10]) # content_word:{sentence:score}
        # print(word_new_sentences_scores)
        # print()
        
        new_dict['id'] = i+1
        new_dict[sentences[i]] = 'Original sentence'
        new_dict.update(word_new_sentences_scores)
        if i==0 and i!=1 or (i+1)%100 == 1:
            filename = f"questions_{i+1}_{i+100}.json"
        else:
            filename = f"questions_{i-i%100+1}_{(i-i%100)+100}.json"
        update_json_file(current_directory+'\\test_designs\\'+filename, new_dict)
        print('completed',i+1,'th sentence')

if __name__ == '__main__':
    ''' Refer to JSON dicitonaries'''
    with open('test_materials\\words_to_alternative_phonemes.json', 'r') as f:
            word_alt_phonemes_data = json.load(f)

    pronunciation_dict, phonemes_list = extract_dictionary(file_to_access='\\dictionaries\\beep-2.0')
    
    # Load spaCy English model
    nlp = spacy.load("en_core_web_sm")
    
    ''' Gather sentences'''
    prompt_sentences = []
    extract_dot_sentences(prompt_sentences)

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    batch_size = 1
    scorer = LMScorer.from_pretrained("gpt2-medium", device=device, batch_size=batch_size)
    reduce_option = 'gmean'
    
    ''' main function '''
    main(prompt_sentences, word_alt_phonemes_data)