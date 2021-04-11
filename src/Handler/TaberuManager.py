class TaberuManager:

    def __init__(self):
        self.tokens = []
        self.verbs = []
        self.ing_nouns = []
        self.random_nouns = []
        self.category_nouns = []
        self.class_nouns = []
        self.intro_nouns = []
        self.exit_nouns = []
        self.general_nouns = []

    def set_tokens(self, tokens):
        self.tokens = tokens

    def set_verbs(self, verbs):
        self.verbs = verbs

    def set_ing_nouns(self, ing_nouns):
        self.ing_nouns = ing_nouns

    def set_random_nouns(self, random_nouns):
        self.random_nouns = random_nouns

    def set_category_nouns(self, category_nouns):
        self.category_nouns = category_nouns

    def set_class_nouns(self, class_nouns):
        self.class_nouns = class_nouns

    def set_intro_nouns(self, intro_nouns):
        self.intro_nouns = intro_nouns

    def set_exit_nouns(self, exit_nouns):
        self.exit_nouns = exit_nouns

    def set_general_nouns(self, general_nouns):
        self.general_nouns = general_nouns
