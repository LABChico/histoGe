import sys
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
#from myLibs.parsers import getDictFromInfoFile
#from myLibs.miscellaneus import getIdxRangeVals, WriteOutputFileRR
#from myLibs.gilmoreStats import *
#from myLibs.fitting import *
#from myLibs.autoPeakFunk import *
from myLibs.QueryDB import OpenDatabase, CloseDatabase, GetChainAndChild, GetMainChain
#from myLibs.plotting import *

def Parent(ListOpt):
    List = ListOpt.copy()
    List.pop(0)  
    
    if len(List) == 0:
        sys.stderr.write("error: --parent option needs an argument\n")
        return 400
    
    pathfile = os.path.realpath(__file__)
    pathfile = pathfile.strip('isoparent.py')
    conexion = OpenDatabase(pathfile)

    for Isotope in List:
        MainChainIso,Child = GetChainAndChild(conexion,Isotope)
        if MainChainIso == None or Child == None:
        
            print('Isotope: ' + Isotope + ' -- Parent: ' + 'None' + ' --Child: ' + 'None' +  '\n')
            print('There is not enough information in the database or the isotope ' + Isotope + ' do not have Child or parents isotopes. \n')
        
        else:
        
            MainChain = GetMainChain(conexion,MainChainIso)
            if '+' in MainChain:
                AuxStr = MainChain.split('+')[1]
                Parentiso = AuxStr.split('#')[0]
            else:
                Parentiso = MainChain[0].split('#')[0]

            print('Isotope: ' + Isotope + ' -- Parent: ' + Parentiso + ' --Child: ' + Child + '\n')
        
    CloseDatabase(conexion)
    return 0