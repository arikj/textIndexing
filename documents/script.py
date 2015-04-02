f= open("doc.txt","r")

content = f.read()

contentList = content.split("\n\n")
index = 0
for k in range(0, len(contentList)):
	content = contentList[k]
	if len(content) == 0:
		continue
	newF = open("./set2/doc"+str(index)+".txt","w")
	newF.write(content)
	newF.close()
	index += 1