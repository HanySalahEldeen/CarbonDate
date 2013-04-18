from getTopsy import getTopsyCreationDate
from getBitly import getBitlyCreationDate
from getArchives import getArchivesCreationDate
from getGoogle import getGoogleCreationDate
from getBacklinks import *
from getLowest import getLowest
from getLastModified import getLastModifiedDate
import time
import math
import calendar
import json
from ordereddict import OrderedDict

fileOut = open("results5.txt", "w")
fileOutAll = open("resultsJSON5.txt", "w")

#URL,RealDate,BitlyDate,TimeForBitly,DeltaBitly,ArchivesDate,TimeForArchives,DeltaArchives,TopsyDate,TimeForTopsy,DeltaTopsy,GoogleDate,TimeForGoogle,DeltaGoogle,LastModifiedDate,TimeForLastModified,DeltaLastModified,BacklinksDate,TimeForBacklinks,DeltaBacklinks,LowestDate,DeltaClosest,ClosestSource

wins = {"Bitly":0, "Archives":0, "Topsy":0, "Google":0, "LastModified":0, "Backlinks":0}
averagesDelta = {"Bitly":0, "Archives":0, "Topsy":0, "Google":0, "LastModified":0, "Backlinks":0}
averageTimes = {"Bitly":0, "Archives":0, "Topsy":0, "Google":0, "LastModified":0, "Backlinks":0}

allstart = time.time()
count = 0
for line in open("finalList.txt","r"):
	count = count + 1
	print count
	if(count<1191):
		continue
	line = line.replace("\n","")
	parts = line.split(",")
	url = parts[0]
	date= parts[1]
	loc = url.find("#")
	if(loc!=-1):
		url = url[:loc]
	to_print = url+","+date
	epochReal = int(calendar.timegm(time.strptime(date, '%Y-%m-%d')))
        closest = epochReal
	which = ""
	#----------------------------------Bitly--------------------------
	start = time.time()
	now = "Bitly"
	timestamp = getBitlyCreationDate(url)
	bitly = timestamp
	end = time.time()
	runTime = end - start
	delta = ""
	if(timestamp!=""):
		epoch = int(calendar.timegm(time.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')))
		delta = epoch-epochReal	
		delta2 = int(math.fabs(delta))
		if(delta2<closest):
			closest = delta2
			which = now
		averagesDelta[now]=averagesDelta[now]+int(delta)

	averageTimes[now]=averageTimes[now]+runTime
	to_print = to_print + "," + timestamp + "," + str(runTime) + "," + str(delta)
	print now
	#----------------------------------Archives--------------------------
	start = time.time()
	now = "Archives"
	allarchives = getArchivesCreationDate(url)
	timestamp = allarchives["Earliest"]
	archives = timestamp
	end = time.time()
	runTime = end - start
	delta = ""
	if(timestamp!=""):
		epoch = int(calendar.timegm(time.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')))
		delta = epoch-epochReal	
		delta2 = int(math.fabs(delta))
		if(delta2<closest):
			closest = delta2
			which = now
		averagesDelta[now]=averagesDelta[now]+int(delta)

	averageTimes[now]=averageTimes[now]+runTime
	to_print = to_print + "," + timestamp + "," + str(runTime) + "," + str(delta)
	print now

	#----------------------------------Topsy--------------------------
	start = time.time()
	now = "Topsy"
	timestamp = getTopsyCreationDate(url)
	topsy = timestamp
	end = time.time()
	runTime = end - start
	delta = ""
	if(timestamp!=""):
		epoch = int(calendar.timegm(time.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')))
		delta = epoch-epochReal	
		delta2 = int(math.fabs(delta))
		if(delta2<closest):
			closest = delta2
			which = now
		averagesDelta[now]=averagesDelta[now]+int(delta)

	averageTimes[now]=averageTimes[now]+runTime
	to_print = to_print + "," + timestamp + "," + str(runTime) + "," + str(delta)
	print now

	#----------------------------------Google--------------------------
	start = time.time()
	now = "Google"
	timestamp = getGoogleCreationDate(url)
	google = timestamp
	end = time.time()
	runTime = end - start
	delta = ""
	if(timestamp!=""):
		epoch = int(calendar.timegm(time.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')))
		delta = epoch-epochReal	
		delta2 = int(math.fabs(delta))
		if(delta2<closest):
			closest = delta2
			which = now
		averagesDelta[now]=averagesDelta[now]+int(delta)

	averageTimes[now]=averageTimes[now]+runTime
	to_print = to_print + "," + timestamp + "," + str(runTime) + "," + str(delta)
	print now

	#----------------------------------Last Modified--------------------------
	start = time.time()
	now = "LastModified"
	timestamp = getLastModifiedDate(url)
	lastmod = timestamp
	end = time.time()
	runTime = end - start
	delta = ""
	if(timestamp!=""):
		epoch = int(calendar.timegm(time.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')))
		delta = epoch-epochReal	
		delta2 = int(math.fabs(delta))
		if(delta2<closest):
			closest = delta2
			which = now
		averagesDelta[now]=averagesDelta[now]+int(delta)

	averageTimes[now]=averageTimes[now]+runTime
	to_print = to_print + "," + timestamp + "," + str(runTime) + "," + str(delta)
	print now

	#----------------------------------Backlinks--------------------------
	if(count< 1190):
		start = time.time()
		now = "Backlinks"
		timestamp = getBacklinksFirstAppearanceDates(url)
		backlinks = timestamp
		end = time.time()
		runTime = end - start
		delta = ""
		if(timestamp!=""):
			epoch = int(calendar.timegm(time.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')))
			delta = epoch-epochReal	
			delta2 = int(math.fabs(delta))
			if(delta2<closest):
				closest = delta2
				which = now
			averagesDelta[now]=averagesDelta[now]+int(delta)

		averageTimes[now]=averageTimes[now]+runTime
		to_print = to_print + "," + timestamp + "," + str(runTime) + "," + str(delta)
		print now
	else:
		backlinks= ""
	#------------------------------------------------------------------

	lowest = getLowest([bitly,topsy,google,archives,lastmod,backlinks])
	if(which != ""):
		wins[which] = wins[which]+1
	to_print = to_print + "," + lowest + "," + str(closest) + "," + which

	fileOut.write(to_print+"\n")
	fileOut.flush()

	#------------------------------Save all results---------------------------
	result = []
	result.append(("URI", url))
	result.append(("Estimated Creation Date", lowest))
	result.append(("Last Modified", lastmod))
	result.append(("Bitly.com", bitly))
	result.append(("Topsy.com", topsy))
	result.append(("Backlinks", backlinks))
	result.append(("Google.com", google))
	result.append(("Archives", allarchives))
	values = OrderedDict(result)
	r = json.dumps(values, sort_keys=False, indent=4, separators=(',', ': '))

	fileOutAll.write(r+"\n\n #-----------------------------------------# \n\n")
	fileOutAll.flush()


#--------Statistics--------
for source in averagesDelta:
	print "Average time delta from real for "+source+": "+ str(int((averagesDelta[source]*1.0)/(count*1.0)))
for source in averageTimes:
	print "Average run time for "+source+": "+ str(int((averageTimes[source]*1.0)/(count*1.0)))
for source in wins:
	print "Number of win times for "+source+": "+ str(wins[source])


allend = time.time()
print "Total runtime =" + str(allend - allstart)

fileOutAll.close()
fileOut.close()
