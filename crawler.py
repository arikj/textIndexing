from bs4 import BeautifulSoup
import urllib2

proxy = urllib2.ProxyHandler({'https': 'http://himagar:Agravan@relproxy.iitk.ac.in:3128', 'http': 'http://himagar:Agravan@relproxy.iitk.ac.in:3128'})
auth = urllib2.HTTPBasicAuthHandler()
opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler,urllib2.HTTPSHandler,urllib2.HTTPRedirectHandler)
urllib2.install_opener(opener)

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


def openurl(site):

	req = urllib2.Request(site, headers=hdr)
	webpage = ""

	try:
		webpage = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print e.fp.read()
	except urllib2.URLError, e2:
		print "There was an error:", e2	

	prova = webpage.read()
	soup = BeautifulSoup(prova, 'html.parser')

	return soup

filePath = "./documents/set1/"

site = "http://www.fullbooks.com/"
soup = openurl(site)

tags = soup.find_all('li')

num = 0

for tag in tags:
	link = tag.find("a")
	newSite = site + link["href"]
	newSoup = openurl(newSite)

	newTags = newSoup.find_all('li')

	for newTag in newTags:
		link2 = newTag.find("a")
		newSite2 = site + link2["href"]
		newSoup2 = openurl(newSite2)

		newTag2 = newSoup2.find_all('li')

		for t in newTag2:
			link3 = t.find("a")
			newSite3 = site + link3["href"]
			newSoup3 = openurl(newSite3)

			print newSite3
			
			x = newSoup3.find_all("font",{'face':'Arial'})
			content = ""
			for y in x:
				content += y.text.encode('utf-8')

			filename = filePath + "doc" + str(num) + ".txt"

			text_file = open(filename, "w")
			text_file.write(content)
			text_file.close()

			num += 1

print "Total documents: " + str(num)


'''
tags = soup.find_all("p","header fbld")

for tag in tags:
	link = tag.find("a")
	url = link["href"]
	title = link["title"]
	story = openurl(url)
	page = BeautifulSoup(story)
	print title
	print page.find("div","firstpublising").text
	print page.find(id="ins_storybody").text.encode('utf-8')
	print "\n"
'''