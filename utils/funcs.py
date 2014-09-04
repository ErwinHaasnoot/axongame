import json
import pickle
import collections
import numpy as np
import scipy.stats as st
from scipy.stats.stats import pearsonr
import scipy.stats.mstats as ssm
import scipy.stats
import random
#####functions-------------------------------------
def sampleWr(population, k):
    "Chooses k random elements (with replacement) from a population"
    "from http://code.activestate.com/recipes/273085-sample-with-replacement"
    n = len(population)
    _random, _int = random.random, int  # speed hack 
    result = [None] * k
    for i in xrange(k):
        j = _int(_random() * n)
        result[i] = population[j]
    return result

def organiseData(data, windows,rankFilter = 0):
    #print "organising bootstrap data for group size " + str(window1) + "," + str(window2)
    #windows = ['%.5d'%(i+1) for i in range(window1+window2)]
    bootdata={a:[] for a in windows}
    data = [k for k in data if len(k) >= len(windows)]
    n = len(data)
    if rankFilter != 0:    
        data = filterByPercRank(data,90)
    loading=0
    if not loading:
        for k in data :
                for attempt in windows:
                    try:
                        bootdata[attempt].append(k[attempt])
                    except KeyError:
                        continue
    return bootdata,n

def filterByPercRank(data, rank):
    maxData = [max(k) for k in data]
    prcentiles = np.percentile(maxData,rank)
    #print prcentiles
    
    return [data[i] for i in range(len(data)) if maxData[i] > prcentiles]

def loadData(location): 
    fh=open(location)
    data=json.load(fh)
    return [[data[k][l][0] for l in collections.OrderedDict(sorted(data[k].items()))] for k in data]
    
def drawGraphs(outFolder, bootName,  windowSizes1, windowSizes2, zBottom = -1, zTop = 1):
    import matplotlib
    matplotlib.use('PDF')
    from matplotlib import pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    print 'Drawing bootstrap graphs for: {}'.format(bootName)
    bootrec = pickle.load(open('{}/{}/bootrec.p'.format(outFolder,bootName),'rb'))
    plt.close('all')
    Z_obs = np.zeros((len(windowSizes1),len(windowSizes2)))
    Z_lower = np.zeros((len(windowSizes1),len(windowSizes2)))
    Z_boot = np.zeros((len(windowSizes1),len(windowSizes2)))
    Z_upper = np.zeros((len(windowSizes1),len(windowSizes2)))
    Z_std = np.zeros((len(windowSizes1),len(windowSizes2)))
    
    currentFolder = outFolder + '/' + bootName
    
    for i1 in xrange(len(windowSizes1)):
        for i2 in xrange(len(windowSizes2)):
            groupn_i = windowSizes1[i1]       
            groupn_j = windowSizes2[i2]
            curbootrec=bootrec[0,i1,i2]
            print
            print "Analyzing %i - %i" % (groupn_i,groupn_j)
            xlist= pickle.load(open(currentFolder + '/save_a5_xlist' + str(groupn_i) + "," + str(groupn_j) +'.p', 'rb'))
            ylist= pickle.load(open(currentFolder + '/save_a5_ylist' + str(groupn_i) + "," + str(groupn_j) +'.p', 'rb'))
            a,b = pearsonr(xlist,ylist)
                    
            #now do CI for r value
            ci_upper=ssm.scoreatpercentile(curbootrec,97.5)
            ci_lower=ssm.scoreatpercentile(curbootrec,02.5)
            ci_mean=np.mean(curbootrec)
            ci_std=np.var(curbootrec)
            print scipy.stats.norm(ci_mean,ci_std).cdf(abs(a))
            print "r = %.3f, p = %.5f, %s of confidence interval" % (a,b, 'outside' if a > ci_upper or a < ci_lower else 'inside')
            print "Bootstrapped confidence intervals were Upper = %0.3f, Lower = %0.3f" % (ci_upper,ci_lower)
            
            Z_obs[i1][i2] = a 
            Z_upper[i1][i2] = ci_upper         
            Z_lower[i1][i2] = ci_lower    
            Z_boot[i1][i2] = ci_mean
            Z_std[i1][i2] = ci_std
            
            
    X = [[k for j in windowSizes2] for k in windowSizes1]  
    Y = [[j for j in windowSizes2] for k in windowSizes1]
    #One-sided Z value to p value
    Z_p = [[st.norm.sf((Z_obs[i][j] - Z_boot[i][j])/Z_std[i][j]) for j in range(len(windowSizes1))] for i in range(len(windowSizes1))]
    
    fig1 = plt.figure()
    
    fontsize = 16
    ax = fig1.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z_obs, rstride=1, cstride=1)
    fig1.suptitle('Observed Correlations', fontsize=20)
    ax.set_xlabel('Size window 1', fontsize = fontsize)
    ax.set_ylabel('Size window 2', fontsize = fontsize)
    ax.set_zlabel('r', fontsize = fontsize)
    ax.set_zlim(bottom = zBottom, top = zTop)
    
    plt.savefig('{}/figures/{}_corObs.pdf'.format(outFolder,bootName), bbox_inches='tight')
        
    fig2 = plt.figure()
    
    ax = fig2.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z_boot, rstride=1, cstride=1)
    fig2.suptitle('Bootstrap Average Correlations', fontsize=20)
    ax.set_xlabel('Size window 1', fontsize = fontsize)
    ax.set_ylabel('Size window 2', fontsize = fontsize)
    ax.set_zlabel('r', fontsize = fontsize)
    ax.set_zlim(bottom = zBottom, top = zTop)
    
    plt.savefig('{}/figures/{}_corBoot.pdf'.format(outFolder,bootName), bbox_inches='tight')
    
def drawPerceptronWeights(outFolder, perceptronName):
    import matplotlib
    matplotlib.use('PDF')
    from matplotlib import pyplot as plt
    print 'Drawing perceptron weight graphs for: {}'.format(perceptronName)
    
    percrec = pickle.load(open('{}/{}.p'.format(outFolder,perceptronName),'rb'))
    meanweights = np.mean([normalize(k[3]) for k in percrec], axis=0)
    
    printBinClassStats(percrec)
    
    fontsize = 16
    fig, ax = plt.subplots()
    plt.ylim([-1,1])
    plt.plot(meanweights, linewidth=2.0)
    fig.suptitle('Perceptron - Average Weights per Attempt', fontsize = 20)
    ax.set_ylabel('Average Weight', fontsize = fontsize)
    ax.set_xlabel('Attempt Nr.', fontsize = fontsize)
    plt.savefig('{}/figures/{}_weights.pdf'.format(outFolder,perceptronName), bbox_inches='tight')
    
def printBinClassStats(percrec):
    
    
    dprimes = [[0 if np.isnan(i) or np.isinf(i)  else i for i in k[2]] for k in percrec]   
    dlen = len(dprimes[0])
    print
    print 'Results:'
    print 'Mean d\' score for each quit opportunity: {}'.format([np.mean([k[i] for k in dprimes]) for i in xrange(dlen)])
    print 'Std : {}'.format([np.std([k[i] for k in dprimes]) for i in xrange(dlen)])
    print 'Max : {}'.format([np.max([k[i] for k in dprimes]) for i in xrange(dlen)])
    print
    print
    
    
def normalize(v):
    norm= np.linalg.norm(v)
    if norm == 0:
        return v
    else:
        return v / norm
    
def generateSamples(l,signalf):
    #Generate artificial training data
    
    mu = [9256.77966807,  14535.38014538,  17875.40788667,  19925.21490191,
      21309.08896041,  22153.02139166,  22965.43790506,  23497.02055964,
      24077.39869066,  25870.68556227]
    sigma = 1000
    data = np.random.randn(l,10)
    for i in xrange(10):
        data[:,i] = mu[i] + sigma * data[:,i]
    samples = np.zeros(l,dtype=[('input',  float, 10), ('output', float, 1)])
    for i in xrange(l):
        #normdata = normalize(data[i])
        normdata = data[i]
        samples[i] = np.array(normdata),signalf(normdata)
    print np.mean(samples['output'])
    return samples

def dprime(hitRate, falseAlarmRate):
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        if not isinstance(hitRate, list):
            hitRate = [hitRate]
            falseAlarmRate = [falseAlarmRate]
        
        return [st.norm.ppf(hitRate[i]) - st.norm.ppf(falseAlarmRate[i]) for i in range(len(hitRate))]
        
def ensurePath(path):
    import os
    if not os.path.exists(path):
        os.makedirs(path)

def flat_for(a, f):
    a = a.reshape(-1)
    for i, v in enumerate(a):
        a[i] = f(v)