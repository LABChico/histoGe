#import sys
import os.path
#from os.path import basename
#import re
import pandas as pd #para imprimir en forma de tabla
#from matplotlib import pyplot as plt
#import numpy as np
#from scipy.optimize import curve_fit
#from scipy import asarray as ar,exp
#from math import sqrt, pi
#import time
#import signal
#import keyboard

# mainPath=sys.path[0] # sources dir
from myLibs.parsers import getDictFromInfoFile
from myLibs.miscellaneus import getIdxRangeVals, WriteOutputFileRR
#from myLibs.gilmoreStats import *
#from myLibs.fitting import *
#from myLibs.autoPeakFunk import *
from myLibs.QueryDB import OpenDatabase, CloseDatabase, EnergyRange, halfLifeUnit
#from myLibs.plotting import *
import sys

def energyFun(ListOpt):
    List = ListOpt.copy()
    List.pop(0)  
    
    if '--wof' in List:
        wofFlag = True
        List.remove('--wof')
    else:
        wofFlag = False

    if '--all' in List:
        allFlag = True
        List.remove('--all')
    else:
        allFlag = False

    if len(List) == 0:
        sys.stderr.write("error: --energyRanges option needs an argument\n")
        return 0
    
    infoFile=List[0]
    if not os.path.isfile(infoFile):
        sys.stderr.write("error: %s does not exist, are you in the right path?\n" %(infoFile))
        return False
    if not infoFile.endswith('.info'):
        sys.stderr.write("error: %s needs a .info extension\n" % (infoFile))
        return False
    infoDict=getDictFromInfoFile(infoFile)
    del infoDict['Range']
    idxPairL = []
    for DictEle in infoDict.values():
        idxPairL.append([DictEle['start'],DictEle['end']])
    #Energy range of the histogram
    
    DBInfoL = []
    pathfile = os.path.realpath(__file__)
    pathfile = pathfile.strip('energy.py')
    conexion = OpenDatabase(pathfile)
    for idxR in idxPairL:
        iEner = idxR[0]
        fEner = idxR[1]
        DBInfoL.append(EnergyRange(conexion,iEner,fEner))
        DBInfo = DBInfoL[-1]

        print('\nThe energy range consulted is between %.2f keV and %.2f keV.\n' % (iEner,fEner))
        Eg , Ig , Decay, Half , Parent = [],[],[],[],[]
        for Ele in DBInfo:
            Eg.append(str(Ele[1])+' ('+str(Ele[2])+')')
            Ig.append(str(Ele[3])+' ('+str(Ele[4])+')')
            Decay.append(Ele[5])
            Half.append(halfLifeUnit(Ele))
            Parent.append(Ele[10])

        if allFlag:
            pd.set_option('display.max_rows', None)
        else:
            pd.set_option('display.max_rows', len(Ele))

        df = pd.DataFrame(list(zip(Eg,Ig,Decay,Half,Parent)),columns=['Eg [keV]','Ig (%)','Decay mode','Half Life (s)','Parent'])
        if allFlag:
            print(df)
        else:
            print(df.head(10))

        if wofFlag:
            try:
                myfilename = infoFile.strip('.info') + '_energyRanges.txt'
                WriteOutputFileRR(myfilename,df,iEner,fEner)
                print('-----------------------------------------')
                print('The file was saved as:')
                print(myfilename)
                print('-----------------------------------------')
            except IOError:
                sys.stderr.write('ERROR: An unexpected error ocurrs. Data could not be saved.\n')
            

    CloseDatabase(conexion)
    return 0