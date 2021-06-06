import nltk
import random
from nltk.corpus import stopwords, wordnet as wn
import string  # to process standard python strings
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Enable lemmer and punctuation removal
lemmer = nltk.stem.WordNetLemmatizer()
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


class NLPHandler:

    def __init__(self):
        nltk.download('punkt')  # first-time use only
        nltk.download('wordnet')  # first-time use only
        nltk.download('stopwords')  # first-time use only
        self.stop_words = stopwords.words('english')

    def analyzeText(self, update, context):
        raw = update.message.text
        raw = raw.lower()  # converts to lowercase

        sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
        word_tokens = nltk.word_tokenize(raw)  # converts to list of words
        print(sent_tokens)
        print(word_tokens)

        for phrase in sent_tokens:
            result = self.LemNormalize(phrase)
            print("Result {}".format(result))

            filtered_sentence = [w for w in result if not w.lower() in self.stop_words]
            # filtered_sentence = []
            # for w in result:
            #    if w not in stop_words:
            #        filtered_sentence.append(w)

            print("Filtered {}".format(filtered_sentence))

            # food = wn.synset('food.n.02')
            # food_list = list(set([w for s in food.closure(lambda s: s.hyponyms()) for w in s.lemma_names()]))

            for filtered in filtered_sentence:
                # check the tokens
                if self.if_food(filtered) == 1:
                    print(filtered, "is food")

            # check if it's a greeting
            greeting_response = self.greeting(filtered_sentence)
            if greeting_response:
                update.message.reply_text(greeting_response)
            else:
                logger.warning("The greeting message response is empty.")

    # WordNet is a semantically-oriented dictionary of English included in NLTK.
    def LemTokens(self, tokens):
        return [lemmer.lemmatize(token) for token in tokens]

    def LemNormalize(self, text):
        return self.LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

    def if_food(self, word):
        syns = wn.synsets(str(word), pos=wn.NOUN)
        for syn in syns:
            if 'food' in syn.lexname():
                return 1
        return 0

    def greeting(self, sentence):
        GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
        GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

        for word in sentence:
            if word.lower() in GREETING_INPUTS:
                return random.choice(GREETING_RESPONSES)
