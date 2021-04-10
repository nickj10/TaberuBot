import json
import requests
from Test.TestIng import TestIng

r = requests.get('https://api.spoonacular.com/recipes/random?apiKey=a96da0b95b0e4491918db6ae0f947393')
ingredient = json.loads(r.text)['recipes'][0]['extendedIngredients']

#For recipes we need: likes, title, extendedIngredients[], readyInMinutes,
#servings, dishTypes[], cuisines[], instrucions, analyzedInstructions[]
arr_ingredients=[]
for ing in ingredient:
    name = ing['name']
    amount = ing['amount']
    unit = ing['unit']

arr_ingredients.append(TestIng(name,amount,unit))
print(arr_ingredients)
