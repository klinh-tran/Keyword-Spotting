import json
from find_alternatives import extract_dictionary, find_word
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

def main(sentences, word_alt_phonemes_dict, scorer, reduce_option, ps):
    #for sentence in sentences:
    for i in range(4,5): # get individual sentence
        # print(sentences[i])

        content_words = []
        # gather all prompts' content words
        for word in sentences[i].split(): # split sentence into words
            if (word in extract_content_words(sentences[i])):  # get content words of each sentence only
                # content_word = word
                content_words.append(word)
        
        # map alternative words to each content word
        content_word_alt_words_dict = {}
        for content_word in content_words:
            content_word_alt_words_dict.setdefault(content_word, [])
            for phoneme in word_alt_phonemes_dict[content_word.upper()]:  # distance-1 phonemes of each content word
                for alt_words in find_word(phoneme[0], pronunciation_dict):
                    content_word_alt_words_dict[content_word].append(alt_words)
        # print(content_word_alt_words_dict)
        # print()
        
        content_word_modified_sentences_dict = {}
        # Replace each content word by the alternative words -> modified sentences
        for key,values in content_word_alt_words_dict.items():
            content_word_modified_sentences_dict.setdefault(key, [])
            # print(key)
            for v in values:
                ''' Replace each content word by the alternative words '''
                if (v.lower() not in sentences[i].split() and ps.stem(v.lower())!=key and ps.stem(v.lower())!=(key+"er") and ps.stem(v.lower())!=(key+"'")): # and ps.stem(v.lower())!=(key+"r")
                    # print(v.lower())
                    modified_words = [v.lower() if (word==key) else word for word in sentences[i].split()]  # replace chosen word by candidate words
                    modified_sentence = " ".join(modified_words)  # new sentence with candidate words
                    content_word_modified_sentences_dict[key].append(modified_sentence)
        # print(content_word_modified_sentences_dict)
        # print()
        
        # Rank each new sentence for each content word's position
        for key, new_sentences in content_word_modified_sentences_dict.items():
            #x=0
            # print(key, new_sentences)
            sentence_score_dict(sentences[i], new_sentences, scorer, reduce_option)
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

    pronunciation_dict, phonemes_list = extract_dictionary(file_to_access='\\dictionaries\\beep-2.0')
    
    # Load spaCy English model
    nlp = spacy.load("en_core_web_sm")
    
    nltk.download("punkt")
    # Initialize Python porter stemmer
    ps = PorterStemmer()
    
    # Initialize LanguageTool with British English
    tool = LanguageTool('en-GB')
    tool.enable_spellchecking()
      
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
    main(prompt_sentences, word_alt_phonemes_data, scorer, reduce_option, ps)
    
