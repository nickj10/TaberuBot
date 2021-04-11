Terminals = ["hello","verb", "gen", "ingredients", "random", "class", "category", "final", "bye"]
noTerminals = ["START", "INTRO", "DATA", "PHRASE", "NOMINAL", "MORE", "FUNCTION", "ING"]
table =[["INTRO", "PHRASE", "NOMINAL", None, None, None, None, None, "bye"],
            ["hello DATA", None, None, None, None, None, None, None, None],
            [None, "PHRASE", "NOMINAL", None, None, None, None, "final", None],
            [None, "verb NOMINAL", "NOMINAL", None, None, None, None, None, None],
            [None, None, "gen MORE", None, None, None, None, None, None],
            [None, None, None, "FUNCTION", "FUNCTION", "FUNCTION", "FUNCTION", "final", None],
            [None, None, None, "ING", "random", "class", "category", None, None],
            [None, None, None, "ingredients", None, None, None, None, None]
            ]

"""TOKENS HARDCODED"""
tokens = ["hello", "verb", "gen", "random", "final"]
"""tokens = ["hello", "final"]"""



def parser():

    stack = []
    stack.append("START")
    flag = True
    counter = 0

    if "bye" in tokens:
        print("bye")
        return

    while counter < len(tokens):

        if counter == len(tokens) - 1:
            if  tokens[len(tokens)-1] != "final":
                print("sentencia no acaba en final")
            else:
                """AQUI SALE EL TIPO QUE NECESITAMOS PARA ELEGIR LA FUNCIÓN"""
                print(tokens[len(tokens)-2])
                break


        top = stack[len(stack)-1]

        del stack[len(stack)-1]


        if checkNoTerminal(top):
                    """Buscamos la siguiente regla"""
                    row = getnoTermIndex(top);
                    column = getTermIndex(tokens[counter]);

                    rule = table[row][column];
                    if rule is None :
                        """Error sintactico"""
                        print("There is no Rule by this");
                    else:

                        newRules = rule.split(" ");
                        newRules.reverse()
                        for r in newRules:
                            stack.append(r)


        elif checkTerminal(top):

                    if top == tokens[counter]:
                        """Miramos si coincide el terminal analizado con el token del scanner"""
                        """Coinciden, miramos siguiente token del scanner"""
                        """next token"""
                        print("next token")
                        counter = counter + 1

                    else:
                        print("error")

        else:
            print("error no esta en gramatica")


def getnoTermIndex(noTerm):
        for i in range(len(noTerminals)):
            if noTerminals[i] == noTerm:
                return i

        return -1


def getTermIndex(Term):
    for i in range(len(Terminals)):
        if Terminals[i] == Term:
            return i

    return -1

def checkNoTerminal(top):
        for t in noTerminals:
            if t == top:
                return True

        return False


def checkTerminal(top):
    for t in Terminals:
        if t == top:
            return True
    return False

