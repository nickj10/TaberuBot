import nltk
import random
from nltk.corpus import stopwords, wordnet as wn
import string  # to process standard python strings
from langdetect import detect
from googletrans import Translator

lemmer = nltk.stem.WordNetLemmatizer()
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


class NLPHandler:
    language="en"

    def __init__(self):
        nltk.download('punkt')  # first-time use only
        nltk.download('wordnet')  # first-time use only
        nltk.download('stopwords')  # first-time use only
        nltk.download('averaged_perceptron_tagger')
        self.stop_words = stopwords.words('english')

    def analyzeText(self, update, context):
        raw = update.message.text
        raw = raw.lower()  # converts to lowercase
        sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
        word_tokens = nltk.word_tokenize(raw)  # converts to list of words
        print(sent_tokens)
        print(word_tokens)
        #tags_list contain tags from every phrase
        tags_list = []
        semantic_list = []
        for phrase in sent_tokens:
            result = self.LemNormalize(phrase)
            print("Result {}".format(result))
            #Tags (tuple) contains token and his grammar category
            tags = nltk.pos_tag(result)
            i = 0
            for w in result:
                if w not in self.stop_words:
                    i = i + 1
                else:
                    tags.pop(i)
            print(tags)
            semantic = []
            for tag in tags:
                #adjetivo
                if tag[1] == "JJ":
                    if self.if_nationality(tag[0]):
                        semantic.append("cuisine")
                    else:
                        semantic.append("random")
                #nouns
                elif tag[1] == "NN":
                    if self.if_food(tag[0]):
                        semantic.append("food")
                    #Parche: random reconocido como NN, no como JJ
                    elif self.if_random(tag[0]):
                        semantic.append("random")
                    else:
                        semantic.append("noun")
                #verb (assumed that if not adj or noun, is a verb)
                else:
                    if self.if_requestVerb(tag[0]):
                        semantic.append("verb")

        tags_list.append(tags)
        semantic_list.append(semantic)


        return tags_list, semantic_list

    # WordNet is a semantically-oriented dictionary of English included in NLTK.
    def LemTokens(self, tokens):
        return [lemmer.lemmatize(token) for token in tokens]

    def LemNormalize(self, text):
        return self.LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

    def if_food(self, word):
        syns = wn.synsets(str(word))
        for syn in syns:
            if 'food' in syn.lexname():
                return True

        return False

    def if_requestVerb(self, word):
        syns = wn.synsets(str(word))
        for syn in syns:
            if 'communication' in syn.lexname() or 'consumption' in syn.lexname() :
                return True

        return False

    def if_nationality(self, word):
        syns = wn.synsets(str(word))
        for syn in syns:
            if 'pert' in syn.lexname():
                return True
        return False

    def if_random(self, word):
        syns = wn.synsets(str(word), pos=wn.NOUN)
        for syn in syns:
            for lemma in syn.lemmas():
                print(lemma.name)
                if "random" == lemma.name() or "aleatory" == lemma.name():
                    print("random")
                    return True
        #Random y aleatory no suelen tener sinonimos en este wordnet
        #Otras palabras como irregular las coge como adjetivo
        if word == "random" or word == "aleatory":
            return True

        print("-")

        return False

    def if_recipe(self, word):
        syns = wn.synsets(str(word), pos=wn.NOUN)
        for syn in syns:
            if 'communication' in syn.lexname():
                return 1

        return 0

    def if_adj(self, word):
        syns = wn.synsets(str(word), pos=wn.ADJ)
        for syn in syns:
            print(syn.lexname())
            if 'communication' in syn.lexname():
                return 1

        return 0

    def greeting(self, sentence):
        GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey",)
        GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

        for word in sentence.split():
            if word.lower() in GREETING_INPUTS:
                return random.choice(GREETING_RESPONSES)


    def checkLanguage(self, message):
        lang = detect(message)
        if lang != self.language:
            self.language = lang
        if lang == "es":
            translator = Translator(service_urls=['translate.googleapis.com'])
            result = translator.translate(message, src="es", dest="en")
            return result
        if lang != "es" and lang != "en":
            return "Error, language not recognized"
        return message