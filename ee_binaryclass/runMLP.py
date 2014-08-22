from utils import funcs
from utils.MLP import MLP
import numpy as np
import pickle
import sys
print 'Predict play of 20 games or more from 10 games analysis with MLP'
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
filename = 'runMLP'
outputFile = '{}/{}{}.p'.format(outputFolder,filename,outputSuffix)
data = funcs.loadData(datafile)

#Filter away bottom 75%
data = funcs.filterByPercRank(data, 75)

print 'iterations: {}\nMultiplier Samplesize Epochs: {}\n output file: {}'.format(iterations,epochmult,outputFile)


#Get first 10 values and try to decide whether people will keep on playing past 20 games
samples = np.fromiter(((funcs.normalize(np.array(k[:10])),0 if len(k) < 20 else 1) for k in data if len(k) >= 10),
                dtype=[('input',  float, 10), ('output', float, 1)])
print 'Learning from {} samples...'.format(samples.size)
network = MLP(10,10,10,1)

def processResults(network,results):
    stepf = lambda x: 0 if x < .5 else 1
    test_data = [(t[0], t[1], stepf(t[2])) for t in results]
    percHits = np.mean([1 if t[2] == 1 else 0 for t in test_data if t[1] == 1]) # Percentage right hits
    falseAlarm = np.mean([1 if t[2] == 1 else 0 for t in test_data if t[1] == 0]) # Percentage false positives
    
    dPrime = funcs.dprime(percHits, falseAlarm)
    out = (percHits, falseAlarm, dPrime, network.weights)
    return out
#print 'Hit % = {}, but false alarm % = {}, d\' = {}'.format(percHits,falseAlarm, dPrime)  
out = network.learnLoop(samples, iterations = iterations, epochs = epochmult * samples.size, processResults = processResults) #40 million epochs for full dataset.. Too many? 

pickle.dump(out,open(outputFile, 'wb'))
#print out

#results = network.test(samples)
dprimes = pickle.load(open(outputFile,'rb'))
#set nan to 0

dprimes = [[0 if np.isnan(i) or np.isinf(i)  else i for i in k[2]] for k in dprimes]   

print
print 'Results:'
print 'Mean d\' score for each quit opportunity: {}'.format([np.mean([k[i] for k in dprimes]) for i in xrange(1)])
print 'Std : {}'.format([np.std([k[i] for k in dprimes]) for i in xrange(1)])
print
print
