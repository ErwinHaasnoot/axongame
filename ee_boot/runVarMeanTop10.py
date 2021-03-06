#Import modules
import pickle
import numpy as np
import utils.funcs as funcs

#Import project files
import utils.bootstrap as bs
import utils.observed as os

def main(datafile = '../data_by_cookie_slim.json', outputFolder = '.', outputSuffix = '', iterations = 10, epochmult = 4):
    #Load data
    print 'Running analysis of variance vs mean correlation top10'
    outextension = '/varMeanTop10'
    outputFolder = outputFolder + outextension
    data = funcs.loadData(datafile)
    funcs.ensurePath(outputFolder)
    print 'iterations: {}\noutput folder: {}\n'.format(iterations,outputFolder)
    
    print "OBSERVED DATA"
    os.runObs(data, outputFolder, rankFilter=90)
    
    print "BOOTSTRAP"
    bs.runBoot(data, iterations, outputFolder, rankFilter = 90)
    
    print
    print
    
    return outextension

if __name__ == "__main__":
    main(datafile, outputFolder, outputSuffix, iterations, epochmult)