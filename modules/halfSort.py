import sys
import os.path
import pandas as pd 
from myLibs.parsers import getDictFromInfoFile
from myLibs.miscellaneus import getIdxRangeVals
from myLibs.miscellaneus import WriteOutputFileRR

from myLibs.QueryDB import OpenDatabase, CloseDatabase, EnergyRange, halfLifeUnit, GetIntensities


def halfSortFun(ListOpt):
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
        return 100
    if not infoFile.endswith('.info'):
        sys.stderr.write("error: %s needs a .info extension\n" % (infoFile))
        return 101
    infoDict=getDictFromInfoFile(infoFile)
    minRange = infoDict['Range']['start']
    maxRange = infoDict['Range']['end']
    del infoDict['Range']

    idxPairL = []
    for DictEle in infoDict.values():
        idxPairL.append([DictEle['start'],DictEle['end']])

    DBInfoL = []
    DBInfoDL = []
    pathfile = os.path.realpath(__file__)
    pathfile = pathfile.replace('/modules/halfSort.py','')
    conexion = OpenDatabase(pathfile)

    for idxR in idxPairL:
        iEner = idxR[0]
        fEner = idxR[1]
        DBInfoL.append(GetIntensities(conexion,iEner,fEner))
        DBInfo = DBInfoL[-1]
        DBInfoD = {}
        for e in DBInfo: 
            #Filling dict with isotope name each isotope has only one tupple
            DBInfoD[e[-1]] = e    
    
        Eg , Ig , Decay, Half , Parent= [],[],[],[],[]
        for Element in DBInfoD:
            Eg.append(str(DBInfoD[Element][1])+' ('+str(DBInfoD[Element][2])+')')
            Ig.append(round(DBInfoD[Element][3],2))
            Decay.append(DBInfoD[Element][5])
            x=halfLifeUnit(DBInfoD[Element])
            if x == 0:
                y = str(x)

            else:
                y = str('{0:.2e}'.format(x))
            
            Half.append(y+ ' [s] ')
            Parent.append(DBInfoD[Element][-1])
        
        print('\nThe energy range consulted is between %.2f keV and %.2f keV.\n' % (iEner,fEner))
        
        if allFlag:
            pd.set_option('display.max_rows', None) 
            pd.options.display.float_format = '{:,.5f}'.format
            df = pd.DataFrame(sorted(list(zip(Eg,Ig,Decay,Half,Parent)), key = lambda x: float(x[3][:-4]), reverse=True),columns=['Eg [keV]','Ig (%)','Decay m','Half Life','Parent'])#crea  la tabla
            print(df)
        else:
            pd.set_option('display.max_rows', None)
            df = pd.DataFrame(sorted(list(zip(Eg,Ig,Decay,Half,Parent)), key = lambda x: float(x[3][-4]), reverse=True),columns=['Eg [keV]','Ig (%)','Decay m','Half Life','Parent'])#crea  la tabla
            print(df.head(10))
            
            

        if wofFlag:
            try:
                myfilename = infoFile.strip('.info') + '_rank_C.txt'
                if allFlag:
                    WriteOutputFileRR(myfilename,df,iEner,fEner)
                else:
                    WriteOutputFileRR(myfilename,df.head(10),iEner,fEner)
                
                print('-----------------------------------------')
                print('The file was saved as:')
                print(myfilename)
                print('-----------------------------------------')        
            

            except IOError:
                sys.stderr.write('ERROR: An unexpected error ocurrs. Data could not be saved.\n')
                break
    
            
    
    return 0


