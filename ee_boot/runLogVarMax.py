#Import modules
import pickle
import numpy as np

import utils.funcs as funcs

#Import project files
import utils.bootstrap as bs
import utils.observed as os

def main(datafile = '../data_by_cookie_slim.json', outputFolder = '.', outputSuffix = '', iterations = 10, epochmult = 4):
    #Load data
    print 'Running log variance vs max'
    outextension = '/logVarMax'
    outputFolder = outputFolder + outextension
    funcs.ensurePath(outputFolder)
    print 'iterations: {}\noutput folder: {}\n'.format(iterations,outputFolder)
    data = funcs.loadData(datafile)
    #Preprocessing = taking logarithm of all data points
    preprocess = lambda x: [np.log(k) for k in x]
    processY = lambda x,x_plays: np.amax(x,axis=0)
    print "OBSERVED DATA"
    os.runObs(data, outputFolder, preprocess = preprocess, processY = processY)
    
    print "BOOTSTRAP"
    bs.runBoot(data, iterations, outputFolder, preprocess = preprocess, processY = processY)
    
    print
    print
    
    
    return [outextension]
    
if __name__ == "__main__":
    main()