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
#from myLibs.parsers import *
#from myLibs.gilmoreStats import *
#from myLibs.fitting import *
#from myLibs.autoPeakFunk import *
from myLibs.QueryDB import OpenDatabase, GetIntensities2, CloseDatabase
#from myLibs.plotting import *

def NormIntensity(ListOpt):
    
    pathfile = os.path.realpath(__file__)
    pathfile = pathfile.strip('normintensity.py')
    List = ListOpt.copy()
    List.pop(0)
    
    try:
        conexion = OpenDatabase(pathfile)
    except:
        sys.stderr.write('------------------------------------------------------')
        sys.stderr.write('ERROR: Database cannot be read. Please, be sure that database is in the folder myDatabase.')
        sys.stderr.write('------------------------------------------------------')
        return 20
    for element in List:
        Isotope = GetIntensities2(conexion,element,order = 'ASC')
        if len(Isotope) == 0:
            print('\nThe isotope consulted is ' + element)
            print('The query did not give any result.')
        else:
            Eg , Ig , IgR , Parent = [],[],[],[]
            for Ele in Isotope:
                Eg.append(str(Ele[1])+' ('+str(Ele[2])+')')
                Ig.append(str(Ele[3])+' ('+str(Ele[4])+')')
                IgR.append(str(Ele[5]))
                Parent.append(Ele[6])
            pd.set_option('display.max_rows', None)#imprime todas las filas
            df = pd.DataFrame(list(zip(Eg,Ig,IgR,Parent)),columns=['Eg [keV]','Ig (%)','Normalized Intensities','Parent'])#crea  la tabla
            print('For the isotope ' + element + ' the gamma decays found are: \n')
            print(df) #imprime la tabla
            print('\n')

    CloseDatabase(conexion)
    return 0

