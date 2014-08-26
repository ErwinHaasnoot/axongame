
#Import modules
import json
import pickle
import collections
import numpy as np
import scipy.stats as st
from scipy.stats.stats import pearsonr
import scipy.stats.mstats as ssm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import * #i know I shouldn't do this
from matplotlib import cm
import utils.funcs as funcs

#Import project files
import utils.bootstrap as bs
import utils.observed as os


import sys
if len(sys.argv[1]) == 1:  
    datafile = '../data_by_cookie_slim.json'
    outputFolder = '.'
    outputSuffix = ''
    iterations = 10
    epochmult = 4
else:
    datafile = sys.argv[0]
    outputFolder = sys.argv[1]
    outputSuffix = sys.argv[2]
    iterations = sys.argv[3]
    epochmult = sys.argv[4]

#Load data
print 'Running log regression analysis of variance vs mean, 2nd order'
outputFolder = outputFolder +  + '/logRegressTop10'
data = funcs.loadData(datafile)
#properData  = [[data[k][l][0] for l in collections.OrderedDict(sorted(data[k].items()))] for k in data]
#Process X = polyfit regression test
processX = lambda x,x_plays: np.polyfit(x_plays, x, 2, full = True)[1]
#Preprocessing = taking logarithm of all data points
preprocess = lambda x: [np.log(k) for k in x]

windowSizes1 = range(5,30,5)    # Sizes of attempt group 1
windowSizes2 = range(5,30,5)    # Sizes of attempt group 2

funcs.ensurePath(outputFolder)

print "OBSERVED DATA"
os.runObs(data, windowSizes1, windowSizes2, outputFolder, rankFilter = 90, preprocess = preprocess, processX = processX)
#execfile("sup_ee_boot_varxy.py")

print "BOOTSTRAP"
bootrec = bs.runBoot(data, iterations, windowSizes1, windowSizes2, rankFilter = 90, preprocess = preprocess, processX = processX)

pickle.dump(bootrec,open(outputFolder + '/logRegress' + outputSuffix + '.p', 'wb'))
#execfile("sup_ee_observed_varxy.py")

#funcs.drawGraphs(bootrec, outfolder, windowSizes1, windowSizes2)