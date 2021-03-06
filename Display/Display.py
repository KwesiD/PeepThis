import IP
import Weather
import pygame
import subprocess
import time as Time 
import random
import datetime
import Yelp
import Recipe
import Assistant

window = None
window_width = 0
window_height = 0
last_time_weather = 0
last_time_recipe = 0
last_time_restaurant = 0
objects = {} #this dictionary stores all the objects from all of the widgets and their positions

def getWeather():
	ip,location,status = IP.getLocation() #returns ip,(city,state,country,postal),status
	if status != None:
		##Send error message, do whatever, Idk
		print(status)
		exit(0)
	#postal = location[3]
	 #returns  condition,(current,high,low),(rain,snow,clouds,humidity,wind_speed,icon),status
	condition,temp,precipitation,status = Weather.getWeatherFromZip(location)
	if status != None:
		##Send error message, do whatever, Idk
		print(status)
		exit(0)

	return condition,temp,precipitation,status


def get_screen_resolution():
    output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
    resolution = output.split()[0].split(b'x')
    return {'width': resolution[0], 'height': resolution[1]}

def create_screen():
	global window
	global window_width
	global window_height
	dimensions = get_screen_resolution()
	window_width = int(dimensions["width"])
	window_height = int(dimensions["height"])
	pygame.init()
	window = pygame.display.set_mode((window_width,window_height))

def text_objects(text,font,color):
    textSurface = font.render(str(text), True,color)
    return textSurface, textSurface.get_rect()

def set_background(temptuple,precipitation):
	temp = temptuple[0]
	rain = precipitation[0]
	snow = precipitation[1]
	if rain != 0:
		bg = pygame.image.load("Images/rain.jpg")
	elif snow != 0:
		bg = pygame.image.load("Images/snow.jpg")
	elif temp > 70:
		bg = pygame.image.load("Images/hot.jpg")
	elif (temp > 55) and (temp <= 70):
		bg = pygame.image.load("Images/warm.jpg")
	elif (temp > 40) and (temp <= 55):
		bg = pygame.image.load("Images/moderate.jpg")
	elif (temp > 35) and (temp <= 40):
		bg = pygame.image.load("Images/chilly.jpg")
	elif (temp <= 35):
		bg = pygame.image.load("Images/cold.jpg")
	bg = pygame.transform.scale(bg,(window_width,window_height))
	bg_rect = bg.get_rect()
	window.blit(bg,bg_rect)

	pygame.display.update()

def show_weather(condition,temp,precipitation,status):
	global window_height
	global window_width
	#print(window_height)
	font_size = int((window_height)**(1/2))
	#print(font_size)
	messages = []
	messages.append(condition)
	messages.append("Now: " + str(temp[0]) + "°F")
	messages.append("Hi: " + str(temp[1]) + "°F")
	messages.append("Lo: " + str(temp[2])  + "°F")
	if precipitation[0] != 0:
		messages.append("Rain: " + precipitation[0])
	if precipitation[1] != 0:
		messages.append("Snow: " + precipitation[1])
	messages.append(precipitation[2])
	messages.append(precipitation[3])
	messages.append("Winds at " + str(precipitation[4]) + "mph")
	position = ((window_width/6),(window_height/5))	

	##weather icon
	image = pygame.transform.scale2x(pygame.image.load(precipitation[5]))
	window.blit(image,(window_width/4,window_height/5))
	objects["weather"] = [(image,(window_width/4,window_height/5))]

	for message in messages:
		font = pygame.font.Font('Ubuntu-M.ttf',font_size)
		TextSurf, TextRect = text_objects(message, font,(255,255,255))#white)
		TextRect.center = position#((window_width/3),(window_height/5))
		window.blit(TextSurf, TextRect)
		position = (position[0],position[1] + (window_height/15))
		objects["weather"].append((TextSurf,TextRect))

	pygame.display.update()

	#Time.sleep(4) ######Change later #Time is capital b/c it is imported as such due to conflicts with time var

def getTime():
	time = datetime.datetime.now()
	return time.strftime("%A, %B %d %Y %I:%M%p"),time.strftime("%I:%M%p")

def convert_time(prev): #converts time to 24hr
	segments = prev.split(":")
	hour = int(segments[0])
	minutes = segments[1][:2]
	if segments[1][2:] == "PM" and (hour < 12): #hour is less than 12 since 1-11pm is equal to 13-23 hours
		hour += 12
	return str(hour)+":"+str(minutes)

def compare_time(last,now): 
	now = convert_time(now)
	hours = (int(now.split(":")[0])-int(last.split(":")[0]))%24 #subtracts time and takes modulus
	minutes = ((int(now.split(":")[1])-int(last.split(":")[1]))%60)/60
	hours += minutes
	return hours

def show_time(time):
	global window_height
	global window_width
	font_size = int((1.50)*((window_height)**(1/2)))
	position = ((window_width/2),(window_height*(3/4)))
	font = pygame.font.Font('Ubuntu-L.ttf',font_size)
	TextSurf, TextRect = text_objects(time, font,(255,255,255))
	TextRect.center = position
	window.blit(TextSurf, TextRect)
	objects["time"] = [(TextSurf,TextRect)]
	pygame.display.update()
	#Time.sleep(4)
	#cant use time.sleep here unless time var is renamed

def show_recipe():
	recipe_response = Assistant.getRecipe()
	font_size = int((.75)*((window_height)**(1/2)))
	position = ((window_width*(4/6)),(window_height*(1/5)))
	objects["recipe"] = []
	empty = [None,"",0]
	for line in recipe_response:
		if line in empty:
			continue
		font = pygame.font.Font('Ubuntu-L.ttf',font_size)
		TextSurf, TextRect = text_objects(line, font,(255,255,255))#white)
		TextRect.center = position#((window_width/3),(window_height/5))
		window.blit(TextSurf, TextRect)
		position = (position[0],position[1] + (window_height/15))
		objects["recipe"].append((TextSurf,TextRect))

	pygame.display.update()

def show_restaurant():
	restaurant_response = Assistant.getRestaurant()
	font_size = int((.75)*((window_height)**(1/2)))
	position = ((window_width*(4/6)),(window_height*(2.5/5)))
	objects["restaurant"] = []
	empty = [None,"",0]
	for line in restaurant_response:
		if line in empty:
			continue
		font = pygame.font.Font('Ubuntu-L.ttf',font_size)
		TextSurf, TextRect = text_objects(line, font,(255,255,255))#white)
		TextRect.center = position#((window_width/3),(window_height/5))
		window.blit(TextSurf, TextRect)
		position = (position[0],position[1] + (window_height/15))
		objects["restaurant"].append((TextSurf,TextRect))

	pygame.display.update()

def update_window(): #refreshes the screen using previously stored widget objects
	window.fill((0,0,0)) #clear to black
	for widget in objects:
		for item in objects[widget]:
			window.blit(*item)
	pygame.display.update()


create_screen()
condition,temp,precipitation,status = getWeather()
show_weather(condition,temp,precipitation,status)
date_time,time = getTime()
last_time_weather = last_time_restaurant = last_time_recipe = convert_time(time)
show_time(date_time)
show_recipe()
show_restaurant()
while(True):
	date_time,time = getTime() #gets current time

	##weather check
	if compare_time(last_time_weather,time) >= .20:
		condition,temp,precipitation,status = getWeather()
		show_weather(condition,temp,precipitation,status)
		last_time_weather = convert_time(time)

	if compare_time(last_time_recipe,time) >= 12:
		show_recipe()
		last_time_recipe = convert_time(time)

	if compare_time(last_time_restaurant,time) >= 12:
		show_restaurant()
		last_time_restaurant = convert_time(time)


	show_time(date_time)
	update_window()
	#Time.sleep(4)
