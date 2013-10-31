
from config import *
from readData import *
from graph import *
from log import *


class MapMatching:

	def __init__(self):

		print "Reading coordinates"
		self.coords = readCoord("data/coords.csv")

		print "Reading attributes"
		self.segments = readAtt("data/att.csv")

		self.G = Graph(self.coords, self.segments)

		self.gpsLocs = []
		self.logTProbs = [[[]]] * MAX_L # idx = to, from cand idx, to cand idx
		self.logEProbs = [[]] * MAX_L
		self.memoiz = [[]] * MAX_L
		self.vtrace = [[]] * MAX_L
		self.cPoints = [[]] * MAX_L
		self.cSegIds = [[]] * MAX_L
		self.mapSegIds = []
		self.maxDistance = [] 
		self.refLIdx = 0 # index 0 of global array corresponds to index self.refLIdx in local array


	def PREV(self, idx, maxIdx):

		if idx == 0:
			return maxIdx - 1
		return idx - 1


	def NEXT(self, idx, maxIdx):

		if idx == maxIdx - 1:
			return 0
		return idx + 1


	def getLIdxFrom(self, gIdx):
		# get local index from global index
		# ! should set the refLIdx before calling this function

		return (gIdx + self.refLIdx) % MAX_L


	def findCandidate(self, gIdx, maxDistance):
		# required: maxDistance = [INF] * len(cSegIds[PREV(lIdx,MAX_L)])

		lIdx = self.getLIdxFrom(gIdx)

		i = self.PREV(lIdx, MAX_L)
		
		if ( len(self.cPoints[i]) == 0 ):

			[segIds, pnts] = self.G.scanAll(self.gpsLocs[gIdx], REGION_DEG)
			
			self.cSegIds[lIdx] = list(segIds)
			self.cPoints[lIdx] = list(pnts)

		else:
			
			cSegs = set()
			pnts = []
			for j in range(len(self.cSegIds[i])):
				initLimit = self.gpsLocs[gIdx - 1].distTo(self.gpsLocs[gIdx]) * 3
				maxDistance[j] = self.G.findCandidate(self.cSegIds[i][j], self.gpsLocs[gIdx], \
					REGION_DEG, initLimit, initLimit / 2.0, cSegs, pnts)
			
			self.cPoints[lIdx] = list(pnts)
			self.cSegIds[lIdx] = list(cSegs)


	def calEProb(self, gIdx):
		# return emission probabilities

		probs = []
		lIdx = self.getLIdxFrom(gIdx)

		for i in range(len(self.cPoints[lIdx])):
			d = self.gpsLocs[gIdx].greatCircleDist( self.cPoints[lIdx][i] )
			probs.append( - d * d * 2 / (SIGMA_EMIS * SIGMA_EMIS) )

		normalizeLogVector(probs)
		
		logEmsProbs(probs, gIdx, self.cSegIds[lIdx], self.G.segments)

		return probs


	def isUturn(self, path):
		# input: path: sequence of segments
		# output: True if there exists a Uturn in path (only check the starting and ending node)

		l = len(path)
		return ( l > 1 and (  (self.G.segments[path[0]].start == self.G.segments[path[1]].end \
						 and self.G.segments[path[0]].end == self.G.segments[path[1]].start) \
		              or(self.G.segments[path[l-1]].start == self.G.segments[path[l-2]].end \
		              	 and self.G.segments[path[l-1]].end == self.G.segments[path[l-2]].start) ) )


	def calTProb(self, gIdx, maxDistance):

		lIdx = self.getLIdxFrom(gIdx)

		pre = self.PREV(lIdx, MAX_L)
		tprobs = [[]] * len(self.cSegIds[pre])

		for i in range(len(self.cSegIds[pre])):

			fromSI = self.cSegIds[pre][i]
			tprobs[i] = [0] * len(self.cSegIds[lIdx])
			for j in range(len(self.cSegIds[lIdx])):

				toSI = self.cSegIds[lIdx][j]
				straightDist = 	self.cPoints[pre][i].greatCircleDist(self.cPoints[lIdx][j])
				shortestDist = 0.0
				uturn = False

				if fromSI != toSI:

					shortest = self.G.shortestPath_Astar(self.G.segments[fromSI].end, \
						self.G.segments[toSI].start, maxDistance[i], toSI)

					shortestPath = shortest[1]
					shortestPath.insert(0, fromSI)
					shortestPath.append(toSI)

					uturn = self.isUturn(shortestPath)

					shortestDist = shortest[0]
					shortestDist += self.cPoints[pre][i].distTo( self.G.points[ self.G.segments[fromSI].end ] ) \
					                + self.cPoints[lIdx][j].distTo( self.G.points[ self.G.segments[toSI].start ] )
						
				else:
					shortestDist = self.cPoints[pre][i].distTo( self.cPoints[lIdx][j] )

				if shortestDist >= INF:
					tprobs[i][j] = -INF
				else:
					tprobs[i][j] = - (straightDist - shortestDist) * (straightDist - shortestDist) \
						/ (20 * SIGMA_TRANS * SIGMA_TRANS)

				if uturn:
					tprobs[i][j] -= log(10.0)

			normalizeLogVector(tprobs[i])

		logTransProbs(tprobs, gIdx, self.cSegIds[pre], self.cSegIds[lIdx], self.G.segments)

		return tprobs 


	def execute(self):

		print "Reading GPS points"
		self.gpsLocs = list(readGPS("data/taxi.txt"))

		for i in range(MAX_L):
			self.logTProbs[i] = [[]]
			self.logEProbs[i] = []
			self.memoiz[i] = []
			self.vtrace[i] = []
			self.cPoints[i] = []
			self.cSegIds[i] = []
		
		self.mapSegIds = []

		for i in range(len(self.gpsLocs)):
			self.mapGPSAt(i)

		self.visualize()


	def executeGreedy(self):

		print "Reading GPS points"
		self.gpsLocs = list(readGPS("data/taxi.txt"))

		for i in range(MAX_L):
			self.logTProbs[i] = [[]]
			self.logEProbs[i] = []
			self.memoiz[i] = []
			self.vtrace[i] = []
			self.cPoints[i] = []
			self.cSegIds[i] = []
		
		self.mapSegIds = []

		for i in range(len(self.gpsLocs)):
			self.mapGPSGreedyAt(i)

		self.visualize()


	def entropyOfLogProbs(self, vect):

		ttl = 0
		for v in vect:
			ttl += ( -v * exp(v) )
		return ttl


	def mapGPSGreedyAt(self, gIdx):

		lIdx = self.getLIdxFrom(gIdx)

		print gIdx
		print "   Clearing"
		self.logTProbs[lIdx] = [[]]
		self.logEProbs[lIdx] = []
		self.memoiz[lIdx] = []
		self.vtrace[lIdx] = []
		self.cPoints[lIdx] = []
		self.cSegIds[lIdx] = []

		print "   Find candidates"
		self.maxDistance = [INF] * len(self.cSegIds[self.PREV(lIdx,MAX_L)])
		self.findCandidate(gIdx, self.maxDistance)

		if len(self.cSegIds[lIdx]) == 0:
			self.mapSegIds.append(-1) # cannot find any candidate segments
			return

		print "   Calculate emission probabilities"
		self.logEProbs[lIdx] = self.calEProb(gIdx)

		e = self.entropyOfLogProbs(self.logEProbs[lIdx])
		if e > 1.5:
		
			maxValue = max(self.logEProbs[lIdx])
			maxIdx = 0
			for i in range(len(self.logEProbs[lIdx])):
				if self.logEProbs[lIdx][i] == maxValue:
					maxIdx = i

			self.mapSegIds.append(self.cSegIds[lIdx][i])

		else:

			self.mapSegIds.append(0)
			

	def mapGPSAt(self, gIdx):

		lIdx = self.getLIdxFrom(gIdx)

		print gIdx
		print "   Clearing"
		self.logTProbs[lIdx] = [[]]
		self.logEProbs[lIdx] = []
		self.memoiz[lIdx] = []
		self.vtrace[lIdx] = []
		self.cPoints[lIdx] = []
		self.cSegIds[lIdx] = []

		print "   Find candidates"
		self.maxDistance = [INF] * len(self.cSegIds[self.PREV(lIdx,MAX_L)])
		self.findCandidate(gIdx, self.maxDistance)

		if len(self.cSegIds[lIdx]) == 0:
			self.mapSegIds.append(-1) # cannot find any candidate segments
			return


		print "   Calculate emission probabilities"
		self.logEProbs[lIdx] = self.calEProb(gIdx)


		curMax = 0 # how many past matchings
		i = self.PREV(lIdx, MAX_L)
		while len(self.cPoints[i]) != 0 and curMax < MAX_L - 1:
			i = self.PREV(i, MAX_L)
			curMax += 1


		print "   Calculate transition probabilities"
		if curMax == 0: # no past matching
			maxIdx = 0

			for i in range(len(self.logEProbs[lIdx])):
		
				if self.logEProbs[lIdx][i] > self.logEProbs[lIdx][maxIdx]:
					maxIdx = i
				self.memoiz[lIdx].append(self.logEProbs[lIdx][i])

			self.mapSegIds.append(self.cSegIds[lIdx][maxIdx])
			return

		else:

			self.logTProbs[lIdx] = self.calTProb(gIdx, self.maxDistance)


		self.memoiz[lIdx] = [0.0] * len(self.cPoints[lIdx])
		self.vtrace[lIdx] = [0] * len(self.cPoints[lIdx])
		pre = self.PREV(lIdx, MAX_L)

		for j in range(len(self.cSegIds[lIdx])):
			maxIdx = 0
			maxValue = self.memoiz[pre][maxIdx] + self.logTProbs[lIdx][maxIdx][j]
			for i in range(len(self.cSegIds[pre])):
				tmp = self.memoiz[pre][i] + self.logTProbs[lIdx][i][j]
				if tmp > maxValue:
					maxValue = tmp
					maxIdx = i

			self.memoiz[lIdx][j] = maxValue + self.logEProbs[lIdx][j]
			self.vtrace[lIdx][j] = maxIdx
		

		print "   Mapmatch and Update results"
		maxIdx = 0
		for i in range(len(self.memoiz[lIdx])):
			if self.memoiz[lIdx][i] > self.memoiz[lIdx][maxIdx]:
				maxIdx = i
		self.mapSegIds.append(self.cSegIds[lIdx][maxIdx])

		tmp = lIdx
		for i in range(curMax):
			maxIdx = self.vtrace[tmp][maxIdx]
			tmp = self.PREV(tmp, MAX_L)
			idx = len(self.mapSegIds) - i - 2

			if self.mapSegIds[idx] != self.cSegIds[tmp][maxIdx]:
				self.mapSegIds[idx] = self.cSegIds[tmp][maxIdx]

		return


	def visualize(self):

		infos = range(len(self.gpsLocs))
		for i in range(len(infos)):
			infos[i] = str(infos[i])

		segs = []
		for sid in self.mapSegIds:
			segs.append(self.G.segments[sid])

		logPoints(self.gpsLocs, infos)
		logSegments(segs, self.G.points, infos)









