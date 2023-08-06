import spacy
import re
import markovify
import nltk
from nltk.corpus import gutenberg
import warnings
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


def load_sents(texts, filetype="gutenberg", cleaner_functions=[], clean_chapter_headings=True, base_cleaner_function=True):
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
            f = open(text, "r")
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

        text_doc = nlp(text)
        sents.append(' '.join([sent.text for sent in text_doc.sents if len(sent.text) > 1]))

    return_sents = ''
    for sent in sents:
        return_sents += sent

    return return_sents

def load_generator(sents):
    generator = POSifiedText(sents, state_size=3)
    return generator

def generate_text(generator, max_chars=100):
    if max_chars == None:
        return generator.make_sentence()
    else:
        return generator.make_short_sentence(max_chars=max_chars)

def load_and_generate_text(texts, filetype):
    generator = load_generator(load_sents(texts, filetype=filetype))
    return generate_text(generator)
