#Import relevant modules

import utils.funcs as funcs
import pickle
#Draw graphs for logRegress
def main(datafile = '../data_by_cookie_slim.json', outputFolder = '.', outputSuffix = '', iterations = 10, epochmult = 4):
    
    
    #Set windowsizes
    windowSizes1 = range(5,30,5)    # Sizes of attempt group 1
    windowSizes2 = range(5,30,5)    # Sizes of attempt group 2
    
    #Draw logregress graph
    bootrec = pickle.load(open(outputFolder + '/logRegress/logRegress' + outputSuffix + '.p','rb'))
    funcs.drawGraphs(bootrec, outputFolder + '/logRegress', windowSizes1, windowSizes2, 'logRegress{}.png'.format(outputSuffix))
    
    #Draw varMean graph
    bootrec = pickle.load(open(outputFolder + '/varMean/varMean' + outputSuffix + '.p','rb'))
    funcs.drawGraphs(bootrec, outputFolder + '/logRegress', windowSizes1, windowSizes2,'varMean{}.png'.format(outputSuffix))

if __name__ == "__main__":
    main(datafile, outputFolder, outputSuffix, iterations, epochmult)