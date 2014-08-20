from utils import funcs
from utils.MLP import MLP
import numpy as np
import json
import collections
import pickle
print 'Loading data...'

location = '../data_by_cookie_slim.json'
fh=open(location)
data=json.load(fh)

#Init values
timethresh = 2
timesize =10
#Properly sort data filter games
data = [[data[k][l] for l in collections.OrderedDict(sorted(data[k].items()))] for k in data]
inputdata = [[l[0] for l in k] for k in data if len(k) == timesize]
#Calculate time differences
timediff_data = [[((k[l][1] - k[l-1][1]) * 24 + (k[l][2] - k[l-1][2])) for l in range(1,len(k))] for k in data if len(k) == timesize]

#Threshold it
timediff_padthresh = [[1 if len(k) <= l or k[l] >= timethresh else 0 for l in range(timesize-1)] for k in timediff_data]

#Set up samples
samples = np.fromiter(((funcs.normalize(inputdata[i]),timediff_padthresh[i]) for i in range(len(inputdata))),
                dtype=[('input',  float, timesize), ('output', float, timesize-1)])


network = MLP(timesize,10,10,timesize-1)

#Calculate d' on a per element basis
def processResults(results):
        
    stepf = lambda x: [0 if i < .5 else 1 for i in x]
    test_data = [(t[0], t[1], stepf(t[2])) for t in results]
    outnum = len(test_data[1][1])
    
    percHits = [np.mean(k) for k in [[1 if t[2][i] == 1 else 0 for t in test_data if t[1][i] == 1] for i in range(outnum)]] # Percentage right hits per element
    falseAlarm = [np.mean(k) for k in [[1 if t[2][i] == 1 else 0 for t in test_data if t[1][i] == 0] for i in range(outnum)]] # Percentage false positives per element
    dPrime = funcs.dprime(percHits, falseAlarm)
    
    out = (percHits,falseAlarm, dPrime)
    #print 'Hit % = {}, but false alarm % = {}, d\' = {}'.format(percHits,falseAlarm, dPrime)   
    
    return out

out = network.learnLoop(samples, iterations = 100, epochs = 400 * samples.size, processResults = processResults) #40 million epochs for full dataset.. Too many?
#results = network.learn(samples, epochs = samples.size * 400) 

pickle.dump(out,open('full_run_data.p', 'wb'))
print out

#network.loadWeights('Run1 Slim sample.w')

#results = network.test(samples)

