from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import keys
import IP
import random


def getRestaurants():
	auth = Oauth1Authenticator(**keys.yelp_keys)
	client = Client(auth)
	location,status = IP.getLatLong() #returns ip,(city,state,country,postal),status
	if status != None:
		##Send error message, do whatever, Idk
		print(status)
		exit(0)
	cuisine = chooseCuisine()
	results = client.search_by_coordinates(*location,term=cuisine).businesses
	selection = random.choice(results)
	return selection
	#print(client.search_by_coordinates(*location,**terms).businesses[0].name)#.location.display_address)


def chooseCuisine():
	food = open("food.txt","r")
	cuisines = []
	for line in food:
		if line == "\n":
			continue
		cuisines.append(line.strip())
	selection = random.choice(cuisines)
	return selection
