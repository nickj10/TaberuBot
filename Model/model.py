from Model.Recipe import Recipe
from Model.Author import Author
from Model.Ingredient import Ingredient
from Model.FoodClass import FoodClass

def prueba():
    ing = Ingredient("patata", "2", "unidades")
    aut = Author("omar", "omar@gmail")
    ings = []
    ings.append(ing)
    classes = []
    classes.append(FoodClass("veggie"))
    aux = Recipe(aut, 5, "pollo con patatas", ings, classes, "03:30:00")