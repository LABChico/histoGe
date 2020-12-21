import sys
#import os.path
#from os.path import basename
#import re
import pandas as pd #para imprimir en forma de tabla
from matplotlib import pyplot as plt
import numpy as np
#from scipy.optimize import curve_fit
#from scipy import asarray as ar,exp
#from math import sqrt, pi
#import time
#import signal
#import keyboard

# mainPath=sys.path[0] # sources dir
from myLibs.parsers import getDictFromSPE,getDictFromMCA,getDictFromGammaVision,isValidSpecFile,getDictFromInfoFile,functionDict
from myLibs.miscellaneus import WriteOutputFile, WritehgeFile
from myLibs.plotting import simplePlot
#from myLibs.gilmoreStats import *
#from myLibs.fitting import *
#from myLibs.autoPeakFunk import *
#from myLibs.QueryDB import *
#from myLibs.plotting import *

def SumSpectra(Dict1,Dict2):
    if not(Dict1['calBoolean'] != Dict2['calBoolean']):
        
        if Dict1['calBoolean'] is False:
            Y1 = np.array(Dict1['theList'][1])
            Y2 = np.array(Dict2['theList'][1])
            Yout = Y1 + Y2
            Dict2['theList'][1] = list(Yout) 
        else:
            X1 = np.array(Dict1['theList'][0])
            X2 = np.array(Dict2['theList'][0])
            Y1 = np.array(Dict1['theList'][1])
            Y2 = np.array(Dict2['theList'][1])
            maxX = max(X1.max(),X2.max())
            minX = min(X1.min(),X2.min())
            DeltaX = max(abs(X1[1]-X1[0]),abs(X2[1]-X2[0]))
            Xaux = np.arange(minX,maxX,DeltaX)
            Yaux = np.empty(Xaux.shape)
            for Xbin,Ybin in zip(X1,Y1):
                Yaux += np.logical_and((Xbin > (Xaux-(DeltaX/2))),(Xbin <= (Xaux+(DeltaX/2))))*Ybin
            for Xbin,Ybin in zip(X2,Y2):
                Yaux += np.logical_and((Xbin > (Xaux-(DeltaX/2))),(Xbin <= (Xaux+(DeltaX/2))))*Ybin
        Dict1['theList'][0] = Xaux
        Dict1['theList'][1] = Yaux
        return Dict1
    else:
        print('--------------------------------------------')
        sys.stderr.write('ERROR: All files must be calibrated or non-calibrated.\n')
        print('Sum cannot be performed between different types of files')
        print('--------------------------------------------')
        exit(43)
        pass

def SumFun(ListOpt):
    List = ListOpt.copy()
    List.pop(0)
    #functionDict = {"SPE": getDictFromSPE,"mca": getDictFromMCA,"Txt": getDictFromGammaVision,"info":getDictFromInfoFile}
    if '--noCal' in List:
        noCalFlag = True
        List.remove('--noCal')
    else:
        noCalFlag = False

    if '--noPlot' in List:
        noPlotFlag = True
        List.remove('--noPlot')
    else:
        noPlotFlag = False
    
    if '--wof' in List:
        wofFlag = True
        List.remove('--wof')
    else:
        wofFlag = False
    
    if '--log' in List:
        logFlag = True
        List.remove('--log')
    else:
        logFlag = False

    if len(List) == 1:
        if isValidSpecFile(List[0]):
            print('----------------------------------------------')
            sys.stderr.write('WARNING: At least two files are needed to make the sum between them.\nNo sum was performed. If option --noPlot is disabled then plot is shown.\n Otherwise, nothing is shown.\n')
            print('----------------------------------------------')
            myFilename = List[0]
            myExtension = myFilename.split(".")[-1]
            if noCalFlag:
                mySubsDict = functionDict[myExtension](myFilename,False)
            else:
                mySubsDict = functionDict[myExtension](myFilename)
            mySubsList = mySubsDict["theList"]
            if noPlotFlag:
                print('----------------------------------------------')
                sys.stderr.write('--noPlot is activated, so there is no figure display.\n')
            else:
                simplePlot(mySubsList,logFlag,noCalFlag,Label=None,show=True,Title=myFilename.split('/')[-1])
        else:
            print('----------------------------------------------')
            sys.stderr.write('WARNING: No .mca, .Txt or .SPE files was indicated.\nPlease, introduce two or more valid files.')
            return 41

    elif len(List) > 1:
        count = 0
        Title = ''
        for myFilename in List:
            count += 1
            Title += myFilename.split('/')[-1] + '+'
            if isValidSpecFile(myFilename):
                myExtension = myFilename.split(".")[-1]
            if noCalFlag:
                mySubsDict = functionDict[myExtension](myFilename,False)
                if count == 1:
                    mySubsDictOut = mySubsDict.copy()
            else:
                mySubsDict = functionDict[myExtension](myFilename)
                if count == 1:
                    mySubsDictOut = mySubsDict.copy()
            if count != 1:
                mySubsDictOut = SumSpectra(mySubsDictOut,mySubsDict)
            
        if not noPlotFlag:
            simplePlot(mySubsDictOut["theList"],logFlag,noCalFlag,Label=None,show=True,Title=Title[:-1])
        if wofFlag:
            myOutFile = myFilename.strip(myFilename.split('/')[-1]) + Title + '.txt'
            try:
                WritehgeFile(myOutFile,mySubsDictOut)
                print('-----------------------------------------')
                print('The file was saved as:')
                print(myOutFile)
                print('-----------------------------------------')
            except:
                try:
                    WriteOutputFile(mySubsDictOut,myOutFile,Title)
                    print('-----------------------------------------')
                    print('The file was saved as:')
                    print(myOutFile)
                    print('-----------------------------------------') 
                except IOError:
                    sys.stderr.write('An unexpected error ocurred while saving the data to file.\n')
                    return 44
                
                
                
    else:
        sys.stderr.write('ERROR: Not a valid argument in "Sum" function.\n')
        return 40

    return 0
