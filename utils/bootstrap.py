import numpy as np
import utils.funcs as funcs
from scipy.stats.stats import pearsonr
from scipy import stats
import pickle
#import bisect

#Run bootstrap
#Amount of samples taken is equal to amount of players in bootstrap
def runBoot(data, runs,  outputFolder, rankFilter = 0, preprocess = False, processX = False, processY = False):
    
    
    windowSizes1 = range(5,30,5)    # Sizes of attempt group 1
    windowSizes2 = range(5,30,5)    # Sizes of attempt group 2
    bootrec=np.zeros( (1,len(windowSizes1),len(windowSizes2),runs) ) #output
    
    #If no processing steps have been added, default processX to variance and processY to mean
    #Like in the paper
    if processX == False:
        processX = lambda x,x_plays: np.var(x,axis=0)
    if processY == False:
        processY = lambda x,x_plays: np.mean(x,axis=0)
        
    #Run preprocessing if passed along
    if(preprocess != False):
        data = preprocess(data)
    
    for i1 in xrange(len(windowSizes1)):
        for i2 in xrange(len(windowSizes2)):
            window1 = windowSizes1[i1]       
            window2 = windowSizes2[i2] 
            first_plays = range(window1)
            second_plays = range(window1,window1+window2)
            #Organize bootdata
            bootdata,n = funcs.organiseData(data, first_plays + second_plays, rankFilter)
            
            #print "Starting bootstrap calculations for group size " + str(window1) + "," + str(window2)
            for booti in xrange(runs):
                #print "iteration " +str(booti) + " of " + str(runs)
                
                first = [funcs.sampleWr(bootdata[key],n) for key in first_plays]
                second = [funcs.sampleWr(bootdata[key],n) for key in second_plays]
                
                # Per column, ie per player, calculate mean/variance
                x = processX(first, first_plays)
                y = processY(second, second_plays)
            
                #pearson r correlation
                a,b = pearsonr(x,y)
                #print "Boot %i" % booti 
                #print "r = %.2f, p = %.2f" % (a,b)
                
                bootrec[0,i1, i2, booti] = a
    
    pickle.dump(bootrec,open(outputFolder + '/bootrec.p', 'wb'))
    
    return bootrec