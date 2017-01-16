import keys
import user_info
import IP
import Recipe
import Yelp
import Calendar
import SMS
import Assistant_Info as assistant

def getRecipe():
	recipe_info,status = Recipe.getRecipe()
	if status != None:
		##Send error message, do whatever, Idk
		print(status)
		exit(0)
	SMS.send_sms("Here's today's recipe! " + recipe_info[0] + ": " +  recipe_info[5])
	#(title,cooking_time,preparation_time,dishtype,ingredients,source,instructions)
	header = "Here's today's recipe!"
	title = recipe_info[0] + ":"
	cook_time = recipe_info[1]
	prep_time = recipe_info[2]
	dishtype = recipe_info[3]
	if dishtype != "":
		header += " It's " + dishtype + " food!!"
	if prep_time != 0:
		prep_time = "It takes " + str(prep_time) + " minutes to prepare!"

	if cook_time != 0:
		cook_time = "It takes " + str(cook_time) + " minutes to cook!"
	response = [header,title,prep_time,cook_time]
	return response

def getRestaurant():
	restaurant,status = Yelp.getRestaurant()
	if status != None:
		##Send error message, do whatever, Idk
		print(status)
		exit(0)
	header = "You should try " + restaurant.name + " today."
	stars = "*"*round(int(restaurant.rating))
	location = "They're at " + " ".join(restaurant.location.display_address)
	response = [header,stars,location]
	return response