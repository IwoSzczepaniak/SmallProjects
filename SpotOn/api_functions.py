# Iwo Szczepaniak
import requests
from time import sleep

### api
    # beta api - worse results(more ingredients), but probably better 
def recipes_API_beta(include, exclude):
    API_KEY = "775aba3235ed4debb5984acfd6b4589b"
    ENDPOINT = "https://api.spoonacular.com/recipes/complexSearch"
    # arrays doesn't work here
    p_include = ""
    for i,el in enumerate(include):
        if i > 0: p_include += ", " + el
        else: p_include += el
    p_exclude = ""
    for i,el in enumerate(exclude):
        if i > 0: p_exclude += ", " + el
        else: p_exclude += el
    params = {
    "query": p_include,
    "apiKey": API_KEY,
    "fillIngredients": "true",
    "intolerances": p_exclude,
    "sort": "min-missing-ingredients", # worse results
    "addRecipeNutrition": 'true',
    "number": "5"
    }

    response = requests.get(ENDPOINT, params=params)
    response_data = response.json()
    if response_data == None: return None
    recipes = response_data["results"]
    return recipes


    # api - worse looking, but probably more effective in lowering the extra elements- **require counting to 5**
def recipes_API_alfa(include, exclude):
    API_KEY = "775aba3235ed4debb5984acfd6b4589b"
    ENDPOINT = "https://api.spoonacular.com/recipes/complexSearch"
    
    params = {
    "query": include,
    "apiKey": API_KEY,
    "fillIngredients": "true",
    "intolerances": exclude,
    "addRecipeNutrition": 'true',
    "number": "10000000"
    }

    response = requests.get(ENDPOINT, params=params)
    response_data = response.json()
    recipes = response_data["results"]
    recipes.sort(key = lambda x: len(x["missedIngredients"]))

    return recipes


### print
    # console print - !not used anymore!
def print_recipes(recipes, include):
    i = 0
    for recipe in recipes:
        if i == 5: break
        elif i > 0: sleep(3)

        print(f"\n\n\t\tRECIPE TITLE:", recipe["title"])

        print(recipe["image"])

        print("\n\tINCLUDED ingredients are:")
        for inc in include: print(inc)
        print("\tEXTRA ingredients are:")
        for ing in recipe["missedIngredients"]:
            if ing not in include: 
                print(ing["original"])
        print("\tNUTRIENTS are:")
        for nut in recipe["nutrition"]["nutrients"]:
            if nut["name"] in ["Calories", "Carbohydrates", "Protein"]: 
                print(nut["name"], nut["amount"], nut["unit"])

        i += 1


    # return recipe variables from api
def return_recipe(recipe, include):
    title = recipe["title"]

    image_url = recipe["image"]

    extra_include = " "
    for ing in recipe["missedIngredients"]:
        if ing not in include: 
            extra_include += ing["original"] + "\n"

    nutrients = " "
    for nut in recipe["nutrition"]["nutrients"]:
        if nut["name"] in ["Calories", "Carbohydrates", "Protein"]: 
            nutrients += str(nut["name"]) +" "+ str(nut["amount"]) + str(nut["unit"]) + " "

    return title, image_url, extra_include, nutrients


