#import sys
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
                else:
                    myFilename = arg
                    myExtension = myFilename.split(".")[-1]
                    mySubsDict = functionDictAdv[myExtension](myFilename)
                    # SPE no funciona con estas condiciones
                    # if not noCalFlag and mySubsDict['calBoolean']:
                    #     mySubsDict = functionDictAdv[myExtension](myFilename,noCalFlag=False)
                    # else:
                    #     mySubsDict = functionDictAdv[myExtension](myFilename,noCalFlag=True)
                    mySubsList = mySubsDict["theList"]
                    plotFlag = True
                    simplePlot(mySubsList,logFlag,mySubsDict['calBoolean'],Label=None,show=False,Title=myFilename,ExpoTime=mySubsDict['expoTime'])
            else:
                print('WARNING: The file ' + arg + ' is invalid. Nothing to do with it.')
                return 90
    if plotFlag:
        plt.show()
    return 0
