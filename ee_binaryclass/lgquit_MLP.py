from utils import funcs
from utils.MLP import MLP
import numpy as np
import json
import collections
import pickle

def main(datafile = '../data_by_cookie_slim.json', outputFolder = '.', outputSuffix = '', iterations = 10, epochmult = 4):
    print 'Local vs Global quit analysis with MLP'
    timethresh = 2
    timesize = 10
    filename = 'lgquit'
    outputFile = '{}/{}{}.p'.format(outputFolder,filename,outputSuffix)
    
    print 'Quit locations: {}\ntime threshold: {} hours\niterations: {}\nMultiplier Samplesize Epochs: {}\noutput file: {}'.format(timesize-1,timethresh,iterations,epochmult,outputFile)
    
    fh=open(datafile)
    data=json.load(fh)
    
    #Init values
    
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
    
    print 'Learning from {} samples...'.format(samples.size)
    
    network = MLP(timesize,10,10,10,timesize-1)
    
    #Calculate d' on a per element basis
    def processResults(network,results):
            
        stepf = lambda x: [0 if i < .5 else 1 for i in x]
        test_data = [(t[0], t[1], stepf(t[2])) for t in results]
        outnum = len(test_data[1][1])
        
        percHits = [np.mean(k) for k in [[1 if t[2][i] == 1 else 0 for t in test_data if t[1][i] == 1] for i in range(outnum)]] # Percentage right hits per element
        falseAlarm = [np.mean(k) for k in [[1 if t[2][i] == 1 else 0 for t in test_data if t[1][i] == 0] for i in range(outnum)]] # Percentage false positives per element
        dPrime = funcs.dprime(percHits, falseAlarm)
        
        out = (percHits,falseAlarm, dPrime, network.weights)
        #print 'Hit % = {}, but false alarm % = {}, d\' = {}'.format(percHits,falseAlarm, dPrime)   
        
        return out
    
    out = network.learnLoop(samples, iterations = iterations, epochs = epochmult * samples.size, processResults = processResults) #40 million epochs for full dataset.. Too many?
    #results = network.learn(samples, epochs = samples.size * 400) 
    
    pickle.dump(out,open(outputFile, 'wb'))
    #print out
    
    #results = network.test(samples)
    dprimes = pickle.load(open(outputFile,'rb'))
    #set nan to 0
    
    #Set NaN to 0 (tends to be Inf - Inf, so 0 makes sense). -Inf to 0 as well, 
    #usually is due to small but negligible difference in hit rate and false alarm rate,
    #that cause false alarm rate to become exactly 0 and hit rate to be slightly above it.
    dprimes = [[0 if np.isnan(i) or np.isinf(i)  else i for i in k[2]] for k in dprimes]
    
    print
    print 'Results:'
    print 'Mean d\' score for each quit opportunity: {}'.format([np.mean([k[i] for k in dprimes]) for i in xrange(timesize-1)])
    print 'Std : {}'.format([np.std([k[i] for k in dprimes]) for i in xrange(timesize-1)])
    print
    print

if __name__ == "__main__":  
    datafile = '../data_by_cookie_slim.json'
    outputFolder = '.'
    outputSuffix = ''
    iterations = 10
    epochmult = 4
    main(datafile, outputFolder, outputSuffix, iterations, epochmult)