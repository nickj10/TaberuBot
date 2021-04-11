import json
import requests

from Model.Ingredient import Ingredient
from Model.InstructionStep import InstructionStep
from Model.Instruction import Instruction
from Model.Recipe import Recipe
from decouple import config

API_KEY = ""
base_url = ""

class SpoonacularAPI:

    def __init__(self):
        self.API_KEY = config('KEY')
        self.base_url = 'https://api.spoonacular.com/recipes/'

    def getIngredientsParameters(self, param_ing):
        count = len(param_ing)
        param = ""
        if param_ing:  # if parameters is not empty
            for ing in param_ing:
                count_aux = + 1
                if count_aux <= (count - 1):
                    param = param + ing + ','
                else:
                    param = + ing
        return param

    def sortRecipeRankingByLikes(self, value):
        return value['likes']

    # def getRecipeWithId(id):

    def getAPIRequestRandom(self):
        r = requests.get(base_url + 'random?apiKey=' + API_KEY)
        dataset = json.loads(r.text)['recipes'][0]

        arr_ingredients= []
        arr_step_ing = []
        arr_dishTypes= []
        arr_cuisines = []
        arr_step_equipment = []
        arr_steps = []

        if dataset['extendedIngredients']:
            for ing in dataset['extendedIngredients']:
                name = ing['name']
                amount = ing['amount']
                unit = ing['unit']
                arr_ingredients.append(Ingredient(name, amount, unit))

        if dataset['dishTypes']:
            for dish in dataset['dishTypes']:
                arr_dishTypes.append(dish)

        if dataset['cuisines']:
            for cuisines in dataset['cuisines']:
                arr_cuisines.append(cuisines)

        #For the steps, we store the ingredients and equipments first
        if dataset['analyzedInstructions']: #if we have instructions
            if dataset['analyzedInstructions'][0]['steps']: #if we have steps to follow
                for steps in dataset['analyzedInstructions'][0]['steps']:
                    for step_ing in steps['ingredients']:
                        arr_step_ing.append(step_ing['name'])
                    for step_equip in steps['equipment']:
                        arr_step_equipment.append(step_equip['name'])
                    arr_steps.append(InstructionStep(arr_step_ing,arr_step_equipment))
                instructions = Instruction(arr_steps)

        recipe_object = (Recipe(dataset['title'],arr_ingredients,dataset['readyInMinutes'],dataset['servings'],arr_dishTypes,arr_cuisines, dataset['instructions'],instructions))
        return recipe_object

    def getAPIRequestByIngredient(self, param_ing):
        param = self.getIngredientsParameters(param_ing)
        r = requests.get(base_url + 'findByIngredients?apiKey=' + API_KEY + 'ingredients=' + param)
        dataset = r.json(r.text)
        dataset_sort = sorted(dataset, key=self.sortRecipeRankingByLikes)
        print('hello')

        # recipe_object = getRecipeWithId()









