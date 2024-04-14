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
    except Exception:
        existing_data = []
        
    existing_data.append(data_to_update)
    
    # Write the updated list back to the file
    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)
        
def is_grammar_issue(sentence):
    '''Check for grammar errors in a sentence'''
    matches = tool.check(sentence)
    return True if matches else False
        
def sentence_score_dict(original_sentence, alt_sentences, scorer, reduce_option):
    new_dict={}
    modified_sentence_score_dict = {}
    
    for sentence in alt_sentences:
        # if is_grammar_issue(sentence) == False:
            score = scorer.sentence_score(sentence, log=True, reduce=reduce_option)
            modified_sentence_score_dict[sentence] = score

    modified_sentence_score_dict = dict(sorted(modified_sentence_score_dict.items(), key=lambda x:x[1], reverse=True))
    new_dict[original_sentence] = "Original sentence"
    new_dict.update(modified_sentence_score_dict)
    print(new_dict)
    print()
    file_path = 'modified_sentence_score.json'
    update_json_file(file_path, new_dict)

def phoneme_score(origin, alternative):
    diff = 0
    # print(alternative.split())
    if (len(origin.split()) == len(alternative.split())):
        for i in range(len(origin.split())):
            diff += abs(phoneme_percentage_data[origin.split()[i]] - phoneme_percentage_data[alternative.split()[i]])
    else:
        unique_chars = [char for char in origin.split() if char not in alternative.split()]
        unique_chars += [char for char in alternative.split() if char not in origin.split()]
        for elem in unique_chars:
            diff+=phoneme_percentage_data[elem]
    return round(diff,2)
    
# def main(sentences, word_alt_phonemes_dict, scorer, reduce_option, ps):
def main(sentences, word_alt_phonemes_dict):
    #for sentence in sentences:
    print('There are', len(sentences), 'sentences')
    for i in range(0,5): # get individual sentence
        # print(sentences[i])
        content_words = []
        # gather all prompts' content words
        for word in sentences[i].split(): # split sentence into words
            if (word in extract_content_words(sentences[i])):  # get content words of each sentence only
                # content_word = word
                content_words.append(word)
        
        # map alternative words to each content word
        temp_score_dict = {}
        for content_word in content_words:
            content_word_pronunciation = find_phoneme(content_word, pronunciation_dict)
            alt_word_phoneme_score_dict = {}
            # alternatives_to_scores_dict.setdefault(content_word, [])
            if content_word != 'matt':
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
        #         # content_word_modified_sentences_dict.setdefault(key, [])
                ''' Replace each content word by the alternative words '''
                if (key.lower() not in sentences[i].split() and ps.stem(key.lower())!=key and ps.stem(key.lower())!=(key+"er") and ps.stem(key.lower())!=(key+"'")): # and ps.stem(v.lower())!=(key+"r")
                    modified_words = [key.lower() if (key_elem==word) else word for word in sentences[i].split()]  # replace chosen word by candidate words
                    modified_sentence = " ".join(modified_words)  # new sentence with candidate words
                    alternatives_to_scores_dict[modified_sentence] = value
            origin_alternatives_to_scores_dict[key_elem] = alternatives_to_scores_dict
        # print(origin_alternatives_to_scores_dict)
        # print()
        # print(origin_alternatives_to_scores_dict)
        
        # alternatives_to_scores_dict[key_elem] = elem
        # print(alternatives_to_scores_dict)
        # print()
        
        # Rank each new sentence for each content word's position
        word_new_sentences_scores = {}
        new_dict={}
        for key, values in origin_alternatives_to_scores_dict.items():
            modified_sentence_score_dict = {}
            for new_sentence, phoneme_diff in values.items():
                
                score = scorer.sentence_score(new_sentence, log=True, reduce=reduce_option)*0.6 - phoneme_diff*0.4 #more weighing on meaning, then about phonetic similarity
                modified_sentence_score_dict[new_sentence] = score
            modified_sentence_score_dict = dict(sorted(modified_sentence_score_dict.items(), key=lambda x:x[1], reverse=True))
            # print(modified_sentence_score_dict)
            word_new_sentences_scores[key] = modified_sentence_score_dict # content_word:{sentence:score}
        # print(word_new_sentences_scores)
        # print()
        new_dict[sentences[i]] = "Original sentence"
        new_dict.update(word_new_sentences_scores)
        file_path = 'modified_sentence_score.json'
        update_json_file(file_path, new_dict)
        print('completed',i,'th sentence')
            
            
            
        #         for phoneme in word_alt_phonemes_data[word.upper()]:  # get distance-1 phonemes of content words of each sentence
        #             for alt_words in find_word(phoneme[0], pronunciation_dict):
        #                 if (alt_words.lower() not in sentences[i].split()) and (alt_words.title() not in sentences[i].split()):
        #                     modified_words = [alt_words.lower() if word==content_word else word for word in sentences[i].split()]  # replace chosen word by candidate words
        #                     modified_sentence = " ".join(modified_words)  # new sentence with candidate words
        #                     print(modified_sentence)
        #                     modified_sentences.append(modified_sentence)
        # print(modified_sentences)                  
        # language model score and parse to JSON file
        #sentence_score_dict(sentences[i], modified_sentences)



if __name__ == '__main__':
    ''' Refer to 'JSON dicitonaries'''
    with open('words_to_alternative_phonemes.json', 'r') as f:
            word_alt_phonemes_data = json.load(f)

    # Open phoneme_percentage file
    current_directory = os.path.dirname(os.path.abspath(__file__))
    with open(current_directory + '\\dictionaries\\CMU_phoneme_percentage.json', 'r') as f:
            phoneme_percentage_data = json.load(f)

    pronunciation_dict, phonemes_list = extract_dictionary(file_to_access='\\dictionaries\\beep-2.0')
    
    # Load spaCy English model
    nlp = spacy.load("en_core_web_sm")
    
    nltk.download("punkt")
    # Initialize Python porter stemmer
    ps = PorterStemmer()
    
    # # Initialize LanguageTool with British English
    # tool = LanguageTool('en-GB')
    # tool.enable_spellchecking()
      
    ''' Gather sentences'''
    prompt_sentences = []
    extract_dot_sentences(prompt_sentences)
    # for s in prompt_sentences:
    #     if is_grammar_issue(s) == True:
    #         print(s)
    # print(sentences)   

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    batch_size = 1
    scorer = LMScorer.from_pretrained("gpt2-medium", device=device, batch_size=batch_size)
    reduce_option = 'gmean'
    
    ''' main function '''
    # main(prompt_sentences, word_alt_phonemes_data, scorer, reduce_option, ps)
    main(prompt_sentences, word_alt_phonemes_data)
    
