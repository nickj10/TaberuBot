import json
import requests

from Model.Ingredient import Ingredient
from Model.InstructionStep import InstructionStep
from Model.Instruction import Instruction
from Model.Recipe import Recipe
from decouple import config
import random

API_KEY = config('KEY')
base_url = 'https://api.spoonacular.com/recipes/'

class SpoonacularAPI:

    def __init__(self):
        self

    def sortRecipeRankingByLikes(self, value):
        return value['likes']

    def getRecipesWithId(self, dataset_sort):
        #arr_possible_recipes = []
        #for recipe in dataset_sort:
        n = random.randint(0, 19)
        id = str(dataset_sort[n]['id'])
        r = requests.get(base_url + id + '/information?apiKey=' + API_KEY)
        recipe_data = json.loads(r.text)

        #arr_possible_recipes.append(self.getRecipeInfo(recipe_data))
        return self.getRecipeInfo(recipe_data)

    def getRecipeInfo(self, dataset):
        arr_ingredients = []
        arr_step_ing = []
        arr_dishTypes = []
        arr_cuisines = []
        arr_step_equipment = []
        arr_steps = []
        instructions = ""

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

        recipe_object = Recipe(dataset['title'], arr_ingredients, dataset['readyInMinutes'], dataset['servings'], dataset['sourceUrl'], arr_dishTypes, arr_cuisines, dataset['instructions'], instructions)
        return recipe_object

    def getAPIRequestRandom(self):
        r = requests.get(base_url + 'random?apiKey=' + API_KEY)
        dataset = json.loads(r.text)['recipes'][0]
        return self.getRecipeInfo(dataset)

    def getAPIRequestByIngredient(self, param_ing):
        r = requests.get(base_url + 'findByIngredients?apiKey=' + API_KEY + '&ingredients=' + param_ing+ "&number=20")
        dataset = json.loads(r.text)
        #Returns sorted recipes by Likes.
        #dataset_sort = self.selectIdRandom(dataset)
        #dataset_sort = sorted(dataset, key=self.sortRecipeRankingByLikes, reverse=True)
        recipes = self.getRecipesWithId(dataset)
        return recipes

    def getAPIRequestByCuisine(self, param_cuisine):
        r = requests.get(base_url + 'complexSearch?apiKey=' + API_KEY + '&cuisine=' + param_cuisine + '&number=20')
        dataset = json.loads(r.text)
        recipes = self.getRecipesWithId(dataset['results'])
        return recipes

    def getAPIRequestByClass(self, param_class):
        r = requests.get(base_url + 'complexSearch?apiKey=' + API_KEY + '&type=' + param_class + '&number=20')
        dataset = json.loads(r.text)
        recipes = self.getRecipesWithId(dataset['results'])
        return recipes











