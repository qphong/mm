
from config import *
from math import *

a = Point(2,-2)
b = Point(1,-4)
c = Point(4,-4)
d = Point(5,-3)
e = Point(3,-3)

a2b = a.distTo(b)
e2d = e.distTo(d)

if a2b != sqrt(5.0):
	print "fail: distTo a2b: %f" % a2b - sqrt(5.0)

if e2d != 2:
	print "fail: distTo e2d: %f" % e2d - 2


if not a.isSame(Point(2,-2.0)):
	print "fail: a isSame (2,-2.0)"


# if Point().greatCircleDist(Point()) != :
# 	print "fail: greatCircleDist"


if a.dist2Line(e,d)[0] != 1:
	print "fail: a.dist2Line e,d: %f" % a.dist2Line(e,d)[0] - 1


if a.dist2LineSeg(e,d)[0] != sqrt(2.0):
	print "fail: a.dist2LineSeg e,d: %f" % a.dist2LineSeg(e,d)[0] - sqrt(2.0)


