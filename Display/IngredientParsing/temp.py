

f = open("foodfile.txt","r")
text = ""
for line in f:
	text += line

text = text.split(",")
output = open("output.txt","w")
for term in text:
	try:
		float(term)
	except:
		if term == "":
			continue
		output.write(term.strip("\n").strip(" ")+"\n")

output.close()


