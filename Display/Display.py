import IP
import Weather
import pygame
import subprocess
import time 
import random



window = None
def getWeather():
	ip,location,status = IP.getLocation() #returns ip,(city,state,country,postal),status
	if status != None:
		##Send error message, do whatever, Idk
		print(status)
		exit(0)
	postal = location[3]
	 #returns  condition,(current,high,low),(rain,snow,clouds,humidity,wind_speed),status
	condition,temp,precipitation,status = Weather.getWeatherFromZip(postal)
	return condition,temp,precipitation,status


def get_screen_resolution():
    output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
    resolution = output.split()[0].split(b'x')
    return {'width': resolution[0], 'height': resolution[1]}

def create_screen():
	dimensions = get_screen_resolution()
	width = int(dimensions["width"])
	height = int(dimensions["height"])
	pygame.init()
	window = pygame.display.set_mode((width,height))

create_screen()