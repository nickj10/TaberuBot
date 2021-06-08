import logging
import nltk
from langdetect import detect

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class ParserHandler:


    #Atributo v1
    grammar = nltk.CFG.fromstring("""
      P -> "NN" SV O | SV O
      SV -> V | V V
      V -> "VB" | "VBP"
      O -> "JJ" SN | SN
      SN -> "NN" SN | "NN"
      """)


    def __init__(self):
        self.rd_parser = nltk.RecursiveDescentParser(self.grammar)
        self.parse_keywords()

    def syntaxAnalysis(self, tokens):
        try:
            trees = self.rd_parser.parse(tokens)
            for tree in trees:
                print(tree)
                return True
        except:
            print("Error: hay tokens no incluidos gramatica")
        return False

    def semanticAnalysis(self, semantics, tags):
        function_id = -1
        if not "verb" in semantics:
            return False, -1
        if "random" in semantics:
            function_id = 0
        elif "food" in semantics:
            for tag in tags:
                isKey, kw = self.checkIfKeyword(tag[0])
                if isKey:
                    function_id = 3
                    break
                else:
                    function_id = 1
        elif "cuisine" in semantics:
            function_id = 2
        else:
            function_id = 0

        return True, function_id

    def createArguments(self, tags, semantics, function_id):
        i = 0
        str1 = ""
        n_ings = 0
        for tag in tags :
            if function_id == 1:
                if semantics[i] == "food":
                    if n_ings == 0:
                        str1 = tag[0]
                        n_ings = n_ings + 1
                    else:
                        str1 = str1 + ",+" + tag[0]
            elif function_id == 2:
                if semantics[i] == "cuisine":
                    str1 = tag[0]
            elif function_id == 3:
                if semantics[i] == "food":
                    str1 = tag[0]
            i += 1
        return str1


    def parse(self, tags, semantics):
        tokens = []
        #Recuperamos categorias gramaticales de los tags
        for tag in tags:
            tokens.append(tag[1])

        gram_ok = self.syntaxAnalysis(tokens)
        if gram_ok:
            print("gram ok")
            sem_ok, function_id = self.semanticAnalysis(semantics, tags)
            args = self.createArguments(tags, semantics, function_id)
            if sem_ok:
                print(function_id)
                return True, function_id, args
            print("Error: semantic")
        else:
            print("Error: sintaxis")

        return False, -1, ""






    def checkIfKeyword(self, token):
        isKey = False
        keywordType = ""
        if token in self.class_nouns:
            isKey = True
            keywordType = "class"

        return isKey, keywordType

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
                keywords = keywords.split(', ')

                if kw_type == "class_nouns":
                    self.class_nouns = keywords



            logger.info("Keywords have been parsed.")
        except IOError:
            logger.warning("File %s cannot be found\n", keywordsFilePath)
        else:
            f.close()


