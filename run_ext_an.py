#savefig('explore_exploit_scatterheatmap.png', dpi=300, facecolor='w', edgecolor='w',
#        orientation='portrait', papertype=None, format=None,
#        transparent=False, bbox_inches='tight', pad_inches=0.1) 
import sys
import os

dataFile = 'data_by_cookie_slim.json'
outputFolder = 'analysis1'
outputSuffix = '_run1'
sys.argv = [dataFile, outputFolder, outputSuffix]

if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

#Run perceptron analysis
execfile('ee_binaryclass/runPerceptron.py')

#Run MLP analysis 
execfile('ee_binaryclass/runMLP.py')

#Run local/global quit analysis with MLP
execfile('ee_binaryclass/lgquit_MLP.py')