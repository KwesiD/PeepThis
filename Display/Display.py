import IP
import Weather
import pygame
import subprocess
import time 
import random



window = None
window_width = 0
window_height = 0

def getWeather():
	ip,location,status = IP.getLocation() #returns ip,(city,state,country,postal),status
	if status != None:
		##Send error message, do whatever, Idk
		print(status)
		exit(0)
	postal = location[3]
	 #returns  condition,(current,high,low),(rain,snow,clouds,humidity,wind_speed,icon),status
	condition,temp,precipitation,status = Weather.getWeatherFromZip(postal)
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

def text_objects(text, font):
    textSurface = font.render(text, True, (255,255,255))
    return textSurface, textSurface.get_rect()

def show_weather(condition,temp,precipitation,status):
	global window_height
	global window_width
	print(window_height)
	font_size = int((window_height)**(1/2))
	print(font_size)
	#text = condition + "\n" + "Now: " + str(temp[0]) + "\n" + "Hi: " + str(temp[1]) + "\n" + "Lo: " + str(temp[2]) + "\n" +\
	# str(precipitation[2])+ "\n" + str(precipitation[3]) + "\n" + "Winds at " + str(precipitation[4])
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

	image = pygame.transform.scale2x(pygame.image.load(precipitation[5]))
	window.blit(image,(window_width/4,window_height/5))

	for message in messages:
		font = pygame.font.Font('freesansbold.ttf',font_size)
		TextSurf, TextRect = text_objects(message, font)
		TextRect.center = position#((window_width/3),(window_height/5))
		window.blit(TextSurf, TextRect)
		position = (position[0],position[1] + (window_height/15))

	pygame.display.update()

	time.sleep(40)


create_screen()
condition,temp,precipitation,status = getWeather()
show_weather(condition,temp,precipitation,status)