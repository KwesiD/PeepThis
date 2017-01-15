import requests
from keys import weather_key
import IP
from urllib.request import urlopen
import io


#gets weather data
def getWeatherFromZip(location):
	request = None
	current = high = low = 0
	wind_speed = 0
	clouds = humidity = 0
	condition = None
	rain = snow = 0
	status = None
	status_code = 0

	try:
		request = requests.get("http://api.openweathermap.org/data/2.5/weather?zip=" + str(location[3]) + "," 
		+ location[2] + "&units=imperial" + "&APPID=" + weather_key) #gets weather data
	except requests.ConnectionError: ##in the event of lack of connection
		status = "Connection Error in Weather API"
		return condition,(current,high,low),(rain,snow,clouds,humidity,wind_speed),status
	except requests.Timeout: #poor connection
		status = "Weather API Timed out"
		return condition,(current,high,low),(rain,snow,clouds,humidity,wind_speed),status
	except: #unknown issue
		status = "Unknown Issue with Weather API"
		return condition,(current,high,low),(rain,snow,clouds,humidity,wind_speed),status

	status_code = request.status_code #200 is good. it went through.
	if status_code != 200: #If it didnt complete properly, then it will let us know what the code was 
		status = "Weather API Returned Status Code" + str(status_code)
		return condition,(current,high,low),(rain,snow,clouds,humidity,wind_speed),status

	data = request.json()
	condition = data["weather"][0]["description"]
	current = data["main"]["temp"]
	high = data["main"]["temp_max"]
	low = data["main"]["temp_min"]
	wind_speed = data["wind"]["speed"]
	clouds = cloud_eval(data["clouds"]["all"])
	humidity = humid_eval(data["main"]["humidity"])
	icon = data["weather"][0]["icon"]
	if "rain" in data:  #because it is not always snowing 
		rain = data["rain"]["3h"]
	if "snow" in data:
		snow = data["snow"]["3h"]

	## handle exceptions
	url = "http://openweathermap.org/img/w/" + str(icon) + ".png"
	image = io.BytesIO(urlopen(url).read())
	##

	return condition,(current,high,low),(rain,snow,clouds,humidity,wind_speed,image),status


def cloud_eval(cloud):
	if cloud < 10:
		return "No Clouds"
	if (cloud >= 10) and (cloud < 25):
		return "Slightly Cloudy"
	elif (cloud >= 25) and (cloud < 50):
		return "Partially Cloudy"
	else:
		return "Heavy Cloud Coverage"

def humid_eval(humid):
	if humid < 10:
		return "No Humidity"
	if (humid >= 10) and (humid < 25):
		return "Slightly Humid"
	elif (humid >= 25) and (humid < 50):
		return "Moderate Humidity"
	else:
		return "Very Humid"


