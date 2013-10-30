# Point(lat, lng, time)
# Segment(id, start, end, length, speedlm=200, alias="", name="")

from math import *
from graph import *

pointData = [[1,3], [1,1], [2,3], [3,4], [3,1], [4,3], [5,3], [5,1], [7,4], [7,2]]
segData = [[0, 1, 2, 2], \
            [1, 2, 5, 2], \
            [2, 1, 5, 2*sqrt(2.0)], \
            [3, 1, 3, 1], \
            [4, 3, 4, sqrt(2.0)], \
            [5, 5, 4, 3], \
            [6, 4, 6, sqrt(2.0)], \
            [7, 5, 6, sqrt(5.0)], \
            [8, 6, 8, sqrt(5.0)], \
            [9, 6, 7, 1], \
            [10, 7,  8, 2], \
            [11, 7, 9, sqrt(5.0)], \
            [12, 8, 10, sqrt(5.0)], \
            [13, 10, 9, 2]] 

for s in segData:
      s[1] -= 1
      s[2] -= 1
      

points = []
for p in pointData:
	points.append(Point(p[0], p[1]))

segments = []
for s in segData:
	segments.append(Segment(s[0], s[1], s[2], s[3]))

G = Graph(points, segments)

# print "Test shortestPath:"
# print "  1. 1 + 2*sqrt(2)", (1 + 2*sqrt(2))
# print "Dijkstra:", G.shortestPath_Dijkstra(0,5)
# print "A*:", G.shortestPath_Astar(0,5)
# print "  2. 2*sqrt(2)", 2*sqrt(2)
# print "Dijkstra:", G.shortestPath_Dijkstra(0,4)
# print "A*:", G.shortestPath_Astar(0,4)
# print "  3. 2 + 2*sqrt(2) + sqrt(5)", (2 + 2*sqrt(2) + sqrt(5))
# print "Dijkstra:", G.shortestPath_Dijkstra(0,8)
# print "A*:", G.shortestPath_Astar(0,8)


# findCandidate(self, startSegId, target, radius, initLimit, step, candidateSegs, candidatePoints)



# from sets import *

# candidateSegs = Set()
# candidatePoints = []

# r = G.findCandidate(3, Point(4,2), 1.0, 1.0, 0.5, candidateSegs, candidatePoints)







