from utils import funcs
from utils.MLP import MLP
import numpy as np
print 'Loading data...'
data = funcs.loadData('../data_by_cookie_slim.json')

#Filter away bottom 75%
data = funcs.filterByPercRank(data, 75)

#Get first 10 values and try to decide whether people will keep on playing past 20 games
samples = np.fromiter(((funcs.normalize(np.array(k[:10])),0 if len(k) < 20 else 1) for k in data if len(k) >= 10),
                dtype=[('input',  float, 10), ('output', float, 1)])
print 'Learning from {} samples'.format(samples.size)
network = MLP(10,10,10,10,1)

out = network.learn(samples, epochs = samples.size * 400) #40 million epochs.. Too many?
network.storeWeights('Run1 10 10 1.w')

out = network.test(samples)
stepf = lambda x: 0 if x < .5 else 1
test_data = [(t[0], t[1], stepf(t[2])) for t in out]
percHits = np.mean([1 if t[2] == 1 else 0 for t in test_data if t[1] == 1]) # Percentage right hits
falseAlarm = np.mean([1 if t[2] == 1 else 0 for t in test_data if t[1] == 0]) # Percentage false positives

dPrime = funcs.dprime(percHits, falseAlarm)
print 'Hit % = {}, but false alarm % = {}, d\' = {}'.format(percHits,falseAlarm, dPrime)   
    

