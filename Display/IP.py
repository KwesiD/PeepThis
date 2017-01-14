import requests

#Gets IP address and location data
def getLocation():
	ip = postal = 0
	city = state = country = "Unknown"
	request = None
	status_code = 0
	status = None #leave as none here.  #0 = good to go, 1 = Connection Error, 2 = Timeout Error, 3 = Exceeded Rate Limit -1 = RIP Idk wtf happened
	#catch when no wifi
	try:
		request = requests.get('http://ipinfo.io/') #gets current ip and location
	except requests.ConnectionError: ##in the event of lack of connection
		status = "Connection Error in IP API"
		return ip,(city,state,country,postal),status
	except requests.Timeout: #poor connection
		status = "IP API Timed out"
		return ip,(city,state,country,postal),status
	except: #unknown issue
		status = "Unknown Issue with IP API"
		return ip,(city,state,country,postal),status

	status_code = request.status_code #200 is good. it went through. 429 means rate limit exceeded
	if status_code != 200: #If it didnt complete properly, then it will let us know what the code was 
		status = "IP API Returned Status Code" + str(status_code)
		return ip,(city,state,country,postal),status

	#if all goes right
	data = request.json()
	ip = data["ip"]
	postal = data["postal"]
	city = data["city"]
	state = data["region"]
	country = data["country"]

	return ip,(city,state,country,postal),status

# ip,location,status = getLocation()
# if status != None:
# 	##Send error message, do whatever, Idk
# 	print(status)
