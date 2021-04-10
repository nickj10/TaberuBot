import re

class TokenHandler:
    expressions = []
    tokens = []
    text = []
    delim_list = "; ", ", ", "# ", "% ", "- "

    def __init__(self):
        return

    def tokenize(self, update, context):
        separatedText = self.custom_splitter(update.message.text)
        itr = iter(separatedText)
        for i in range(len(separatedText)):
            tokens = separatedText[i].split(' ')
            self.tokens.append(tokens)

        update.message.reply_text(self.tokens)
        return

    def custom_splitter(self, str_to_split):
        regular_exp = '|'.join(map(re.escape, self.delim_list))
        return re.split(regular_exp, str_to_split)
