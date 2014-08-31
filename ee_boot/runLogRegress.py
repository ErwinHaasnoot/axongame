#Import modules
import pickle
import numpy as np

import utils.funcs as funcs

#Import project files
import utils.bootstrap as bs
import utils.observed as os

def main(datafile = '../data_by_cookie_slim.json', outputFolder = '.', outputSuffix = '', iterations = 10, epochmult = 4):
    #Load data
    print 'Running log regression analysis of variance vs mean, 1st order'
    outextension = '/logRegress'
    outputFolder = outputFolder + outextension
    
    funcs.ensurePath(outputFolder)
    print 'iterations: {}\noutput folder: {}\n'.format(iterations,outputFolder)
    data = funcs.loadData(datafile)
    #Process X = polyfit regression test
    processX = lambda x,x_plays: np.polyfit(x_plays, x, 1, full = True)[1]
    #Preprocessing = taking logarithm of all data points
    preprocess = lambda x: [np.log(k) for k in x]
    
    print "OBSERVED DATA"
    os.runObs(data, outputFolder, preprocess = preprocess, processX = processX)
    
    print "BOOTSTRAP"
    bs.runBoot(data, iterations, outputFolder, preprocess = preprocess, processX = processX)
    
    print
    print
    
    return outextension
    
    

if __name__ == "__main__":
    main()