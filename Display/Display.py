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
	 #returns  condition,(current,high,low),(rain,snow,clouds,humidity,wind_speed),status
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
	text = condition + "\n" + "Now: " + str(temp[0]) + "\n" + "Hi: " + str(temp[1]) + "\n" + "Lo: " + str(temp[2]) + "\n" +\
	 str(precipitation[2])+ "\n" + str(precipitation[3]) + "\n" + "Winds at " + str(precipitation[4])
	font = pygame.font.Font('freesansbold.ttf',20)
	TextSurf, TextRect = text_objects(text, font)
	TextRect.center = ((window_width/3),(window_height/5))
	window.blit(TextSurf, TextRect)

	pygame.display.update()

	time.sleep(4)


create_screen()
condition,temp,precipitation,status = getWeather()
show_weather(condition,temp,precipitation,status)