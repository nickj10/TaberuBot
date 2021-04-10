from Model.Recipe import Recipe
from Model.Ingredient import Ingredient

def prueba():
    ing = Ingredient("patata", "2", "unidades")
    ings = []
    ings.append(ing)
    classes = []
    aux = Recipe( 5, "pollo con patatas", ings, classes, "03:30:00")