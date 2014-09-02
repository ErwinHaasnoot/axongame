#Import relevant modules

import utils.funcs as funcs
#Draw graphs for logRegress
def main(datafile = '../data_by_cookie_slim.json', outputFolder = '.', iterations = 10, epochmult = 4):
    
    bootFolders = ['logVarMean','varMeanTop10','varMean','regressMean','logVarMax','varMax']
    perceptrons = ['runPerceptronReal','runPerceptronArtificial']
    
    #Set windowsizes
    windowSizes1 = range(5,30,5)    # Sizes of attempt group 1
    windowSizes2 = range(5,30,5)    # Sizes of attempt group 2
    
    #Draw logregress graph
    funcs.ensurePath(outputFolder + '/figures')
    for folder in bootFolders:
        print 
        print
        print 'Drawing bootstrap graphs for: {}'.format(folder)
        print
        print
        funcs.drawGraphs(outputFolder, folder, windowSizes1, windowSizes2)
        
    for folder in perceptrons:
        print
        print
        print 'Drawing perceptron weight graphs for: {}'.format(folder)
        print
        print
        funcs.drawPerceptronWeights(outputFolder, folder)
if __name__ == "__main__":
    main()