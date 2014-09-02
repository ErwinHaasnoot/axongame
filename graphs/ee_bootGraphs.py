#Import relevant modules

import utils.funcs as funcs
#Draw graphs for logRegress
def main(datafile = '../data_by_cookie_slim.json', outputFolder = '.', iterations = 10, epochmult = 4):
    
    #Set windowsizes
    windowSizes1 = range(5,30,5)    # Sizes of attempt group 1
    windowSizes2 = range(5,30,5)    # Sizes of attempt group 2
    
    #Draw logregress graph
    funcs.ensurePath(outputFolder + '/figures')
    funcs.drawGraphs(outputFolder, 'logVarMean', windowSizes1, windowSizes2,zBottom = -.3, zTop = .3)
    funcs.drawGraphs(outputFolder, 'varMeanTop10', windowSizes1, windowSizes2)
    funcs.drawGraphs(outputFolder, 'varMean', windowSizes1, windowSizes2)
    funcs.drawGraphs(outputFolder, 'regressMean', windowSizes1, windowSizes2)
    
    funcs.drawPerceptronWeights(outputFolder, 'runPerceptronReal')
    funcs.drawPerceptronWeights(outputFolder, 'runPerceptronArtificial')
if __name__ == "__main__":
    main()