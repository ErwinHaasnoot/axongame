
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

#Load data
print "loading data"
data = funcs.loadData('/home/erwin/workspace/ee_bootstrap/data_by_cookie.json')

outfolder = 'files/Top10Perc'
windowSizes1 = range(5,30,5)    # Sizes of attempt group 1
windowSizes2 = range(5,30,5)    # Sizes of attempt group 2

print "OBSERVED DATA"
os.runObs(data, windowSizes1, windowSizes2,outfolder, 90)

print "BOOTSTRAP"
bootrec = bs.runBoot(data, 20, windowSizes1, windowSizes2, 90)

funcs.drawGraphs(bootrec, outfolder, windowSizes1, windowSizes2)