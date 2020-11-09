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
#from myLibs.miscellaneus import getIdxRangeVals, WriteOutputFileRR
#from myLibs.gilmoreStats import *
#from myLibs.fitting import *
#from myLibs.autoPeakFunk import *
from myLibs.QueryDB import OpenDatabase, CloseDatabase, GetChainAndChild, GetMainChain, EnergyRange, halfLifeUnit, GetIntensities, chaintoList
#from myLibs.plotting import *
from myLibs.miscellaneus import WriteOutputFileRR
from myLibs.parsers import getDictFromInfoFile
from myLibs.miscellaneus import getIdxRangeVals
from myLibs.QueryDB import OpenDatabase, CloseDatabase, EnergyRange, halfLifeUnit, GetIntensities

def ChainRankFun(ListOpt):
    List = ListOpt.copy()
    List.pop(0)  
    i = 0 #for rank op
    #rankOp = []
    
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

    if '--peak' in List:
        addFlag = True
        List.remove('--peak')
        xId = -2
    else:
        addFlag = False
        xId = -1

    # for Arg in List:
    #     try:
    #         rankOp.append(int(Arg))
    #         if rankOp[i] > 0 and rankOp[i] < 4:
                
    #             if type(rankOp[i]) == int:
    #                 i += 1
            
    #         #break
    #     except:
    #         rankOp.append(3)
    #         continue   

    if len(List) == 0:
        print("error: --Rank option needs an argument")
        return 0

    infoFile=List[0]
    if not os.path.isfile(infoFile):
        print("error: %s does not exist, are you in the right path?" %(infoFile))
        return 100
    if not infoFile.endswith('.info'):
        print("error: %s needs a .info extension" % (infoFile))
        return 101
    infoDict=getDictFromInfoFile(infoFile)
    minRange = infoDict['Range']['start']
    maxRange = infoDict['Range']['end']
    del infoDict['Range']

    idxPairL = []
    for DictEle in infoDict.values():

        # if addFlag :
        #     if rankOp[2] == 1:
        #         rankSort = 'Rank'
                
        #         idxPairL.append([DictEle['start'],DictEle['end']])
            
        #     elif rankOp[2] == 2:
        #         rankSort = 'Rank2'
                
        #         idxPairL.append([DictEle['start'],DictEle['end']])
                
            
        #     elif rankOp[2] == 3:
        #         rankSort = 'Rank3'
                
        #         idxPairL.append([DictEle['start'],DictEle['end']])
            
        #     else:
        #         idxPairL.append([DictEle['start'],DictEle['end']])
        #         print('theres n|o rank op {}, please try an option between 1 and 3'.format(rankOp))
        #         break
        # else:
        #     rankSort = 'Rank3'
            
        idxPairL.append([DictEle['start'],DictEle['end']])
        
    
    DBInfoL = []
    pathfile = os.path.realpath(__file__)
    pathfile = pathfile.rstrip('chainRank.py')
    conexion = OpenDatabase(pathfile)
    
    ChainDict = {}

    memoLenDict={}
    isoPeakLL = []
    isoCountD = {}
    DBInfoL = []
    DBInfoDL = []
    #tMinE,tMaxE = infoDict['theList'][0],infoDict['theList'][-1]
    tMinEL = []
    tMaxEL = []
    
    if True:
        for infoPair in infoDict.values():
            tMinEL.append(infoPair['start'])
            tMaxEL.append(infoPair['end'])
        tMinE = min(tMinEL)
        tMaxE = max(tMaxEL)
    else:
        tMinE = minRange
        tMaxE = maxRange


    for idxR in idxPairL:
        iEner = idxR[0]
        fEner = idxR[1]
        #DBInfoL.append(EnergyRange(conexion,iEner,fEner))
        DBInfoL.append(GetIntensities(conexion,iEner,fEner))
        DBInfo = DBInfoL[-1]
        DBInfoD = {}
        for e in DBInfo: 
            #Filling dict with isotope name each isotope has only one tupple
            DBInfoD[e[-1]] = e      
        DBInfoDL.append(DBInfoD)   
        isoPeakL = []
        for Ele in DBInfo:
            iso = Ele[-1]
            if [iso,1,0,0] not in isoPeakL:
                isoPeakL.append([iso,1,0,Ele[10]]) #So that there is only one count of each isotope per peak
                if iso not in isoCountD: #Considering the number of entries in the energy range of the histogram
                    if iso not in memoLenDict:
                        #memoLenDict[iso]=len(EnergyRange(conexion,tMinE,tMaxE,iso))
                        memoLenDict[iso]=len(GetIntensities(conexion,tMinE,tMaxE,iso))
                    nInRange=memoLenDict[iso]
                    isoCountD[iso] = [0,nInRange,0]
                isoCountD[iso][0] += 1
            
            MainChainIso, _ = GetChainAndChild(conexion,Ele[-1])
            if MainChainIso not in ChainDict and MainChainIso is not None:
                ChainDict[MainChainIso] = [chaintoList(GetMainChain(conexion,MainChainIso)[0]),[0,0]]
              

        isoPeakLL.append(isoPeakL)

    IgRDict = {}

    for DBInfo in DBInfoL:
        for Ele in DBInfo:
            iso = Ele[-1]
            if iso not in IgRDict:
                IgRDict[iso] = Ele[10]
            else:
                IgRDict[iso] += Ele[10]

    for isoLL in isoPeakLL:
        for isoL in isoLL:
            iso = isoL[0]
            isoC = isoCountD[iso][0]
            isoL[1] = isoC
            isoL[2] = isoC/isoCountD[iso][1]
            isoCountD[iso][2] += isoL[-1]
            isoL[3] = IgRDict[iso]

    for keyChain in ChainDict.keys():
        for chainList in ChainDict[keyChain][0]:
            try:
                ChainDict[keyChain][1][0] += isoCountD[chainList][0]/isoCountD[chainList][1]
            except:
                continue

            try:
                ChainDict[keyChain][1][1] += IgRDict[chainList]
            except:
                continue
        
        
        ChainDict[keyChain][1][0] /=  len(ChainDict[keyChain][0]) - 1
        ChainDict[keyChain][1][1] /=  len(ChainDict[keyChain][0]) - 1

        # if addFlag:
        #     isoLL.sort(key = lambda x: x[rankOp[1]],reverse = True) # Main Sort of RANK HGE
        # else:
        #     if i:
        #         isoLL.sort(key = lambda x: x[rankOp[1]],reverse = True) # Main Sort of RANK HGE
        #     else:
        #         isoLL.sort(key = lambda x: x[rankOp[0]],reverse = True) # Main Sort of RANK HGE

    Ranges = []
    chainRankIso = {}

    for ChainAnsestor in ChainDict:
        ChainList = ChainDict[ChainAnsestor]
        for ChainMember in ChainList[0]:
            if ChainMember not in chainRankIso: 
                chainRankIso[ChainMember] = ChainList[1]


 
    for idxR, isoPeakL, DBInfoD in zip(idxPairL,isoPeakLL,DBInfoDL):
        iEner = idxR[0]
        fEner = idxR[1]
        Ranges.append([iEner,fEner])

        print('\nThe energy range consulted is between %.2f keV and %.2f keV.\n' % (iEner,fEner))
        Eg , Ig , Decay, Half , Parent, rank, rank2,rank3, CR2, CR3 = [],[],[],[],[],[],[],[],[],[]
        for pInfo in isoPeakL:
            iso = pInfo[0]
            if iso not in chainRankIso:
                cr2, cr3 = [0,0]
            else:
                cr2,cr3 = chainRankIso[iso]

            CR2.append(cr2)
            CR3.append(cr3)

            
            Ele = DBInfoD[iso]
            Eg.append(str(Ele[1])+' ('+str(Ele[2])+')')
            Ig.append(round(Ele[3],2))#+' ('+str(Ele[4])+')') #Normalized Intensity
            Decay.append(Ele[5])
            #Half.append(str(Ele[6])+' '+Ele[7]+' ('+str(Ele[8])+')')
            x=halfLifeUnit(Ele)
            if x == 0:
                y = str(x)
            else:
                y = str('{0:.2e}'.format(x))
            Half.append(y+ ' [s] ')# + str(Ele[6]) +' ' +str(Ele[7]) + ' ('+str(Ele[8])+')')
            Parent.append(Ele[-1])
            rank.append(pInfo[1])
            rank2.append(round(pInfo[2],3))
            rank3.append(round(pInfo[-1],3))

            pd.set_option('display.max_rows', None) #imprime todas las filas
            pd.options.display.float_format = '{:,.5f}'.format
            df = pd.DataFrame(sorted(list(zip(Eg,Ig,Decay,Half,Parent,rank,rank2,rank3,CR2,CR3)), key=lambda x:x[xId], reverse= True),columns=['Eg [keV]','Ig (%)','Decay m','Half Life','Parent','Rank','Rank2','Rank3','CR2','CR3'])#crea  la tabla
        
        if allFlag:
            print(df)
        else:
            print(df.head(10))

        if wofFlag:
            try:
                if addFlag:
                    myfilename = infoFile.strip('.info') + '_rank_I.txt'
                else:
                    myfilename = infoFile.strip('.info') + '_rank_J.txt'
                if allFlag:
                    WriteOutputFileRR(myfilename,df,iEner,fEner)
                else:
                    WriteOutputFileRR(myfilename,df.head(10),iEner,fEner)
                
                print('-----------------------------------------')
                print('The file was saved as:')
                print(myfilename)
                print('-----------------------------------------')        
            

            except IOError:
                print('ERROR: An unexpected error ocurrs. Data could not be saved.')
                break
        
    return 0
        


# def ChainRankFun(ListOpt):
#     List = ListOpt.copy()
#     List.pop(0)  
    
#     if '--wof' in List:
#         wofFlag = True
#         List.remove('--wof')
#     else:
#         wofFlag = False

#     if '--all' in List:
#         allFlag = True
#         List.remove('--all')
#     else:
#         allFlag = False

#     if len(List) == 0:
#         print("error: --chainRank option needs an argument")
#         return 3500
    
#     infoFile=List[0]
#     if not os.path.isfile(infoFile):
#         print("error: %s does not exist, are you in the right path?" %(infoFile))
#         return 3501
#     if not infoFile.endswith('.info'):
#         print("error: %s needs a .info extension" % (infoFile))
#         return 3502

#     infoDict=getDictFromInfoFile(infoFile)
#     minRange = infoDict['Range']['start']
#     maxRange = infoDict['Range']['end']
#     #del infoDict['Range']

#     pathfile = os.path.realpath(__file__)
#     pathfile = pathfile.strip('chainRank.py')
#     conexion = OpenDatabase(pathfile)

#     ChainDict = {}

#     memoLenDict={}
#     isoPeakLL = []
#     isoCountD = {}
#     DBInfoL = []
#     DBInfoDL = []
#     #tMinE,tMaxE = infoDict['theList'][0],infoDict['theList'][-1]
#     tMinEL = []
#     tMaxEL = []
#     idxPairL = []

#     for DictEle in infoDict.values():
#         idxPairL.append([DictEle['start'],DictEle['end']])

#     if True:
#         for infoPair in infoDict.values():
#             tMinEL.append(infoPair['start'])
#             tMaxEL.append(infoPair['end'])
#         tMinE = min(tMinEL)
#         tMaxE = max(tMaxEL)
#     else:
#         tMinE = minRange
#         tMaxE = maxRange

#     for idxR in idxPairL:
#         iEner = idxR[0]
#         fEner = idxR[1]
#         #DBInfoL.append(EnergyRange(conexion,iEner,fEner))
#         DBInfoL.append(GetIntensities(conexion,iEner,fEner))
#         DBInfo = DBInfoL[-1]
#         DBInfoD = {}
#         for e in DBInfo: 
#             #Filling dict with isotope name each isotope has only one tupple
#             DBInfoD[e[-1]] = e      
#         DBInfoDL.append(DBInfoD)   
#         isoPeakL = []
#         for Ele in DBInfo:
#             MainChainIso, _ = GetChainAndChild(conexion,Ele[-1])
#             if MainChainIso not in ChainDict and MainChainIso is not None:
#                 ChainDict[MainChainIso] = [chaintoList(GetMainChain(conexion,MainChainIso)[0]),0]
              

#             pass

       
#         #     iso = Ele[-1]
#         #     if [iso,1,0,0] not in isoPeakL:
#         #         isoPeakL.append([iso,1,0,Ele[10]]) #So that there is only one count of each isotope per peak
#         #         if iso not in isoCountD: #Considering the number of entries in the energy range of the histogram
#         #             if iso not in memoLenDict:
#         #                 #memoLenDict[iso]=len(EnergyRange(conexion,tMinE,tMaxE,iso))
#         #                 memoLenDict[iso]=len(GetIntensities(conexion,tMinE,tMaxE,iso))
#         #             nInRange=memoLenDict[iso]
#         #             isoCountD[iso] = [0,nInRange,0]
#         #         isoCountD[iso][0] += 1
#         # isoPeakLL.append(isoPeakL)










#     # for Isotope in List:
#     #     MainChainIso,Child = GetChainAndChild(conexion,Isotope)
#     #     if MainChainIso == None or Child == None:
        
#     #         print('Isotope: ' + Isotope + ' -- Parent: ' + 'None' + ' --Child: ' + 'None' +  '\n')
#     #         print('There is not enough information in the database or the isotope ' + Isotope + ' do not have Child or parents isotopes. \n')
        
#     #     else:
        
#     #         MainChain = GetMainChain(conexion,MainChainIso)
#     #         if '+' in MainChain:
#     #             AuxStr = MainChain.split('+')[1]
#     #             Parentiso = AuxStr.split('#')[0]
#     #         else:
#     #             Parentiso = MainChain[0].split('#')[0]

#     #         print('Isotope: ' + Isotope + ' -- Parent: ' + Parentiso + ' --Child: ' + Child + '\n')
        
#     CloseDatabase(conexion)
#     return 0