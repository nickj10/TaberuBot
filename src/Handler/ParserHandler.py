import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class ParserHandler:
    Terminals = ["hello", "verb", "gen", "ing", "random", "class", "category", "final", "bye"]
    noTerminals = ["START", "INTRO", "DATA", "PHRASE", "NOMINAL", "FUNCTION", "GEN", "ING"]
    table = [["INTRO", "PHRASE", "NOMINAL", None, "FUNCTION", "FUNCTION", "FUNCTION", None, "bye"],
             ["hello DATA", None, None, None, None, None, None, None, None],
             [None, "PHRASE", "NOMINAL", None, "FUNCTION", "FUNCTION", "FUNCTION", "final", None],
             [None, "verb NOMINAL", "NOMINAL", None, "FUNCTION", "FUNCTION", "FUNCTION", None, None],
             [None, None, "gen ING", None, "FUNCTION", "FUNCTION", "FUNCTION", None, None],
             [None, None, None, None, "random GEN", "class GEN", "category GEN", "final", None],
             [None, None, "gen", None, None, None, None, None, None],
             [None, None, None, "ing", None, None, None, None, None]
             ]

    def __init__(self, model):
        self.model = model

    def parse(self, tokens):
        stack = ["START"]  # initialize stack
        flag = True
        counter = 0

        if "bye" in tokens:
            logger.info("User has said goodbye to the bot.")
            return "bye"

        while counter < len(tokens):

            if counter == len(tokens) - 1:
                if tokens[len(tokens) - 1] != "final":
                    logger.error("The Sentence does not end in 'final'")
                elif tokens[len(tokens) - 2] == "hello":
                    return "hello"
                else:
                    """AQUI SALE EL TIPO QUE NECESITAMOS PARA ELEGIR LA FUNCIÓN"""
                    if tokens[len(tokens) - 3] == "random":
                        return "random"
                    elif tokens[len(tokens) - 3] == "class":
                        return "class"
                    elif tokens[len(tokens) - 3] == "category":
                        return "category"
                    elif tokens[len(tokens) - 3] == "gen":
                        return "ing"
                    else:
                        return "random"

            top = stack[len(stack) - 1]

            del stack[len(stack) - 1]

            if self.checkNoTerminal(top):
                """Buscamos la siguiente regla"""
                row = self.getnoTermIndex(top)
                column = self.getTermIndex(tokens[counter])

                # control negative values to avoid limit out of range exceptions
                if row < 0 or column < 0:
                    rule = None
                else:
                    rule = self.table[row][column]
                if rule is None:
                    """Error sintactico"""
                    logging.error("There is no defined Rule for the token: %s", tokens[counter])
                    newRules = []
                else:
                    newRules = rule.split(" ")
                    newRules.reverse()
                for r in newRules:
                    stack.append(r)
            elif self.checkTerminal(top):
                if top == tokens[counter]:
                    """Miramos si coincide el terminal analizado con el token del scanner"""
                    """Coinciden, miramos siguiente token del scanner"""
                    """next token"""
                    logging.debug("Next token")
                    counter = counter + 1
                else:
                    logging.error("Error in checking Terminal.")
            else:
                logging.warning("The error is not in the grammar.")

    def getnoTermIndex(self, noTerm):
        for i in range(len(self.noTerminals)):
            if self.noTerminals[i] == noTerm:
                return i
        return -1

    def getTermIndex(self, Term):
        for i in range(len(self.Terminals)):
            if self.Terminals[i] == Term:
                return i
        return -1

    def checkNoTerminal(self, top):
        for t in self.noTerminals:
            if t == top:
                return True
        return False

    def checkTerminal(self, top):
        for t in self.Terminals:
            if t == top:
                return True
        return False

    def checkIfKeyword(self, token):
        isKey = False
        keywordType = ""
        if token in self.model.get_verbs():
            isKey = True
            keywordType = "verb"
        elif token in self.model.ing_nouns:
            isKey = True
            keywordType = "ing"
        elif token in self.model.random_nouns:
            isKey = True
            keywordType = "random"
        elif token in self.model.category_nouns:
            isKey = True
            keywordType = "category"
        elif token in self.model.class_nouns:
            isKey = True
            keywordType = "class"
        elif token in self.model.intro_nouns:
            isKey = True
            keywordType = "hello"
        elif token in self.model.exit_nouns:
            isKey = True
            keywordType = "bye"
        elif token in self.model.general_nouns:
            isKey = True
            keywordType = "gen"
        return isKey, keywordType
