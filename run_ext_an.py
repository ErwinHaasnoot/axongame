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
epochmult = 4
sys.argv = [dataFile, outputFolder, outputSuffix, iterations, epochmult]

funcs.ensurePath(outputFolder)

#Run perceptron analysis
execfile('ee_binaryclass/runPerceptron.py')

#Run MLP analysis 
execfile('ee_binaryclass/runMLP.py')

#Run local/global quit analysis with MLP
execfile('ee_binaryclass/lgquit_MLP.py')

funcs.ensurePath(outputFolder + '/logRegress')
funcs.ensurePath(outputFolder + '/varMean')

execfile('ee_boot/runLogRegress.py')
execfile('ee_boot/runVarMean.py')

#Create graphs
#execfile('ext_an_graphs.py')