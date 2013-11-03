
"""
This file contains definition of class Graph
"""

from config import *
import predTest as pred
import Queue
import sets

class Graph:
	
	points = []
	segments = [] 
	adjList = [[]] # Adjacency List: list of segments connecting to a point idx
	
	
	def __init__(self, points, segments):
		
		self.points = points
		self.segments = segments
		self.buildAdjList()

	
	def buildAdjList(self):
		# [point][segment] : list of segments connecting to a point
		# return adjList
		
		self.adjList = []
		for i in range(len(self.points)):
			self.adjList.append([])
			
		for s in self.segments:
			self.adjList[s.start].append(s.id)

	
	def shortestPath_Dijkstra(self, startNodeId, endNodeId, limit=INF):
		# Dijkstra shortest Path from startNodeId to endNodeId
		# limit is the maximum path length that the Dijkstra visits

		segments = self.segments
		dist = [INF] * len(self.points)
		pq = Queue.PriorityQueue()
		dist[startNodeId] = 0.0
		pq.put([dist[startNodeId],startNodeId])

		while not pq.empty():

			t = pq.get()

			if t[1] == endNodeId:
				return dist[endNodeId]
			if t[0] > limit:
				break
				
			if t[0] == dist[t[1]]:
				for sid in self.adjList[t[1]]:
					if segments[sid].length + t[0] < dist[segments[sid].end]:
						id = segments[sid].end
						length = segments[sid].length
						dist[id] = length + t[0]
						pq.put([dist[id], id])
						
		return INF
			
						
	def shortestPath_Astar(self, startNodeId, endNodeId, limit=INF, endSegId=-1):
		# A* search from startNodeId to endNodeId
		# avoid turning back, including endSegId if specified
		#       since startSeg is not included, don't need to check for first segment

		segments = self.segments
		trace = [-1] * len(self.points)
		cost = [INF] * len(self.points)
		pq = Queue.PriorityQueue()
		cost[startNodeId] = self.points[endNodeId].distTo(self.points[startNodeId])
		pq.put([cost[startNodeId], startNodeId, -1]) # cost, node id, segment id

		while not pq.empty():
		
			t = pq.get()

			trace[t[1]] = t[2]
			preS = self.segments[t[2]]

			if t[1] == endNodeId and (endSegId != -1 and segments[endSegId].end != preS.start):
				
				path = []
				tmp = endNodeId
				while trace[tmp] != -1:
					sid = trace[tmp]
					path.append(sid)
					tmp = segments[sid].start
				path.reverse()

				return [cost[endNodeId] - self.points[t[1]].distTo(self.points[endNodeId]), path]
			
			if t[0] > limit:
				break
				

			if t[0] == cost[t[1]]:

				for sid in self.adjList[t[1]]:
					
					s = segments[sid]

					length = segments[sid].length
					newcost = t[0] - self.points[t[1]].distTo(self.points[endNodeId]) \
						+ length + self.points[s.end].distTo(self.points[endNodeId])
					if newcost < cost[s.end] and (preS.end != s.start or preS.start != s.end):
						cost[s.end] = newcost
						pq.put([cost[s.end], s.end, sid])
		

		return [INF, []]


	def routePredict(self, cur, past):
		# cur: current segment idx
		# past: list of past segments idx
		#       past[0]: furthest in the past
		#       past[len - 1]: nearest in the past
		
		segments = self.segments
		adjList = self.adjList

		# assume uniform distribution
		# p = 1.0
		# for s in past:
		# 	p *= 1.0 / (len(adjList[ self.segments[s].end ]) + 1.0)

		# use route prediction
		p = pred.calProbOf(cur, past)

		return p


	def filterMarkovian(self, stateProbs, limitLen):
		# states: dictionary of candidate segments id and its probabilities
		# stateProbs = { segment_Id: probabilites }
		# limitLen: when the maximum length exceeds limitLen, stop filtering
		# !!! assume Markovian

		segments = self.segments
		adjList = self.adjList


		if limitLen <= 0:
			print 'limitLen:', limitLen
			return stateProbs


		states = stateProbs.keys()
		nxtStateProbs = {}

		maxSegLen = 0.0
		for s in states:

			# staying on same segment
			if s not in nxtStateProbs:
				nxtStateProbs[s] = 0.0
			nxtStateProbs[s] += stateProbs[s] * self.routePredict(s, [s])

			maxSegLen = max(maxSegLen, self.segments[s].length)

			# transition to the next segments
			for sid in adjList[segments[s].end]:

				if sid not in nxtStateProbs:
					nxtStateProbs[sid] = 0.0
				nxtStateProbs[sid] += stateProbs[s] * self.routePredict(sid, [s])		

				maxSegLen = max(maxSegLen, self.segments[sid].length)

		limitLen -= maxSegLen # reduce the limitLen by the maximum length of visited path

		return self.filterMarkovian(nxtStateProbs, limitLen)


	# def filterMarkovian(self, stateProbs, coverSet):
	# 	# states: dictionary of candidate segments id and its probabilities
	# 	# stateProbs = { segment_Id: probabilites }
	# 	# coverSet: set of candidate segments in need of visiting
	# 	#            the coverSet is removed until it is empty
	# 	#            function stops when coverSet is empty
	# 	# !!! assume Markovian

	# 	segments = self.segments
	# 	adjList = self.adjList


	# 	if len(coverSet) == 0:
	# 		return stateProbs


	# 	states = stateProbs.keys()
	# 	nxtStateProbs = {}


	# 	for s in states:

	# 		if s in coverSet:
	# 			coverSet.remove(s)

	# 		# staying on same segment
	# 		if s not in nxtStateProbs:
	# 			nxtStateProbs[s] = 0.0
	# 		nxtStateProbs[s] += stateProbs[s] * self.routePredict(s, [s])

	# 		# transition to the next segments
	# 		for sid in adjList[segments[s].end]:
				
	# 			if sid in coverSet:
	# 				coverSet.remove(sid)

	# 			if sid not in nxtStateProbs:
	# 				nxtStateProbs[sid] = 0.0
	# 			nxtStateProbs[sid] += stateProbs[s] * self.routePredict(sid, [s])		


	# 	return self.filterMarkovian(nxtStateProbs, coverSet)


	def BFS(self, startSegId, length):
	# allow to stay on the same segment
	# breadth first search from startSegId, with length limit = length

		segments = self.segments
		points = self.points
		adjList = self.adjList

		paths = [ [startSegId] ]
		length -= 1

		while length > 0:
			
			length -= 1
			newpaths = []

			for p in paths:

				l = p[len(p) - 1]
				for sid in adjList[segments[l].end]:
					np = p[:] + [sid]
					newpaths.append(np)

				np = p[:] + [l]
				newpaths.append(np)

			paths = newpaths[:]

		return paths


	def filter(self, stateProbs, limitLen, numBacks):
		# startProbs = {segmentId:probability}
		# limitLen: algorithm terminates when limitLen reaches
		# numBack: >= 2 (2 == Markovian)

		# P(x1,x2,x3) = P(x1|x2,x3) * P(x2|x3) * P(x3)
		# bel0(x3)
		# bel1(x2) = sum_x3( P(x2|x3) * P(x3) )
		# bel2(x1) = sum_x2_x3( P(x1|x2,x3) * P(x2|x3) * bel0(x3) )
		# need backward pointers? -> create a reverse adjList: rAdjList 
		# --> no need for backward pointers (no need rAdjList)
		# stateProbs 2 steps aways
		# also need stateProbs 1 steps aways to cover all cases
	
		segments = self.segments
		adjList = self.adjList
		BFS = self.BFS

		if limitLen <= 0:
			print 'limitLen:', limitLen
			return stateProbs

		states = stateProbs.keys()
		nxtStateProbs = {}

		maxSegLen = 0.0

		for s in states:

			paths = BFS(s, numBacks)

			for p in paths:
				pl = 0.0
				for i in p:
					pl += self.segments[i].length
				maxSegLen = max(maxSegLen, pl)

			for p in paths:
				l = p[len(p) - 1]

				if l not in nxtStateProbs:
					nxtStateProbs[l] = 0

				nxtStateProbs[l] += stateProbs[p[0]] * self.routePredict(l, p[:len(p)-1])

		limitLen -= maxSegLen # reduce the limitLen by the maximum length of visited path

		return self.filter(nxtStateProbs, limitLen, numBacks)


	# def filter(self, stateProbs, coverSet, numBacks):
	# # P(x1,x2,x3) = P(x1|x2,x3) * P(x2|x3) * P(x3)
	# # bel0(x3)
	# # bel1(x2) = sum_x3( P(x2|x3) * P(x3) )
	# # bel2(x1) = sum_x2_x3( P(x1|x2,x3) * P(x2|x3) * bel0(x3) )
	# # need backward pointers? -> create a reverse adjList: rAdjList 
	# # --> no need for backward pointers (no need rAdjList)
	# # stateProbs 2 steps aways
	# # also need stateProbs 1 steps aways to cover all cases
	# # REQUIRE: numBacks >= 2 (2 ~ Markovian)
	
	# 	segments = self.segments
	# 	adjList = self.adjList
	# 	BFS = self.BFS

	# 	if len(coverSet) == 0:
	# 		# !!! need to check if stateProbs cover all cases (i steps away where i < numBacks)
	# 		#     if not, include other stateProbs of smaller numBacks --> take cared of in the BFS function
	# 		# !!! what if coverSet cannot be covered all? --> Use maximum length instead
	# 		print "empty coverSet"
	# 		return stateProbs

	# 	states = stateProbs.keys()
	# 	nxtStateProbs = {}


	# 	for s in states:

	# 		paths = BFS(s, numBacks)

	# 		for p in paths:
	# 			l = p[len(p) - 1]

	# 			if l in coverSet:
	# 				coverSet.remove(l)

	# 			if l not in nxtStateProbs:
	# 				nxtStateProbs[l] = 0

	# 			nxtStateProbs[l] += stateProbs[p[0]] * self.routePredict(l, p[:len(p)-1])

	# 	return self.filter(nxtStateProbs, coverSet, numBacks)


	def findCandidate(self, startSegId, target, radius, initLimit, step, candidateSegs, candidatePoints):
		# input: startNodeId on graph
		#        point target is of any coordinate
		#        radius is maximum distance of candidate from target
		#        initLimit for A* search, will be increased until
		#          number of candidates unchanged
		#        each time limit is increase by step value
		# notes: A* avoids turning back from 2nd segments onwards
		# return [candidateSegs, candidatePoints, limit]
		#         where: limit is maximum path length that A* visits

		startNodeId = self.segments[startSegId].end

		cost = [INF] * len(self.points)
		pq = Queue.PriorityQueue()
		cost[startNodeId] = self.points[startNodeId].distTo(target) # is it ok not to use segId for identity?
		pq.put([cost[startNodeId], startNodeId, startSegId])
		
		s = self.segments[startSegId]
		d = target.dist2LineSeg(self.points[s.start], self.points[s.end])
		if d[0] <= radius and startSegId not in candidateSegs:
			candidateSegs.add(startSegId)
			candidatePoints.append(d[1])

		# check if startSegId is a candidate or not
		
		limit = initLimit
		cNo = -1
		first = True
		
		while not pq.empty():
		
			t = pq.get()
			
			if t[0] > limit:
				if len(candidateSegs) != cNo: # or len(candidateSegs) == 0: try to make initial limit large enough
					while limit < t[0]:
						limit += step
					cNo = len(candidateSegs)
				else:
					return limit - step
					
			if t[0] == cost[t[1]]:
				for sid in self.adjList[t[1]]:
					s = self.segments[sid]
					preS = self.segments[t[2]]
					
					newcost = s.length + self.points[s.end].distTo(target)
					if newcost < cost[s.end] and (preS.end != s.start or preS.start != s.end or first): # prevent turning back
						cost[s.end] = newcost
						pq.put([cost[s.end], s.end, s.id])
						d = target.dist2LineSeg(self.points[s.start], self.points[s.end])
						if d[0] <= radius and s.id not in candidateSegs:
							candidateSegs.add(s.id)
							candidatePoints.append(d[1])

			first = False
		
		return limit - step # should never reach here


	def scanAll(self, target, radius):
		# scan all the network to find candidate segments
		# within radius from target, and projected points 
		# on those candidate segments
		# return [candidateSegs, candidatePoints]

		candidateSegs = []
		candidatePoints = []

		for s in self.segments:
			d = target.dist2LineSeg(self.points[s.start], self.points[s.end])
			if d[0] <= radius:
				candidateSegs.append(s.id)
				candidatePoints.append(d[1])

		return [candidateSegs, candidatePoints]


