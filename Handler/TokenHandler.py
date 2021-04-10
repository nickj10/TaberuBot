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
        update.message.reply_text(separatedText)
        return

    def custom_splitter(self, str_to_split):
        regular_exp = '|'.join(map(re.escape, self.delim_list))
        return re.split(regular_exp, str_to_split)
