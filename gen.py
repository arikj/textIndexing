from random import randint

numSet = 2
nData = 100

if numSet == 1:
	numDocs = 799
if numSet == 2:
	numDocs = 1391

totalWords = []
contentDocs = []

for k in range(0,numDocs):
	print k

	w = []
	x = []
	words = []

	filename = "./documents/set" + str(numSet) + "/doc" + str(k) + ".txt"
	f = open(filename,"r")
	content = f.read()
	f.close

	w = content.split(' ')
	for i in range(0,len(w)):
		x = w[i].split('\n')
		for j in range(0,len(x)):
			words.append(x[j])

	for i in range(0,len(words)):
		contentDocs.append(words[i])
		if words[i] not in totalWords:
			totalWords.append(words[i])

queries = []
for k in range(1,4):
	for i in range(0,nData):
		
		query = str(k) + "\t"

		if k == 1:
			for j in range(0,randint(1,8)):
				query += totalWords[randint(0,len(totalWords)-1)] + " "

		elif k == 2:
			l = len(contentDocs)
			r = randint(0,l)

			for i in range(r,r+randint(5,15)):
				if i > l:
					break
				query += contentDocs[i] + " "

		else:
			for j in range(0,randint(1,8)):
				query += totalWords[randint(0,len(totalWords)-1)] + " "
			query += "\t" + str(randint(1,25))

		queries.append(query + "\n")

# print contentDocs
f = open("querydata_set"+str(numSet)+".txt","w")
for k in range(0,len(queries)):
	f.write(queries[k])
f.close()