

meatlist = ["salmon","pork","fish","chicken","beef","steak","ham","kobe","wagyu","lamb","brisket","goat","veal",
"duck","venison","meat","poultry","turkey","sausage"]

ingredients = []
food = open("ingredientstemp.txt","r")
for line in food:
	item = line.split(",")[0].split("(")[0].strip()
	if item not in ingredients:
		ingredients.append(item)


output = open("ingredientslist.txt",'w')
for item in ingredients:
	hasmeat= False
	for meat in meatlist:
		if (meat in item) or (meat.capitalize() in item):
			print(item)
			hasmeat = True
			break
	if not hasmeat:
		output.write(item+"\n")

output.close()