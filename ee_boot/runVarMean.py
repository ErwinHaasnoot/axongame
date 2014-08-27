#Import modules
import pickle
import numpy as np
import utils.funcs as funcs

#Import project files
import utils.bootstrap as bs
import utils.observed as os

def main(datafile = '../data_by_cookie_slim.json', outputFolder = '.', outputSuffix = '', iterations = 10, epochmult = 4):
    #Load data
    print 'Running analysis of variance vs mean correlation, 1st order'
    outputFolder = outputFolder + '/varMean'
    data = funcs.loadData(datafile)
    #Process X = polyfit regression test
    print 'iterations: {}\noutput folder: {}\n'.format(iterations,outputFolder)
    #processX = lambda x,x_plays: np.mean(x,axis=0)
    #processY = lambda x,x_plays: np.var(x,axis=0)
    
    preprocess = False
    
    windowSizes1 = range(5,30,5)    # Sizes of attempt group 1
    windowSizes2 = range(5,30,5)    # Sizes of attempt group 2
    
    print "OBSERVED DATA"
    os.runObs(data, windowSizes1, windowSizes2, outputFolder, preprocess = preprocess, processX = processX, processY = processY)
    #execfile("sup_ee_boot_varxy.py")
    
    print "BOOTSTRAP"
    bootrec = bs.runBoot(data, 20, windowSizes1, windowSizes2, preprocess = preprocess, processX = processX, processY = processY)
    #execfile("sup_ee_observed_varxy.py")
    
    pickle.dump(bootrec,open(outputFolder + '/varMean' + outputSuffix + '.p', 'wb'))
    
    #funcs.drawGraphs(bootrec, outfolder, windowSizes1, windowSizes2)
    
    print
    print

if __name__ == "__main__":
    main(datafile, outputFolder, outputSuffix, iterations, epochmult)