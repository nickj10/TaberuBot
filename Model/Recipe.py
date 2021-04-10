class Recipe:
    """Class that represents a Recipe"""
    likes = ""  # rating
    title = ""  # name of the recipe
    ingredients = []
    readyInMinutes = ""
    image = ""
    servings = ""
    dishTypes = []
    cuisines = []
    instructions = ""
    analyzedInstructions = []

    def __init__(self):
        return

    def __init__(self, rating, name, ingredients, readyInMinutes):
        self.rating = rating
        self.name = name
        self.ingredients = ingredients
        self.readyInMinutes = readyInMinutes

    def print_author(self):
        print(self.author)
