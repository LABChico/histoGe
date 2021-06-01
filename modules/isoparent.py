import sys
import os.path
import pandas as pd 
from myLibs.QueryDB import OpenDatabase, CloseDatabase, GetChainAndChild, GetMainChain
from myLibs.miscellaneus import operatingSystem
def Parent(ListOpt):
    List = ListOpt.copy()
    List.pop(0)  
    
    if len(List) == 0:
        sys.stderr.write("error: --parent option needs an argument\n")
        return 400
    
    pathfile = os.path.realpath(__file__)
    if operatingSystem == 'Linux' or operatingSystem == 'Darwin':
        pathfile = pathfile.replace('/modules/isoparent.py','')
    elif operatingSystem == 'Windows':
        pathfile = pathfile.replace('\\modules\\isoparent.py','')

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