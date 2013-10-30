
from config import *
from readData import *
from graph import *
from log import *



print "Reading coordinates"
coords = readCoord("data/coords.csv")

print "Reading attributes"
segments = readAtt("data/att.csv")

G = Graph(coords, segments)

gpsLocs = []
logTProbs = [[[]]] * MAX_L # idx = to, from cand idx, to cand idx
logEProbs = [[]] * MAX_L
memoiz = [[]] * MAX_L
vtrace = [[]] * MAX_L
cPoints = [[]] * MAX_L
cSegIds = [[]] * MAX_L
mapSegIds = []
maxDistance = [] 
refLIdx = 0


def PREV(idx, maxIdx):

	if idx == 0:
		return maxIdx - 1
	return idx - 1


def NEXT(idx, maxIdx):

	if idx == maxIdx - 1:
		return 0
	return idx + 1


# def initRefLIdx(lidx):
# 	# lidx is value for local index corresponding to global index of value 0
# 	# ! should be called only once

# 	global refLIdx
# 	refLIdx = lidx
# !!! alway set refLIdx = 0


def getLIdxFrom(gIdx):
	# get local index from global index
	# ! should set the refLIdx before calling this function

	return (gIdx + refLIdx) % MAX_L


def findCandidate(gIdx, maxDistance):
	# required: maxDistance = [INF] * len(cSegIds[PREV(lIdx,MAX_L)])

	global G
	global gpsLocs
	global cSegIds
	global cPoints

	lIdx = getLIdxFrom(gIdx)

	i = PREV(lIdx, MAX_L)
	
	if ( len(cPoints[i]) == 0 ):

		[segIds, pnts] = G.scanAll(gpsLocs[gIdx], REGION_DEG)
		
		cSegIds[lIdx] = list(segIds)
		cPoints[lIdx] = list(pnts)

	else:
		
		cSegs = set()
		pnts = []
		for j in range(len(cSegIds[i])):
			initLimit = gpsLocs[gIdx - 1].distTo(gpsLocs[gIdx]) * 3
			maxDistance[j] = G.findCandidate(cSegIds[i][j], gpsLocs[gIdx], REGION_DEG, initLimit, initLimit / 2.0, cSegs, pnts)
		
		cPoints[lIdx] = list(pnts)
		cSegIds[lIdx] = list(cSegs)


def calEProb(gIdx):
	# return emission probabilities

	global gpsLocs
	global cPoints

	probs = []
	lIdx = getLIdxFrom(gIdx)

	for i in range(len(cPoints[lIdx])):
		d = gpsLocs[gIdx].greatCircleDist( cPoints[lIdx][i] )
		probs.append( - d * d * 2 / (SIGMA_EMIS * SIGMA_EMIS) )

	normalizeLogVector(probs)
	
	logEmsProbs(probs, gIdx, cSegIds[lIdx], G.segments)

	return probs


def isUturn(path):
	# input: path: sequence of segments
	# output: True if there exists a Uturn in path (only check the starting and ending node)

	l = len(path)
	return ( l > 1 and (  (G.segments[path[0]].start == G.segments[path[1]].end \
					 and G.segments[path[0]].end == G.segments[path[1]].start) \
	              or(G.segments[path[l-1]].start == G.segments[path[l-2]].end \
	              	 and G.segments[path[l-1]].end == G.segments[path[l-2]].start) ) )


# def isUturn2(path):

# 	l = len(path)
# 	return ( l > 1 and ( (path[0].start == path[1].end \
# 		                  and path[0].end == path[1].start) \
# 	                   or(path[l-1].start == path[l-2].end \
# 	                   	  and path[l-1].end == path[l-2].start) ) )



def calTProb(gIdx, maxDistance):

	global cSegIds
	global cPoints
	global G

	lIdx = getLIdxFrom(gIdx)

	pre = PREV(lIdx, MAX_L)
	tprobs = [[]] * len(cSegIds[pre])

	for i in range(len(cSegIds[pre])):

		fromSI = cSegIds[pre][i]
		tprobs[i] = [0] * len(cSegIds[lIdx])
		for j in range(len(cSegIds[lIdx])):

			toSI = cSegIds[lIdx][j]
			straightDist = 	cPoints[pre][i].greatCircleDist(cPoints[lIdx][j])
			shortestDist = 0.0
			uturn = False

			if fromSI != toSI:

				shortest = G.shortestPath_Astar(G.segments[fromSI].end, G.segments[toSI].start, maxDistance[i], toSI)

				shortestPath = shortest[1]
				shortestPath.insert(0, fromSI)
				shortestPath.append(toSI)

				uturn = isUturn(shortestPath)

				shortestDist = shortest[0]
				shortestDist += cPoints[pre][i].distTo( G.points[ G.segments[fromSI].end ] ) \
				                + cPoints[lIdx][j].distTo( G.points[ G.segments[toSI].start ] )
					
			else:
				shortestDist = cPoints[pre][i].distTo( cPoints[lIdx][j] )

			if shortestDist >= INF:
				tprobs[i][j] = -INF
			else:
				tprobs[i][j] = - (straightDist - shortestDist) * (straightDist - shortestDist) / (20 * SIGMA_TRANS * SIGMA_TRANS)

			if uturn:
				tprobs[i][j] -= log(10.0)

		normalizeLogVector(tprobs[i])

	logTransProbs(tprobs, gIdx, cSegIds[pre], cSegIds[lIdx], G.segments)

	return tprobs 


def execute():

	global gpsLocs
	global mapSegIds
	global logTProbs
	global logEProbs
	global memoiz
	global vtrace
	global cPoints
	global cSegIds

	print "Reading GPS points"
	gpsLocs = list(readGPS("data/taxi.txt"))

	for i in range(MAX_L):
		logTProbs[i] = [[]]
		logEProbs[i] = []
		memoiz[i] = []
		vtrace[i] = []
		cPoints[i] = []
		cSegIds[i] = []
	
	mapSegIds = []

	for i in range(len(gpsLocs)):
		mapGPSAt(i)

	visualize()


def executeGreedy():

	global gpsLocs
	global mapSegIds
	global logTProbs
	global logEProbs
	global memoiz
	global vtrace
	global cPoints
	global cSegIds

	print "Reading GPS points"
	gpsLocs = list(readGPS("data/taxi.txt"))

	for i in range(MAX_L):
		logTProbs[i] = [[]]
		logEProbs[i] = []
		memoiz[i] = []
		vtrace[i] = []
		cPoints[i] = []
		cSegIds[i] = []
	
	mapSegIds = []

	for i in range(len(gpsLocs)):
		mapGPSGreedyAt(i)

	visualize()


def entropyOfLogProbs(vect):

	ttl = 0
	for v in vect:
		ttl += ( -v * exp(v) )
	return ttl


def mapGPSGreedyAt(gIdx):

	global G
	global gpsLocs
	global logTProbs
	global logEProbs
	global memoiz
	global vtrace
	global cPoints
	global cSegIds
	global mapSegIds
	global maxDistance

	lIdx = getLIdxFrom(gIdx)

	print gIdx
	print "   Clearing"
	logTProbs[lIdx] = [[]]
	logEProbs[lIdx] = []
	memoiz[lIdx] = []
	vtrace[lIdx] = []
	cPoints[lIdx] = []
	cSegIds[lIdx] = []

	print "   Find candidates"
	maxDistance = [INF] * len(cSegIds[PREV(lIdx,MAX_L)])
	findCandidate(gIdx, maxDistance)

	if len(cSegIds[lIdx]) == 0:
		mapSegIds.append(-1) # cannot find any candidate segments
		return

	print "   Calculate emission probabilities"
	logEProbs[lIdx] = calEProb(gIdx)

	e = entropyOfLogProbs(logEProbs[lIdx])
	if e > 1.5:
	
		maxValue = max(logEProbs[lIdx])
		maxIdx = 0
		for i in range(len(logEProbs[lIdx])):
			if logEProbs[lIdx][i] == maxValue:
				maxIdx = i

		mapSegIds.append(cSegIds[lIdx][i])

	else:

		mapSegIds.append(0)
		

def mapGPSAt(gIdx):

	global G
	global gpsLocs
	global logTProbs
	global logEProbs
	global memoiz
	global vtrace
	global cPoints
	global cSegIds
	global mapSegIds
	global maxDistance

	lIdx = getLIdxFrom(gIdx)

	print gIdx
	print "   Clearing"
	logTProbs[lIdx] = [[]]
	logEProbs[lIdx] = []
	memoiz[lIdx] = []
	vtrace[lIdx] = []
	cPoints[lIdx] = []
	cSegIds[lIdx] = []

	print "   Find candidates"
	maxDistance = [INF] * len(cSegIds[PREV(lIdx,MAX_L)])
	findCandidate(gIdx, maxDistance)

	if len(cSegIds[lIdx]) == 0:
		mapSegIds.append(-1) # cannot find any candidate segments
		return


	print "   Calculate emission probabilities"
	logEProbs[lIdx] = calEProb(gIdx)


	curMax = 0 # how many past matchings
	i = PREV(lIdx, MAX_L)
	while len(cPoints[i]) != 0 and curMax < MAX_L - 1:
		i = PREV(i, MAX_L)
		curMax += 1


	print "   Calculate transition probabilities"
	if curMax == 0: # no past matching
		maxIdx = 0

		for i in range(len(logEProbs[lIdx])):
	
			if logEProbs[lIdx][i] > logEProbs[lIdx][maxIdx]:
				maxIdx = i
			memoiz[lIdx].append(logEProbs[lIdx][i])

		mapSegIds.append(cSegIds[lIdx][maxIdx])
		return

	else:

		logTProbs[lIdx] = calTProb(gIdx, maxDistance)


	memoiz[lIdx] = [0.0] * len(cPoints[lIdx])
	vtrace[lIdx] = [0] * len(cPoints[lIdx])
	pre = PREV(lIdx, MAX_L)

	for j in range(len(cSegIds[lIdx])):
		maxIdx = 0
		maxValue = memoiz[pre][maxIdx] + logTProbs[lIdx][maxIdx][j]
		for i in range(len(cSegIds[pre])):
			tmp = memoiz[pre][i] + logTProbs[lIdx][i][j]
			if tmp > maxValue:
				maxValue = tmp
				maxIdx = i

		memoiz[lIdx][j] = maxValue + logEProbs[lIdx][j]
		vtrace[lIdx][j] = maxIdx
	

	print "   Mapmatch and Update results"
	maxIdx = 0
	for i in range(len(memoiz[lIdx])):
		if memoiz[lIdx][i] > memoiz[lIdx][maxIdx]:
			maxIdx = i
	mapSegIds.append(cSegIds[lIdx][maxIdx])

	tmp = lIdx
	for i in range(curMax):
		maxIdx = vtrace[tmp][maxIdx]
		tmp = PREV(tmp, MAX_L)
		idx = len(mapSegIds) - i - 2
		if mapSegIds[idx] != cSegIds[tmp][maxIdx]:
			mapSegIds[idx] = cSegIds[tmp][maxIdx]

	return


def visualize():

	global mapSegIds
	global G
	global gpsLocs

	infos = range(len(gpsLocs))
	for i in range(len(infos)):
		infos[i] = str(infos[i])

	segs = []
	for sid in mapSegIds:
		segs.append(G.segments[sid])

	logPoints(gpsLocs, infos)
	logSegments(segs, G.points, infos)









