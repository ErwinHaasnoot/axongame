import utils.funcs as funcs
import numpy as np
import scipy.stats as st
from random import choice
#import matplotlib.pyplot as plt
import pickle

def main(datafile = '../data_by_cookie_slim.json', outputFolder = '.', iterations = 10, epochmult = 4):
    
    filename = 'runPerceptronArtificial'
    outputFile = '{}/{}.p'.format(outputFolder,filename)
    
    #plt.close('all')
    #Load data
    print 'Perceptron quit after 20 from 10 games with Perceptron'
    
    #data = funcs.loadData(datafile)
    
    #Generate artificial training data
    #mu = np.mean([k[:10] for k in data if len(k) >= 10],axis=0)
    
    signalf = lambda x: 0 if x[2] < 18000 else 1
    training_data = funcs.generateSamples(50000, signalf)
    
    #Set up perceptron
    s = 10 # games
    eta = 0.2 # learning rate
    dPrimes = [0]*iterations #
    out = []
    stepf = lambda x: 0 if x < 0 else 1
    #training_data = [(np.array(k[:s]),0 if len(k) < 2*s else 1) for k in data if len(k) >= s]
    n = len(training_data) * epochmult
    
    print 'iterations: {}\nMultiplier Samplesize Epochs: {}\noutput file: {}\n'.format(iterations,epochmult,outputFile)
    print 'Overall plays over 20 plays: {}'.format(np.mean([t[1] for t in training_data]))
    print 'Learning from {} samples...'.format(len(training_data))
    for i in xrange(iterations):
        #print 'Preparing training data'
        w = 2 * np.random.rand(s) - 1
        
        #print 'Training perceptron - n = {} and s = {}'.format(n,s)
        for j in xrange(n):
            x, expected = choice(training_data)
            result = np.dot(w,x)
            error = expected - stepf(result)
            w += eta * error * funcs.normalize(x)
        #print 'Training completed'
        #print 'Testing performance'
        #test_data consists of rows (x, expected, result) or (x, signal, response)
        
        #print w
        test_data = [(t[0], t[1], stepf(np.dot(w,t[0]))) for t in training_data]
        percHits = np.mean([1 if t[2] == 1 else 0 for t in test_data if t[1] == 1]) # Percentage right hits
        falseAlarm = np.mean([1 if t[2] == 1 else 0 for t in test_data if t[1] == 0]) # Percentage false positives
        dPrime = funcs.dprime(percHits, falseAlarm)
        #if percHits> .65:        
        #endweights.append(funcs.normalize(w))
        dPrimes[i] = dPrime
        #print 'Hit % = {}, but false alarm % = {}, d\' = {}'.format(percHits,falseAlarm, dPrime)   
        out.append((percHits, falseAlarm, dPrime, w))
        #print w # print the weights
        
    dprimes = out    
    pickle.dump(out,open(outputFile, 'wb'))      
        
    print
    print 'Results:'
    print 'Mean d\' score for each quit opportunity: {}'.format([np.mean([k[i] for k in dprimes]) for i in xrange(1)])
    print 'Std : {}'.format([np.std([k[i] for k in dprimes]) for i in xrange(1)])
    print 'Max : {}'.format([np.max([k[i] for k in dprimes]) for i in xrange(1)])
    print
    print
    
if __name__ == "__main__":
    main()
