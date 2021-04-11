import re
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class TokenHandler:
    expressions = []
    tokens = []
    text = []
    delim_list = "; ", ", ", "# ", "% ", "- "
    prepositions = ["about", "above", "across", "after", "against", "among", "around", "at",
                    "before", "behind", "below", "beside", "between", "by", "down", "during",
                    "for", "from", "in", "inside", "into", "near", "of", "off", "on", "out",
                    "over", "through", "to", "toward", "under", "up"]

    def __init__(self, model, parser):
        self.model = model
        self.parser = parser

        return

    def get_model(self):
        return self.model

    def get_parser(self):
        return self.parser

    def tokenize(self, update, context):
        lowerText = update.message.text.lower()
        separatedText = self.custom_splitter(lowerText)
        itr = iter(separatedText)
        for i in range(len(separatedText)):
            tokens = separatedText[i].split(' ')
            for token in tokens:
                if token in self.prepositions:
                    tokens.remove(token)
            self.tokens.append(tokens)
        self.model.set_tokens(self.tokens)
        # update.message.reply_text(self.tokens)
        return

    def parse_tokens(self, tokens):
        return self.parser.parse(tokens)

    def custom_splitter(self, str_to_split):
        regular_exp = '|'.join(map(re.escape, self.delim_list))
        return re.split(regular_exp, str_to_split)

    def parse_keywords(self):
        keywordsFilePath = '../resources/keywords.txt'
        try:
            with open(keywordsFilePath) as f:
                lines = f.readlines()

            for line in lines:
                line = line.replace("\n", "")
                eachLine = line.split(':')
                kw_type = eachLine[0].strip()
                keywords = eachLine[1].replace("\n", "")
                keywords = keywords.strip()
                keywords = keywords.split(' ')
                if kw_type == "verbs":
                    self.model.set_verbs(keywords)
                elif kw_type == "ing_nouns":
                    self.model.set_ing_nouns(keywords)
                elif kw_type == "random_nouns":
                    self.model.set_random_nouns(keywords)
                elif kw_type == "category_nouns":
                    self.model.set_category_nouns(keywords)
                elif kw_type == "class_nouns":
                    self.model.set_class_nouns(keywords)
                elif kw_type == "intro_nouns":
                    self.model.set_intro_nouns(keywords)
                elif kw_type == "exit_nouns":
                    self.model.set_exit_nouns(keywords)
                elif kw_type == "general_nouns":
                    self.model.set_general_nouns(keywords)

            logger.info("Keywords have been parsed.")
        except IOError:
            logger.warning("File %s cannot be found\n", keywordsFilePath)
        else:
            f.close()
