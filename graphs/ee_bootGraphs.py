#Import relevant modules

import utils.funcs as funcs
import pickle
#Draw graphs for logRegress
def main(datafile = '../data_by_cookie_slim.json', outputFolder = '.', bootFolders = '', iterations = 10, epochmult = 4):
    
    
    #Set windowsizes
    windowSizes1 = range(5,30,5)    # Sizes of attempt group 1
    windowSizes2 = range(5,30,5)    # Sizes of attempt group 2
    
    #Draw logregress graph
    
    for folder in bootFolders:
        bootrec = pickle.load(open(outputFolder + '/' + folder + 'bootrec.p','rb'))
        funcs.drawGraphs(bootrec, outputFolder, folder, windowSizes1, windowSizes2)

if __name__ == "__main__":
    main(datafile, outputFolder, outputSuffix, iterations, epochmult)