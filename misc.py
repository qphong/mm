
from math import *
from config import *


def deg2rad(x):
	
	return x * pi / 180.0
	

def rad2deg(x):
	
	return x * 180.0 / pi


def str2time(str):
	# input '04/08/201000:00:03'
	# output 00 * 3600 + 00 * 60 + 03
	
	s = str.split(':')
	
	hr = int(s[0][-2:])
	min = int(s[1])
	sec = int(s[2])
	
	return hr * 3600 + min * 60 + sec
	
	
def timeDiff(t1, t2):
	# input t = hr * 3600 + min * 60 + sec
	# output difference in seconds between t1 and t2
	
	if t1 <= t2:
		return t2 - t1
	return 24 * 3600 + t2 - t1
	

def normalizeLogVector(lvect):
	# modified lvect: nomalized log vector

	m = max(lvect)
	cvect = lvect[:]

	for i in range(len(lvect)):

		if m - lvect[i] > 300 or lvect[i] <= -INF:
			lvect[i] = -INF
		else:
			ttl = 0.0

			for j in range(len(cvect)):
				ttl += exp(cvect[j] - cvect[i])

			lvect[i] = log(1.0 / ttl)



