import nltk
import random
from nltk.corpus import stopwords, wordnet as wn
import string  # to process standard python strings
from langdetect import detect
from googletrans import Translator

lemmer = nltk.stem.WordNetLemmatizer()
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

GREETING_INPUTS = ["hello", "hi", "greetings", "sup", "howdy", "hey", "yo", "yow"]
GREETING_RESPONSES = ["Hello there", "Hi", "Hi there", "Hello", "Hey"]
GOODBYE_INPUTS = ["bye", "goodbye"]
GOODBYE_RESPONSES = ["Goodbye", "Hope I see you soon", "Bye, have a nice day", "Bye, it has been a pleasure"]
ALREADY_GREETING_RESPONSES = ["Hey, you already greeted me, but nothing happens, I like to talk to you ", "You like to greet people huh? For me the more times the better! ", "Hello again friend! ", "I think you are trying to bug me with so much greeting :( "]
NOT_UNDERSTANDABLE_RESPONSES = ["I'm sorry, I didn't understand you. Can you put it another way? :) ",
                                "Sorry, I’m afraid I don’t follow you.",
                                "Excuse me, could you repeat it?",
                                "I’m sorry, I don’t understand. Could you say it again?",
                                "I’m sorry, I didn’t catch that. Would you mind saying it again?",
                                "I’m confused. Could you rephrase it for me?",
                                "Sorry, I didn’t understand. Could you say it in a different way?,"
                                "I didn’t hear you. Say again?"]

ERROR_MESSAGES = ["Oops, I think there was an error. Please try again later.", "Sorry, TaberuBot is under maintenance.",
                  "Please try again in a few minutes.", "Sorry, there was an error. Try again later."]


class NLPHandler:
    language="en"

    def __init__(self):
        nltk.download('punkt')  # first-time use only
        nltk.download('wordnet')  # first-time use only
        nltk.download('stopwords')  # first-time use only
        nltk.download('averaged_perceptron_tagger')
        self.stop_words = stopwords.words('english')
        self.waiting_ing = False
        self.waiting_args = ""
        self.greeting = False
        self.n_phrases = 0

    def analyzeText(self, update, context):
        raw = update.message.text
        raw = raw.lower()  # converts to lowercase
        sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
        word_tokens = nltk.word_tokenize(raw)  # converts to list of words
        print(sent_tokens)
        print(word_tokens)
        #tags_list contains tags from every phrase
        tags_list = []
        semantic_list = []
        for phrase in sent_tokens:

            result = self.LemNormalize(phrase)
            print("Result {}".format(result))
            #Tags (tuple) contains token and his grammar category
            tags = nltk.pos_tag(result)


            i = 0
            # Check if the user sent some greetings
            isGreeting, message = self.is_greeting(update, result)
            if isGreeting:
                #Already had a greeting
                if self.greeting:
                    update.message.reply_text(random.choice(ALREADY_GREETING_RESPONSES))
                else:
                    update.message.reply_text(message)
                    self.greeting = True
            isGoodbye, message = self.is_goodbye(update, result)
            if isGoodbye:
                update.message.reply_text(message)
                return False, False



            for w in result:
                if w not in self.stop_words:
                    #Filtering: nos quedamos solo con las categorias que queremos
                    if tags[i][1] != "VB" and tags[i][1] != "VBP" and tags[i][1] != "JJ" and tags[i][1] != "NN":
                        tags.pop(i)
                    else:
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

    def is_greeting(self, update, tokens):
        for word in tokens:
            if word.lower() in GREETING_INPUTS:
                return True, random.choice(GREETING_RESPONSES) + " " + update.message.from_user.first_name
        return False, ""

    def is_goodbye(self, update, tokens):
        for word in tokens:
            if word.lower() in GOODBYE_INPUTS or self.if_negation(word.lower):
                return True, random.choice(GOODBYE_RESPONSES) + " " + update.message.from_user.first_name
        return False, ""


    def if_negation(self, word):
        syns = wn.synsets(str(word))
        for syn in syns:
            if "adv" in syn.lexname():
                for lemma in syn.lemmas():
                    print(lemma.name())
                    print(word)
                    if word == lemma.name():
                        return True

        return False

    def addMoreIngredients(self, message):
        raw = message
        raw = raw.lower()  # converts to lowercase
        sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
        extra_ings = ""
        for phrase in sent_tokens:
            result = self.LemNormalize(phrase)
            print("Result {}".format(result))
            for w in result:
                    if self.if_food(w):
                        extra_ings = extra_ings + ",+" + w
                    elif self.if_negation(w):
                        return "", False
        return extra_ings, True


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

    def sendRandomNotUnderstandable(self):
        return random.choice(NOT_UNDERSTANDABLE_RESPONSES)

    def sendRandomErrorMessage(self):
        return random.choice(ERROR_MESSAGES)