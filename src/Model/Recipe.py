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

    def __init__(self, title, ingredients, readyInMinutes, servings, dishTypes, cuisines, instructions, analyzedInstructions):
        self.title = title
        self.ingredients = ingredients
        self.readyInMinutes = readyInMinutes
        self.servings = servings
        self.dishTypes = dishTypes
        self.cuisines = cuisines
        self.instructions = instructions
        self.analyzedInstructions = analyzedInstructions

    def print_author(self):
        print(self.author)
