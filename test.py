

def mdf(vect):
		
	vect = [1, 2, 3]

a = 5
def mdfa(b):
	
	global a
	a = b


gpsLocs = []

def execute():

	global gpsLocs
	print "Reading GPS points"
	gpsLocs = list(readGPS("data/taxi.txt"))


def m1(b):
	global gpsLocs
	gpsLocs = list(b)
	print gpsLocs

def m2(b):
	global gpsLocs
	gpsLocs = b[:]
	print gpsLocs

def m3(b):
	global gpsLocs

	for i in b:
		gpsLocs.append(b)
	print gpsLocs

import os
os.chdir("C:/Users/Admin Guest/Dropbox/ThinkPad/")
