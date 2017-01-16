import requests 
import keys
import random
# import io
# from urllib.request import urlopen


def getRecipe():
	title = dishtype = source = instructions = ""
	cooking_time = preparation_time = 0
	ingredients = []
	request = None
	status = None

	try:
		request = requests.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/random?limitLicense=false&number=1&tags=vegetarian",
  headers={
    "X-Mashape-Key": keys.recipe_key,
    "Accept": "application/json"
  }
)
	except requests.ConnectionError: ##in the event of lack of connection
		status = "Connection Error in Recipe API"
		recipe_info = (title,cooking_time,preparation_time,dishtype,ingredients,source,instructions)
		return recipe_info,status
	except requests.Timeout: #poor connection
		status = "Recipe API Timed out"
		recipe_info = (title,cooking_time,preparation_time,dishtype,ingredients,source,instructions)
		return recipe_info,status
	except: #unknown issue
		status = "Unknown Issue with Recipe API"
		recipe_info = (title,cooking_time,preparation_time,dishtype,ingredients,source,instructions)
		return recipe_info,status

	status_code = request.status_code #200 is good. it went through. 429 means rate limit exceeded
	if status_code != 200: #If it didnt complete properly, then it will let us know what the code was 
		status = "Recipe API Returned Status Code" + str(status_code)
		recipe_info = (title,cooking_time,preparation_time,dishtype,ingredients,source,instructions)
		return recipe_info,status

	request = request.json()
	recipe = request["recipes"][0]
	#print(recipe)
	if "cookingMinutes" in recipe:
		cooking_time = recipe["cookingMinutes"]
	if "preparationMinutes" in recipe:
		preparation_time = recipe["preparationMinutes"]
	source = recipe["sourceUrl"]
	for ingredient in recipe["extendedIngredients"]:
		ingredients.append(ingredient["originalString"])
	title = recipe["title"]
	if recipe["dishTypes"] != []:
		dishtype = recipe["dishTypes"][0]
	instructions = recipe["instructions"]

	recipe_info = (title,cooking_time,preparation_time,dishtype,ingredients,source,instructions)
	return recipe_info,status


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
