import numpy as np
import utils.funcs as funcs
import pickle

def runObs(data, outfolder ='.', rankFilter = 0, preprocess = False, processX = False, processY = False):
    windowSizes1 = range(5,30,5)    # Sizes of attempt group 1
    windowSizes2 = range(5,30,5)    # Sizes of attempt group 2
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
            total_attempts = window1 + window2            
                        
                        
        # --------------------------------------------
            # look at subsample of people who played more than x times   
            #print "organising data"
            big = [k for k in data if len(k) >= total_attempts]
            # --------------------------------------------
            #calc dict of maximum score for each player(=each key)
            #maxscore=[max(a) for a in big]
            
            #calc percentile ranking for each player (=each key)
            #prcentiles= np.percentile(maxscore,range(100))             
                        
                        
                        
            
            #construct vaiables dicts
            
            #print "calculating summary stats"
            #for each player make two lists, of plays 1-5 (first) and 6-10 (second)
            #and calculate summary stats av1,var1 and av2, var2
            
            if(rankFilter != 0):
                big = funcs.filterByPercRank(big,rankFilter)
                
            first = [k[0:window1] for k in big]
            second = [k[window1:window2+window1] for k in big]
            
            
            #av1=np.mean(first,axis=1)
            x = processX(zip(*first),first_plays)
            #x = processX(zip(*first), first_plays)   
            y = processY(zip(*second),second_plays) #processY(second, second_plays) 
            #var2 = np.var(second,axis=1)
            
            
                                     
                    
        
            #find percentile values                    
            #prcentiles_x=np.percentile(x,range(100))                    
            #prcentiles_y=np.percentile(y,range(100))
        
        
            #make dict of prcentile values for each statistic for each player
            #xlist=[bisect.bisect(prcentiles_x,k) for k in x]
            #ylist=[bisect.bisect(prcentiles_y,k) for k in y]
                   
            #print "saving data"
            pickle.dump(x, open(outfolder + '/save_a5_xlist' + str(window1) + "," + str(window2) +'.p', 'wb'))
            pickle.dump(y, open(outfolder + '/save_a5_ylist' + str(window1) + "," + str(window2) +'.p', 'wb'))
            
            #print "mean x: ",np.mean(x)
            #print "mean y: ",np.mean(y)