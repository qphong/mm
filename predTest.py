
import libplump

# simple example predict the next element given the list of history elements


restaurant = libplump.SimpleFullRestaurant()

nodeManager = libplump.SimpleNodeManager(restaurant.getFactory())
parameters = libplump.SimpleParameters()

seq = libplump.VectorInt([0, 1, 5, 6, 9, 11,\
	0, 1, 7, 9, 11,\
	0, 1, 5, 6, 8, 12, 13,\
	0, 1, 5, 6, 9, 10, 12, 13,\
	0, 1, 7, 9, 10, 12, 13,\
	0, 1, 7, 8, 12, 13,\
	3, 4, 6, 9, 11,\
	2, 5, 6, 9, 11])
numTypes = max(seq)

model = libplump.HPYPModel(seq, nodeManager, restaurant, parameters, numTypes)


def computeL(start, end):

	global model
	for i in range(start, end):
		model.computeLosses(i, end)

def clearSeq():
	"""
		remove all elements in sequence s
	"""

	global seq
	while len(seq) > 0:
		seq.pop_back()


def calProbOf(cur, past):
	"""
		input: array of elements in model (integer)
		output: probability of this array (log2 probability)
		5 order Markov
	"""
	global seq
	global model

	clearSeq()

	res = 0.0
	for i in range(0,len(past)):
		seq.push_back(past[i])
	seq.push_back(cur)

	res = model.predict(0, len(seq) - 1, seq[ len(seq) - 1 ])

	clearSeq()

	return res


computeL(0, 6)
computeL(6, 11)
computeL(11, 18)
computeL(18, 26)
computeL(26, 33)
computeL(33, 38)
computeL(38, 43)

# del model
# del nodeManager
# del restaurant

# addSeqsFromFile("data.txt")

# model.insertContextAndObservation(0,2,13)
# model.insertContextAndObservation(0,2,14)

# print model.computeLosses(0,len(seq))
# for i in range(seq.size()):
# 	model.computeLosses(i, len(seq))
	
# for i in range(seq.size()):
#   print model.toString()

# for i in range(len(seq)):
#    print model.predict(0,i,seq[i])

# make sure destructors are called in correct order
# del model
# del nodeManager


