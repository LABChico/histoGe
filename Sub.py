import sys
import os.path
#from os.path import basename
#import re
#import pandas as pd #para imprimir en forma de tabla
#from matplotlib import pyplot as plt
#import numpy as np
#from scipy.optimize import curve_fit
#from scipy import asarray as ar,exp
#from math import sqrt, pi
#import time
#import signal
#import keyboard

# mainPath=sys.path[0] # sources dir
from myLibs.parsers import isValidSpecFile,functionDict,getDictFromMCA,getDictFromSPE,getDictFromGammaVision
from myLibs.miscellaneus import WriteOutputFile, WritehgeFile
from myLibs.plotting import simplePlot
#from myLibs.gilmoreStats import *
#from myLibs.fitting import *
#from myLibs.autoPeakFunk import *
#from myLibs.QueryDB import *
#from myLibs.plotting import *
from myLibs.miscellaneus import getSubstractedList, getRebinedList,getRescaledList
def SubFun(ListOpt):
    List = ListOpt.copy()
    List.pop(0)
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
    if '--rebin' in List:
        rebinFlag = True
        List.remove('--rebin')
        rebinNum = None
        for Arg in List:
            try:
                rebinNum = float(Arg)
                break
            except:
                continue
        if rebinNum == None:
            return 64

    else:
        rebinFlag = False

    FileName1 = List[0]
    FileName2 = List[1]
    if len(List) == 0:
        sys.stderr.write('ERROR: "-r" option needs 2 arguments: File1 and File2, which will be substracted to File1.')
        return 60

    if not os.path.isfile(FileName1):
        sys.stderr.write("ERROR: %s does not exist.\n"%(FileName1))
        return 61
    
    if not os.path.isfile(FileName2):
        sys.stderr.write("ERROR: %s does not exist.\n"%(FileName2))
        return 62
    File1Ext = FileName1.split('.')[-1]
    File2Ext = FileName2.split('.')[-1]
    if  File1Ext != File2Ext:
        sys.stderr.write("Errror: background substraction needs the same extension as the main file. (for now)")
        return 65

    if noCalFlag:
        File1Dict = functionDict[File1Ext](FileName1,False)
        File2Dict = functionDict[File2Ext](FileName2,False)
    else:
        File1Dict = functionDict[File1Ext](FileName1)
        File2Dict = functionDict[File2Ext](FileName2)

    if rebinFlag:
        File1Dict["theRebinedList"]=getRebinedList(File1Dict["theList"],rebinNum)
        File2Dict["theRebinedList"]=getRebinedList(File2Dict["theList"],rebinNum)
        myLen1 = len(File1Dict["theRebinedList"][1])
        myLen2 = len(File2Dict["theRebinedList"][1])
    else:
        myLen1 = len(File1Dict["theList"][1])
        myLen2 = len(File2Dict["theList"][1])

    if myLen1 != myLen2:
        sys.stderr.write("ERROR: histograms do not have the same length and histoGe cannot continue.\n")
        return 63

    time1=File1Dict["expoTime"]
    time2=File2Dict["expoTime"]
    tRatio=time1/time2
    rescaledList=getRescaledList(File2Dict['theList'],tRatio)
    subsTractedL=getSubstractedList(File1Dict['theList'],rescaledList)

    Title = FileName1.split('/')[-1].rstrip('.' + File1Ext) + '-' +FileName2.split('/')[-1].rstrip('.' + File2Ext)
    IdFile = FileName1.rfind('/')
    myOutFile = FileName1[:IdFile+1] + Title + '.txt'
    
    if not noPlotFlag:
        simplePlot(subsTractedL,logFlag,noCalFlag,Label=None,show=True,Title=Title)
    if wofFlag:
        try:
            WritehgeFile(myOutFile,subsTractedL)
            print('-----------------------------------------')
            print('The file was saved as:')
            print(myOutFile)
            print('-----------------------------------------')
        except:
            try:
                WriteOutputFile(subsTractedL,myOutFile,Title)
                print('-----------------------------------------')
                print('The file was saved as:')
                print(myOutFile)
                print('-----------------------------------------')
            except IOError:
                sys.stderr.write('An unexpected error ocurred while saving the data to file.\n')
                return 66
               
    return 0
