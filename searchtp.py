import urllib2
import argparse
from datetime import datetime

mainurl = "http://126.177.15.150/reflexes/common/"
archiveurl = "http://126.177.15.150/reflexes/common/archive/"
currenturl = ""
hour = 0


def start():
	today = datetime.today()
	parser = argparse.ArgumentParser(description='Short sample app')
	parser.add_argument('-hr', action="store", dest="hour", type=int, default=0)
	parser.add_argument('-d', action="store", dest="day", type=int, default=today.day)
	parser.add_argument('-m', action="store", dest="month", type=int, default=today.month)
	parser.add_argument('-y', action="store", dest="year", type=int, default=today.year)
	parser.add_argument('-w', action="store", dest="word", type=str, default="")
	options = parser.parse_args()
	print options
	if options.day != today.day or options.month != today.month or options.year != today.year:
		currenturl = archiveurl + "%d/"%options.year + str(options.month).zfill(2) + "/" + str(options.day).zfill(2) + "/"
	else:
		currenturl = mainurl
	print currenturl
	#start the programm
	main(currenturl, options.word, options.hour)
	


def main(url, word, hour):
	u = urllib2.urlopen(url)
	localFile = open('index', 'w')
	localFile.write(u.read())
	localFile.close()

	f = open('index', 'r')

	for line in f:
		index = line.find("weblogic")
		if index > -1:
			if hour > 0:
				index2 = line.find(str(hour).zfill(2) + ":")
				if(index2 > -1):
					temp = line[index:]
					index3 = temp.find("\"")
					fileName = temp[:index3]
					parseFile(url, fileName, word)
			else:
				temp = line[index:]
				index3 = temp.find("\"")
				fileName = temp[:index3]
				parseFile(url, fileName, word)
	f.close()			

def parseFile(url, filename, searchword):
	print "looking up word: " + searchword + " in: " + filename
	url2 = url + filename
	ur = urllib2.urlopen(url2)
	local = open('log', 'w')
	local.write(ur.read())
	local.close()
	fl = open('log', 'r')
	for lin in fl:
		if lin.find(searchword) > -1:
			print('\a')
			print "found in " + filename
			break
	fl.close()

start()
