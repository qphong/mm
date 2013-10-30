
import csv
from config import *


def readCoord(fname):
	
	points = []
	
	with open(fname) as csvfile:
	
		reader = csv.reader(csvfile)
		reader.next()
		[order_id, global_id, lat, lng] = [0, 1, 2, 3]
		for row in reader:
			points.append( Point(float(row[lat]), float(row[lng])) )
	
	return points
	

def readAtt(fname):

	segments = []
	
	with open(fname) as csvfile:
	
		reader = csv.reader(csvfile)
		lable = reader.next()
		
		[shapeid, no, fromNodeNo, toNodeNo, name, length, numLanes, \
			rNo,  rFromNo, rToNodeNo, rLength, rNumLanes] = \
			[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
		count = 0
		
		for r in reader:
		
			if int(r[numLanes]) > 0:
				segments.append( Segment(count, int(r[fromNodeNo]), int(r[toNodeNo]), float(r[length]), 200.0, r[no], r[name]) )
				count += 1
				
			if int(r[rNumLanes]) > 0:
				segments.append( Segment(count, int(r[rFromNo]), int(r[rToNodeNo]), float(r[rLength]), 200.0, r[rNo], r[name]) )
				count += 1
		
	return segments

	

def readGPS(fname):
	
	gpsLocs = []
	
	with open(fname) as csvfile:
		
		reader = csv.reader(csvfile)
		
		[time, plate, driver, lng, lat, speed, mode] = \
			[0, 1, 2, 3, 4, 5, 6]
		
		for r in reader:
			gpsLocs.append( Point(float(r[lat]), float(r[lng]), \
				str2time(r[time])) )
		
	return gpsLocs





