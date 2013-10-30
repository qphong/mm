

from math import *
import UTM

PATH_GPS = "data/taxi.txt"
PATH_COORD = "data/coords.csv"
PATH_ATT = "data/att.csv"
PATH_PNTS = "drawToTest/logPoints.js"
PATH_SEGS = "drawToTest/logSegs.js"
PATH_SEGS_INFO = "drawToTest/logIds.js"
PATH_LOGS = "logs/"

INF = 1e9
EPS = 1e-9
R = 6371000

MAX_L = 5

# REGION_DEG = 0.0007587
# REGION = 20
REGION_DEG = 70 # meters, this is not degree anymore! after UTM conversion
SIGMA_EMIS = 20
SIGMA_TRANS = 20

MAX_DIST = 1875.0



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
		if lvect[i] - m < -300 or lvect[i] - m > 300 or lvect[i] <= -INF:
			lvect[i] = -INF
		else:
			ttl = 0.0

			for j in range(len(cvect)):
				ttl += exp(cvect[j] - cvect[i])

			lvect[i] = log(1.0 / ttl)



class Point:

	def __init__(self, lat=0.0, lng=0.0, tm=-1):
		# latitude, longitude, timestamp
		
		self.orgCoord = [float(lat), float(lng)]
		self.coord = UTM.LLtoUTM(23, lng, lat, zone = None)[1:] # convert to UTM coordinates
		self.tm = float(tm)
		
		
	def distTo(self, p):
		# straight distance from self to point p
		return sqrt( sum((a - b)**2 for (a,b) in zip(self.coord, p.coord)) )

		
	def isSame(self, p):
		# if self and p are of same coordinate
		
		if abs(self.coord[0] - p.coord[0]) < EPS \
			and abs(self.coord[1] - p.coord[1]) < EPS:
			return True

		return False
		
		
	def greatCircleDist(self, p):
		# return the great circle distance from point self to p
		
		# if self.distTo(p) < EPS:
		# 	return 0.0
		
		# innerAngle = acos( sin(deg2rad(self.coord[0])) * sin(deg2rad(p.coord[0])) \
		#                       + cos(deg2rad(self.coord[0])) * cos(deg2rad(p.coord[0])) \
		# 					    * cos(deg2rad(self.coord[1] - p.coord[1])) );

		# return R * innerAngle
		
		return self.distTo(p)

	
	def dist2Line(self, a, b):
		# return [distance from point self to line ab,
		#        projected point self onto ab]
		
		scale = ( (self.coord[0] - a.coord[0]) * (b.coord[0] - a.coord[0]) \
		         +(self.coord[1] - a.coord[1]) * (b.coord[1] - a.coord[1]) ) / \
				( (b.coord[0] - a.coord[0]) * (b.coord[0] - a.coord[0]) \
				 +(b.coord[1] - a.coord[1]) * (b.coord[1] - a.coord[1]) ) 
		
		c = Point()
		c.coord = [ a.coord[0] + scale * (b.coord[0] - a.coord[0]), \
				    a.coord[1] + scale * (b.coord[1] - a.coord[1]) ]
		
		return [self.distTo(c), c]
		
	
	def dist2LineSeg(self, a, b):
		# return [distance from point self to line segment ab,
		#        projected point self onto line segment ab]
		
		c = Point()

		if (b.coord[0] - a.coord[0]) * (self.coord[0] - a.coord[0]) \
		  +(b.coord[1] - a.coord[1]) * (self.coord[1] - a.coord[1]) < EPS:
			c.coord = a.coord[:]
			return (self.distTo(a), c)
		
		if (a.coord[0] - b.coord[0]) * (self.coord[0] - b.coord[0]) \
		  +(a.coord[1] - b.coord[1]) * (self.coord[1] - b.coord[1]) < EPS:
			c.coord = b.coord[:]
			return [self.distTo(b), c]
		
		return self.dist2Line(a,b)
		
	
	
	
class Segment:

	def __init__(self, id, start, end, length, speedlm=200, alias="", name=""):
		# id, start node id, end node id, length
		# speed limit, alias id, name
		
		self.id = id
		self.start = start
		self.end = end
		self.length = length
		self.speedlm = speedlm
		self.alias = alias
		self.name = name
		
	
	
	