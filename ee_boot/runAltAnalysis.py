#Import modules
import pickle
import numpy as np
import utils.funcs as funcs

#Import project files
import utils.bootstrap as bs
import utils.observed as os

def main(datafile = 'data_by_cookie_slim.json', outputFolder = 'testAnalysis', outputSuffix = 'test', iterations = 10, epochmult = 4):
    #Load data
    print 'Running analysis of Alternative thing, 1st order'
    outextension = '/altBoot'
    outputFolder = outputFolder + outextension
    funcs.ensurePath(outputFolder)
    data = funcs.loadData(datafile)
    print 'iterations: {}\noutput folder: {}\n'.format(iterations,outputFolder)
    
    def processX(x, x_plays):
        f = np.vectorize(lambda x: 1 if x > 0 else -1, otypes=[np.float]) 
        a = np.mean(f(np.diff(x, axis = 0)),axis=0)
        #print f(np.diff(x, axis = 0))[0]
        
        return a
    
    print "OBSERVED DATA"
    os.runObs(data, outputFolder, processX = processX)
    
    print "BOOTSTRAP"
    bs.runBoot(data, iterations, outputFolder, processX = processX)
    
    print
    print
    
    return outextension

if __name__ == "__main__":
    main()