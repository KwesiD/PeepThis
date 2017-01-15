import requests 
import keys
import random
# import io
# from urllib.request import urlopen


def getRecipe():
	response = requests.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/random?limitLicense=false&number=1&tags=vegetarian",
  headers={
    "X-Mashape-Key": keys.recipe_key,
    "Accept": "application/json"
  }
)
	response = response.json()
	recipe = response["recipes"][0]
	cooking_time = recipe["cookingMinutes"]
	preparation_time = recipe["preparationMinutes"]
	source = recipe["sourceUrl"]
	ingredients = []
	for ingredient in recipe["extendedIngredients"]:
		ingredients.append(ingredient["originalString"])
	title = recipe["title"]
	dishtype = recipe["dishTypes"][0]
	instructions = recipe["instructions"]

	recipe_info = (title,cooking_time,preparation_time,dishtype,ingredients,source,instructions)
	return recipe_info

# 	response = requests.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?"
# 		+"fillIngredients=false&ingredients="+ ingredients + "&limitLicense=false&number=5&ranking=1",
#   headers={
#     "X-Mashape-Key": keys.recipe_key,
#     "Accept": "application/json"
#   }
# )
# 	recipe = random.choice(response.json())
# 	title = recipe["title"]

# 	return title



# def chooseIngredients(): #turns out api already has a random recipie requests
# 	selection = ""
# 	ingredients = []
# 	ingredientslist = open("ingredientslist.txt",'r')
# 	for ingredient in ingredientslist:
# 		ingredients.append(ingredient.strip())
# 	number_of_ingredients = random.choice(range(5))
# 	if number_of_ingredients == 0:
# 		number_of_ingredients = 5
# 	for i in range(number_of_ingredients):
# 		ingredient = random.choice(ingredients)
# 		while(ingredient in selection):
# 			ingredient = random.choice(ingredients)
# 		selection += ingredient+","
# 	print(selection)
# 	return selection.strip(',')
