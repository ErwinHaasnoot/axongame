#savefig('explore_exploit_scatterheatmap.png', dpi=300, facecolor='w', edgecolor='w',
#        orientation='portrait', papertype=None, format=None,
#        transparent=False, bbox_inches='tight', pad_inches=0.1) 
import sys
import os
import utils.funcs as funcs

dataFile = 'data_by_cookie.json'
outFolder = 'fullTestRun'
iterations = 100
epochmult = 40

funcs.ensurePath(outFolder)

#Run perceptron analysis
import ee_binaryclass.runPerceptronArtificial as runPerceptronArt
runPerceptronArt.main(dataFile, outFolder, iterations, epochmult)
import ee_binaryclass.runPerceptronReal as runPerceptron
runPerceptron.main(dataFile, outFolder, iterations, epochmult)

#Run MLP analysis 
import ee_binaryclass.runMLP as runMLP
runMLP.main(dataFile, outFolder, iterations, epochmult)

#Run local/global quit analysis with MLP
import ee_binaryclass.lgquit_MLP as lgquit_MLP
lgquit_MLP.main(dataFile, outFolder, iterations, epochmult)


import ee_boot.runRegressMean as runRegressMean
runRegressMean.main(dataFile, outFolder, iterations*10, epochmult)

import ee_boot.runVarMean as runVarMean
runVarMean.main(dataFile, outFolder, iterations*10, epochmult)

import ee_boot.runVarMeanTop10 as runVarMeanTop10
runVarMeanTop10.main(dataFile, outFolder, iterations*10, epochmult)

import ee_boot.runLogVarMean as runLogVarMean
runLogVarMean.main(dataFile, outFolder, iterations*10, epochmult)

#Create graphs
import graphs.ee_bootGraphs as ee_bootGraphs
ee_bootGraphs.main(dataFile, outFolder, iterations, epochmult)
