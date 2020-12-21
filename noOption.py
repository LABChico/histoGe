import sys
#import os.path
#from os.path import basename
#import re
#import pandas as pd #para imprimir en forma de tabla
from matplotlib import pyplot as plt
#import numpy as np
#from scipy.optimize import curve_fit
#from scipy import asarray as ar,exp
#from math import sqrt, pi
#import time
#import signal
#import keyboard

# mainPath=sys.path[0] # sources dir
from energy import energyFun
from myLibs.parsers import isValidSpecFile, functionDictAdv, getDictFromGammaVision,getDictFromMCA,getDictFromSPE
from myLibs.plotting import simplePlot
#from myLibs.gilmoreStats import *
#from myLibs.fitting import *
#from myLibs.autoPeakFunk import *
#from myLibs.QueryDB import *
#from myLibs.plotting import *
from Help import helpFun
from myLibs.miscellaneus import getRebinedList

def noOption(ListOpt):
    List = ListOpt.copy()
    if '--log' in List:
        logFlag = True
        List.remove('--log')
    else:
        logFlag = False

    if '--noCal' in List:
        noCalFlag = True
        List.remove('--noCal')
    else:
        noCalFlag = False

    if '--rebin' in List:
        rebinFlag = True
        List.remove('--rebin')
        rebinNum = None
        for Arg in List:
            try:
                rebinNum = int(Arg)
                List.remove(Arg)
                break
            except:
                continue
    else:
        rebinFlag = False

    ListAux = List
    for arg in ListAux:
        if arg[0] == '-':
            List.remove(arg)

    plotFlag = False
    exitcode = 0

    if len(ListOpt) == 0:
        exitcode = helpFun(['None'],['.Txt','.SPE','.mca','.info'],extBool=False)
        return exitcode
    else:
        for arg in List:
            if isValidSpecFile(arg):
                if arg.endswith('.info'):
                    exitcode = energyFun(['--energyRanges',arg])
                
                try:
                    if isValidSpecFile(arg):
                        FileExt = arg.split('.')[-1]
                except:
                    sys.stderr.write('ERROR: Unexpected error. Not a valid file used.')
                    return 110

                ######
                if rebinFlag:
                    FileDict = functionDictAdv[FileExt](arg)
         
                    if isinstance(rebinNum, int) == False:
                        rebinNum=5
                        sys.stderr.write("There was no rebin integer detected, the default rebin value used was 5")
                

                    if "theRebinedList" not in FileDict:
                        FileDict["theRebinedList"]=getRebinedList(FileDict["theList"],rebinNum)
                        myDataList = FileDict["theRebinedList"]
                        myDataList[0] = list(myDataList[0])
                        myDataList[1] = list(myDataList[1])
                               
                    else:
                        sys.stderr.write("There was no rebin option detected, the rebin option is --rebin")
                        #myDataList = FileDict['theList']
                    
                    myFilename = arg
                    mySubsList=myDataList
                    plotFlag = True
                    simplePlot(mySubsList,logFlag,FileDict['calBoolean'],Label=None,show=False,Title=myFilename,ExpoTime=FileDict['expoTime'])
                    
                ######  
                else:
                    # SPE no funciona con estas condiciones
                    # if not noCalFlag and mySubsDict['calBoolean']:
                    #     mySubsDict = functionDictAdv[myExtension](myFilename,noCalFlag=False)
                    # else:
                    #     mySubsDict = functionDictAdv[myExtension](myFilename,noCalFlag=True)
                    myFilename = arg
                    myExtension = myFilename.split(".")[-1]
                    mySubsDict = functionDictAdv[myExtension](myFilename)
                    mySubsList = mySubsDict["theList"]
                    plotFlag = True
                    simplePlot(mySubsList,logFlag,mySubsDict['calBoolean'],Label=None,show=False,Title=myFilename,ExpoTime=mySubsDict['expoTime'])
            else:
                sys.stderr.write('WARNING: The file ' + arg + ' is invalid. Nothing to do with it.')
                return 90
    if plotFlag:
        plt.show()
    return 0
