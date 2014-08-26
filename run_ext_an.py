#savefig('explore_exploit_scatterheatmap.png', dpi=300, facecolor='w', edgecolor='w',
#        orientation='portrait', papertype=None, format=None,
#        transparent=False, bbox_inches='tight', pad_inches=0.1) 
import sys
import os
import utils.funcs as funcs

dataFile = 'data_by_cookie_slim.json'
outputFolder = 'analysis1'
outputSuffix = '_run1'
iterations = 2
epochmult = 40
#sys.argv = [dataFile, outputFolder, outputSuffix, iterations, epochmult]

funcs.ensurePath(outputFolder)

# #Run perceptron analysis
# import ee_binaryclass.runPerceptron as runPerceptron
# runPerceptron.main(dataFile, outputFolder, outputSuffix, iterations, epochmult)

# #Run MLP analysis 
# import ee_binaryclass.runMLP as runMLP
# runMLP.main(dataFile, outputFolder, outputSuffix, iterations, epochmult)

# #Run local/global quit analysis with MLP
# import ee_binaryclass.lgquit_MLP as lgquit_MLP
# lgquit_MLP.main(dataFile, outputFolder, outputSuffix, iterations, epochmult)

# funcs.ensurePath(outputFolder + '/logRegress')
# funcs.ensurePath(outputFolder + '/varMean')

# import ee_boot.runLogRegress as runLogRegress
# runLogRegress.main(dataFile, outputFolder, outputSuffix, iterations, epochmult)

# import ee_boot.runVarMean as runVarMean
# runVarMean.main(dataFile, outputFolder, outputSuffix, iterations, epochmult)

#Create graphs
import graphs.ee_bootGraphs as ee_bootGraphs
ee_bootGraphs.main(dataFile, outputFolder, outputSuffix, iterations, epochmult)