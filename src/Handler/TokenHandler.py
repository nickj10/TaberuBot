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

    def __init__(self, model):
        self.model = model

        return

    def tokenize(self, update, context):
        separatedText = self.custom_splitter(update.message.text)
        itr = iter(separatedText)
        for i in range(len(separatedText)):
            tokens = separatedText[i].split(' ')
            for token in tokens:
                if token in self.prepositions:
                    tokens.remove(token)
            self.tokens.append(tokens)
        self.model.set_token(self.tokens)
        # update.message.reply_text(self.tokens)
        return

    def custom_splitter(self, str_to_split):
        regular_exp = '|'.join(map(re.escape, self.delim_list))
        return re.split(regular_exp, str_to_split)

    def parse_keywords(self):
        keywordsFilePath = 'resources\\keywords.txt'
        try:
            with open(keywordsFilePath) as f:
                lines = f.readlines()
        except IOError:
            logger.warning("File %s cannot be found\n", keywordsFilePath)
        else:
            f.close()
