class IngredientHandler:

    recipes = []
    next_recipe = 0

    def __init__(self, spoonacular):
        self.spoonacular = spoonacular

    def getRecipesByIngredient(self, ingredients):
        # self.recipes = self.spoonacular.getRecipesByIngredient(ingredients)
        self.next_recipe = 0  # initialize pointer when retrieving a new set of recipes
        return self

    def getNextRecipe(self):
        self.next_recipe += 1
        return self.recipes[self.next_recipe]