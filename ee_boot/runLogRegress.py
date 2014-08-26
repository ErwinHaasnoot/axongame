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
    outputFolder = outputFolder + '/logRegress'
    print 'iterations: {}\noutput folder: {}\n'.format(iterations,outputFolder)
    data = funcs.loadData(datafile)
    #properData  = [[data[k][l][0] for l in collections.OrderedDict(sorted(data[k].items()))] for k in data]
    #Process X = polyfit regression test
    processX = lambda x,x_plays: np.polyfit(x_plays, x, 1, full = True)[1]
    #Preprocessing = taking logarithm of all data points
    preprocess = lambda x: [np.log(k) for k in x]
    
    windowSizes1 = range(5,30,5)    # Sizes of attempt group 1
    windowSizes2 = range(5,30,5)    # Sizes of attempt group 2
    
    funcs.ensurePath(outputFolder)
    
    print "OBSERVED DATA"
    os.runObs(data, windowSizes1, windowSizes2, outputFolder, preprocess = preprocess, processX = processX)
    #execfile("sup_ee_boot_varxy.py")
    
    print "BOOTSTRAP"
    bootrec = bs.runBoot(data, iterations, windowSizes1, windowSizes2, preprocess = preprocess, processX = processX)
    
    pickle.dump(bootrec,open(outputFolder + '/logRegress' + outputSuffix + '.p', 'wb'))
    #execfile("sup_ee_observed_varxy.py")
    
    #funcs.drawGraphs(bootrec, outfolder, windowSizes1, windowSizes2)
    
    print
    print
    
    

if __name__ == "__main__":
    main(datafile, outputFolder, outputSuffix, iterations, epochmult)