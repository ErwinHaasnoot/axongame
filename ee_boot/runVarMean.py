#Import modules
import pickle
import numpy as np
import utils.funcs as funcs

#Import project files
import utils.bootstrap as bs
import utils.observed as os

def main(datafile = '../data_by_cookie_slim.json', outputFolder = '.', outputSuffix = '', iterations = 10, epochmult = 4):
    #Load data
    print 'Running analysis of variance vs mean correlation'
    outextension = '/varMean'
    outputFolder = outputFolder + outextension
    funcs.ensurePath(outputFolder)
    data = funcs.loadData(datafile)
    print 'iterations: {}\noutput folder: {}\n'.format(iterations,outputFolder)
    
    print "OBSERVED DATA"
    os.runObs(data, outputFolder)
    
    print "BOOTSTRAP"
    bs.runBoot(data, iterations, outputFolder)
    
    print
    print
    
    return [outextension]

if __name__ == "__main__":
    main(datafile, outputFolder, outputSuffix, iterations, epochmult)