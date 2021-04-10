class Recipe:
    """Clase que representa una receta"""
    author = ""
    rating = ""
    name = ""
    ingredients = ""
    foodClasses = ""
    time = ""

    def __init__(self, author, rating, name, ingredients, foodClasses, time):
        self.author = author
        self.rating = rating
        self.name = name
        self.ingredients = ingredients
        self.foodClasses = foodClasses
        self.time = time

    def print_author(self):
        print(self.author)
