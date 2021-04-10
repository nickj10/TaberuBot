import json
import requests

from Model.Ingredient import Ingredient
from Model.InstructionStep import InstructionStep
from Model.Instruction import Instruction
from Model.Recipe import Recipe

r = requests.get('https://api.spoonacular.com/recipes/random?apiKey=a96da0b95b0e4491918db6ae0f947393')
dataset = json.loads(r.text)['recipes'][0]

#For recipes we need: likes, title, extendedIngredients[], readyInMinutes,
#servings, dishTypes[], cuisines[], instrucions, analyzedInstructions[]

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
            arr_steps.append(InstructionStep("",arr_step_ing,arr_step_equipment))
        instructions = Instruction("",arr_steps)


recipe_object = (Recipe(dataset['title'],arr_ingredients,dataset['readyInMinutes'],dataset['servings'],arr_dishTypes,arr_cuisines, dataset['instructions'],instructions))
