
"""
This file contains functions to log information: transition and emission probabilites 
to text file; segments and points to javascript file for visualizing on Google map.
"""

from config import *


def logPoints(pnts, infos):
	# input: list of points pnts of type Point
	#        list of infos for these points in order
	#                infos of type string
	# Points are written into PATH_PNTS to visualize on Google map

	with open(PATH_PNTS, "w") as f:
		f.write("var points = [\n")

		if len(pnts) != 0:
			f.write("new google.maps.LatLng(%.10f, %.10f)" % (pnts[0].orgCoord[0], pnts[0].orgCoord[1]) )
		for p in pnts[1:]:
			f.write(",\nnew google.maps.LatLng(%.10f, %.10f)" % (p.orgCoord[0], p.orgCoord[1]) )

		f.write("];\n")


		f.write("var pointsInfo = [\n")
		
		if len(infos) != 0:
			f.write("\"%s\"" % infos[0])
		for i in infos[1:]:
			f.write(",\"%s\"" % i)
		
		f.write("];\n")



def logSegments(segs, pnts, infos):
	# input: list of segments segs of type Segments
	#        list of points pnts of type Point
	#        list of infos for these segments in order
	#                infos of type string
	# Segments are written into PATH_SEGS to visualize on Google map

	with open(PATH_SEGS, "w") as f:
		f.write("var segs = [\n")

		if len(segs) != 0:
			s = segs[0]
			f.write("[ new google.maps.LatLng(%.10f, %.10f), new google.maps.LatLng(%.10f, %.10f) ]" % \
				( pnts[s.start].orgCoord[0], pnts[s.start].orgCoord[1], \
				pnts[s.end].orgCoord[0], pnts[s.end].orgCoord[1]) )
		for s in segs[1:]:
			f.write(",\n[ new google.maps.LatLng(%.10f, %.10f), new google.maps.LatLng(%.10f, %.10f) ]" % \
				( pnts[s.start].orgCoord[0], pnts[s.start].orgCoord[1], \
				pnts[s.end].orgCoord[0], pnts[s.end].orgCoord[1]) )

		f.write("];\n")


	with open(PATH_SEGS_INFO, "w") as f:

		f.write("var ids = [")
		
		if len(segs) != 0:
			f.write("\'%s: %s(%d) %s\'" % (infos[0], segs[0].alias, segs[0].id, segs[0].name) )
		for i in range(len(segs))[1:]:
			f.write(",\'%s: %s(%d) %s\'" % (infos[i], segs[i].alias, segs[i].id, segs[i].name) )
		
		f.write("];\n")


def logEmsProbs(emsProbs, gpsIdx, segIds, segments):
	# append emission probabilites to file PATH_LOGS/ems.txt

	with open(PATH_LOGS + "ems.txt", "a") as f:

		f.write("==========%5d%5s==========\n" % (gpsIdx, "=") )

		for i in range(len(segIds)):
			s = segments[segIds[i]]
			f.write("%15d %30.15f\n" % (s.id, emsProbs[i]))


def logTransProbs(transProbs, gpsIdx, fromSegIds, toSegIds, segments):
	# append transition probabilites to file PATH_LOGS/trans.txt

	with open(PATH_LOGS + "trans.txt", "a") as f:
		
		f.write("==========%5d%5s==========\n" % (gpsIdx, "=") )
		
		for fi in range(len(fromSegIds)):
			fs = segments[fromSegIds[fi]]

			for ti in range(len(toSegIds)):
				ts = segments[toSegIds[ti]]
				f.write( "%15d %15d %30.15f\n" % (fs.id, ts.id, transProbs[fi][ti]) )


def logSegmentIds(segIds, segs, pnts):
	# segments with segIds are written to file PATH_SEGS 
	# for visualizing on Google map

	with open(PATH_SEGS, "w") as f:
		f.write("var segs = [\n")

		if len(segIds) != 0:
			
			s = segs[ segIds[0] ]

			f.write("[ new google.maps.LatLng(%.10f, %.10f), new google.maps.LatLng(%.10f, %.10f) ]" % \
				( pnts[s.start].orgCoord[0], pnts[s.start].orgCoord[1], \
				pnts[s.end].orgCoord[0], pnts[s.end].orgCoord[1]) )

		for sid in segIds[1:]:
			
			s = segs[ sid ]

			f.write(",\n[ new google.maps.LatLng(%.10f, %.10f), new google.maps.LatLng(%.10f, %.10f) ]" % \
				( pnts[s.start].orgCoord[0], pnts[s.start].orgCoord[1], \
				pnts[s.end].orgCoord[0], pnts[s.end].orgCoord[1]) )

		f.write("];\n")

		
	with open(PATH_SEGS_INFO, "w") as f:

		f.write("var ids = [")
		
		if len(segIds) != 0:
			f.write("\'%d: %s %s\'" % (segs[ segIds[0] ].id, segs[ segIds[0] ].alias, segs[ segIds[0] ].name) )

		for i in range(len(segIds))[1:]:
			f.write(",\'%d: %s %s\'" % (segs[ segIds[i] ].id, segs[ segIds[i] ].alias, segs[ segIds[i] ].name) )

		f.write("];\n")
