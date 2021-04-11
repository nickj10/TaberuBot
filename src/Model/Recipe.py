class Recipe:
    """Class that represents a Recipe"""
    id = ""
    likes = ""  # rating
    title = ""  # name of the recipe
    ingredients = []
    readyInMinutes = ""
    image = ""
    servings = ""
    sourceUrl = ""
    dishTypes = []
    cuisines = []
    instructions = ""
    analyzedInstructions = []

    def __init__(self, title, ingredients, readyInMinutes, servings, sourceUrl, dishTypes, cuisines, instructions, analyzedInstructions):
        self.title = title
        self.ingredients = ingredients
        self.readyInMinutes = readyInMinutes
        self.servings = servings
        self.sourceUrl = sourceUrl
        self.dishTypes = dishTypes
        self.cuisines = cuisines
        self.instructions = instructions
        self.analyzedInstructions = analyzedInstructions

