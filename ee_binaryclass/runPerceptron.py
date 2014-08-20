import utils.funcs as funcs
import numpy as np
import scipy.stats as st
#from numpy import array, dot, random, mean
from random import choice
import matplotlib.pyplot as plt

plt.close('all')
#Load data
print "loading data"
data = funcs.loadData('../data_by_cookie.json')

#Generate artificial training data
#mu = np.mean([k[:10] for k in data if len(k) >= 10],axis=0)

#signalf = lambda x: 0 if x[2] < 18000 else 1
#training_data = funcs.generateSamples(500000, signalf)

#Set up perceptron
m = 100
s = 10
errors = []
eta = 0.2
n = 100000
dPrimes = [0]*m
endweights = []
training_data = [(np.array(k[:s]),0 if len(k) < 2*s else 1) for k in data if len(k) >= s]
print 'Overall plays over 20 plays: {}'.format(np.mean([t[1] for t in training_data]))
for i in xrange(m):
    #print 'Preparing training data'
    w = 2 * np.random.rand(s) - 1
    stepf = lambda x: 0 if x < 0 else 1
    
    #print 'Training perceptron - n = {} and s = {}'.format(n,s)
    for j in xrange(n):
        x, expected = choice(training_data)
        result = np.dot(w,x)
        error = expected - stepf(result)
        errors.append(error)
        w += eta * error * funcs.normalize(x)
        #w = w / np.linalg.norm(w) #normalize
    #print 'Training completed'
    #print 'Testing performance'
    #test_data consists of rows (x, expected, result) or (x, signal, response)
    
    print w
    test_data = [(t[0], t[1], stepf(np.dot(w,t[0]))) for t in training_data]
    percHits = np.mean([1 if t[2] == 1 else 0 for t in test_data if t[1] == 1]) # Percentage right hits
    falseAlarm = np.mean([1 if t[2] == 1 else 0 for t in test_data if t[1] == 0]) # Percentage false positives
    dPrime = funcs.dprime(percHits, falseAlarm)
    #if percHits> .65:        
    endweights.append(funcs.normalize(w))
    
    dPrimes[i] = dPrime
    print 'Hit % = {}, but false alarm % = {}, d\' = {}'.format(percHits,falseAlarm, dPrime)   
    #print w # print the weights

#print dPrimes
#print np.mean(dPrimes),np.std(dPrimes)

plt.close()
fig = plt.figure()
for k in endweights:    
    plt.ylim([-1,1])    
    plt.plot(k)


plt.figure()
plt.ylim([-1,1])
plt.plot(np.mean(endweights,axis=0))
plt.show()
