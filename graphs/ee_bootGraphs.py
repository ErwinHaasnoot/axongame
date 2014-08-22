#Load current run settings
import sys
datafile = sys.argv[0]
outputFolder = sys.argv[1]
outputSuffix = sys.argv[2]
iterations = sys.argv[3]
epochmult = sys.argv[4]

#Import relevant modules

import utils.funcs as funcs
import pickle
#Draw graphs for logRegress

#Set windowsizes
windowSizes1 = range(5,30,5)    # Sizes of attempt group 1
windowSizes2 = range(5,30,5)    # Sizes of attempt group 2

#Draw logregress graph
bootrec = pickle.load(open(outputFolder + '/logRegress/logRegress' + outputSuffix + '.p','rb'))
funcs.drawGraphs(bootrec, outputFolder, windowSizes1, windowSizes2)

#Draw varMean graph
bootrec = pickle.load(open(outputFolder + '/varMean/varMean' + outputSuffix + '.p','rb'))
funcs.drawGraphs(bootrec, outputFolder, windowSizes1, windowSizes2)