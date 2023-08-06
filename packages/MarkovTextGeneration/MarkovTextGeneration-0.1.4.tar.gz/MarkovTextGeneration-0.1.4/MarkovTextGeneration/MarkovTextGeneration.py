import spacy
import re
import markovify
import nltk
from nltk.corpus import gutenberg
import warnings
import json
warnings.filterwarnings('ignore')
nlp = spacy.load('en_core_web_sm')


#source - https://towardsdatascience.com/text-generation-with-markov-chains-an-introduction-to-using-markovify-742e6680dc33

#utility function for text cleaning
def text_cleaner(text):
    text = re.sub(r'--', ' ', text)
    text = re.sub('[\[].*?[\]]', '', text)
    text = re.sub(r'(\b|\s+\-?|^\-?)(\d+|\d*\.\d+)\b','', text)
    text = ' '.join(text.split())
    return text


#next we will use spacy's part of speech to generate more legible text
class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ['::'.join((word.orth_, word.pos_)) for word in nlp(sentence)]
    def word_join(self, words):
        sentence = ' '.join(word.split('::')[0] for word in words)
        return sentence

def get_gutenberg_ids():
    return gutenberg.fileids()

def load_sents(texts, filetype="gutenberg", cleaner_functions=[], 
    clean_chapter_headings=True, base_cleaner_function=True, encoding=None, long=False):

    
    texts_raw = []
    sents = []


    if filetype == "gutenberg":
        for text in texts:
            try:
                texts_raw.append(gutenberg.raw(text))
            except:
                raise Exception(f"The only valid text options in the gutenberg corpus are: \n{gutenberg.fileids()}")
    elif filetype == "file":
        for text in texts:
            if encoding == None:
                f = open(text, "r")
            else:
                f = open(text, "r", encoding=encoding)
            texts_raw.append(f.read())
    
    else:
        raise Exception(f"{filetype} is not a valid option. Please refer to the docs")


    
    #clean the text
    for text in texts_raw:
        if clean_chapter_headings == True:
            text = re.sub(r'Chapter \d+', '', text)

        if base_cleaner_function == True:
            text = text_cleaner(text)

        for cleaner_function in cleaner_functions:
            text = cleaner_function(text)
        if long:
            nlp.max_length = len(text)+100
        text_doc = nlp(text)
        sents.append(' '.join([sent.text for sent in text_doc.sents if len(sent.text) > 1]))

    return_sents = ''
    for sent in sents:
        return_sents += sent

    return return_sents

def load_generator(sents, state_size=3, long=False):
    if long:
        generator = POSifiedText(sents, state_size=state_size, retain_original=False)
    else:
        generator = POSifiedText(sents, state_size=state_size)
    return generator

def generate_text(generator, max_chars=100, tries=100, clean_for_spaces=True):
    if max_chars == None:
        text = generator.make_sentence(tries=tries)
    else:
        text = generator.make_short_sentence(max_chars=max_chars, tries=tries)
    if clean_for_spaces:
        return clean_spaces(text)
    else:
        return text

def load_and_generate_text(texts, filetype, tries=100):
    generator = load_generator(load_sents(texts, filetype=filetype))
    return generate_text(generator, tries=tries)

def save_model(generator, path="model.json"):
    model_json = generator.to_json()
    jsonFile = open(path, "w")
    jsonFile.write(model_json)
    jsonFile.close()
    return True

def load_model(json_path):
    # Opening JSON file
    f = open(json_path,)
    
    # returns JSON object as 
    # a dictionary
    data = json.load(f)

    return POSifiedText.from_json(json.dumps(data))

def clean_spaces(text):
    return_str = []
    for k in range(0, len(text)):
        if text[k] == " " and text[k-1].isalpha() and text[k+1].isalpha() == False:
            pass
        else:
            return_str.append(text[k])
    return "".join(return_str)

