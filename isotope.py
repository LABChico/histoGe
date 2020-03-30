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
#from myLibs.parsers import *
#from myLibs.gilmoreStats import *
#from myLibs.fitting import *
#from myLibs.autoPeakFunk import *
from myLibs.QueryDB import OpenDatabase, LookForElement, CloseDatabase
#from myLibs.plotting import *

def isotopeFun(ListOpt):
    
    pathfile = os.path.realpath(__file__)
    pathfile = pathfile.strip('isotope.py')
    List = ListOpt.copy()
    List.pop(0)
    
    try:
        conexion = OpenDatabase(pathfile)
    except:
        print('------------------------------------------------------')
        print('ERROR: Database cannot be read. Please, be sure that database is in the folder myDatabase.')
        print('------------------------------------------------------')
        return 20
    for element in List:
        Isotope = LookForElement(conexion,element,order = 'ASC')
        if len(Isotope) == 0:
            print('\nThe isotope consulted is ' + element)
            print('The query did not give any result.')
        else:
            Eg , Ig , Decay, Half , Parent = [],[],[],[],[]
            for Ele in Isotope:
                Eg.append(str(Ele[1])+' ('+str(Ele[2])+')')
                Ig.append(str(Ele[3])+' ('+str(Ele[4])+')')
                Decay.append(Ele[5])
                Half.append(str(Ele[6]) +' ' +str(Ele[7]) + ' ('+str(Ele[8])+')')
                Parent.append(Ele[10])
            pd.set_option('display.max_rows', None)#imprime todas las filas
            df = pd.DataFrame(list(zip(Eg,Ig,Decay,Half,Parent)),columns=['Eg [keV]','Ig (%)','Decay mode','Half Life','Parent'])#crea  la tabla
            print('For the isotope ' + element + ' the gamma decays found are: \n')
            print(df) #imprime la tabla
            print('\n')

    CloseDatabase(conexion)
    return 0

