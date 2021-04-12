class TaberuManager:

    def __init__(self):
        self.tokens = []
        self.values = []
        self.categories = []
        self.classes = []
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

    def set_values(self, values):
        self.values = values

    def set_categories(self, categories):
        self.categories = categories

    def set_classes(self, classes):
        self.classes = classes

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

    def get_tokens(self):
        return self.tokens

    def get_values(self):
        return self.values

    def get_categories(self):
        return self.categories

    def get_classes(self):
        return self.classes

    def get_verbs(self):
        return self.verbs
