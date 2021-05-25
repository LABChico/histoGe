import sys
import os.path
import pandas as pd 
from myLibs.miscellaneus import WriteOutputFileRR
from math import sqrt
from myLibs.parsers import getDictFromInfoFile, getMyFileDictRankAdv, functionDictAdv, findRangeInfoDict
from myLibs.miscellaneus import getIdxRangeVals, removeDuplicates, operatingSystem
from myLibs.QueryDB import OpenDatabase, CloseDatabase, EnergyRange, halfLifeUnit, GetIntensities
from myLibs.fitting import doFittingStuff
from myLibs.gilmoreStats import doGilmoreStuff
from operator import itemgetter

def rankImp(ListOpt):
    List = ListOpt.copy()
    List.pop(0)  
    i = 0 #for rank op
    rankOp = []
    rankOp2 = [None,None,None]
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

    for Arg in List:
        try:
            #if int(Arg) > 0 and int(Arg) < 4:
            if Arg == 'D':
                #rankOp.append(int(Arg))
                rankOp.append(1)
            
            elif Arg == 'E':
               #rankOp.append(int(Arg))
                rankOp.append(2)
            
            elif Arg == 'F':
                #rankOp.append(int(Arg))
                rankOp.append(3)
            else:
                continue
        except:
            if len(List) <= 1:
                rankOp.append(3)
            continue
    
    if len(rankOp) == 0:
        rankOp.append(3)
        rankOp.append(2)
        rankOp.append(1)
    elif len(rankOp) == 1:
        if rankOp[0] == 3:
            rankOp.append(2)
            rankOp.append(1)
        elif rankOp[0] == 2:
            rankOp.append(3)
            rankOp.append(1)
        elif rankOp[0] == 1:
            rankOp.append(3)
            rankOp.append(2) 

    rankOp = removeDuplicates(rankOp)    
    rankOp2 = [x-4 for x in rankOp]
    rankOp2.append(1)

    if len(List) == 0:
        sys.stderr.write("error: --rank option needs an argument")
        return 0

    infoFile=List[0]
    if not os.path.isfile(infoFile):
        sys.stderr.write("error: %s does not exist, are you in the right path?" %(infoFile))
        return 10000
    if not infoFile.endswith('.info'):
        sys.stderr.write("error: %s needs a .info extension" % (infoFile))
        return 10001
    infoDict=getDictFromInfoFile(infoFile)
    
    try:
        minRange = infoDict['Range']['start']
        maxRange = infoDict['Range']['end']
        del infoDict['Range']
    except:
        minRange, maxRange = findRangeInfoDict(infoDict)
    
    idxPairL = []
    for DictEle in infoDict.values():
        idxPairL.append([DictEle['start'],DictEle['end']])

    DBInfoL = []
    pathfile = os.path.realpath(__file__)
    if operatingSystem == 'Linux' or operatingSystem == 'Darwin':
        pathfile = pathfile.replace('/modules/rank_imp.py','')
    elif operatingSystem == 'Windows':
        pathfile = pathfile.replace('\\modules\\rank_imp.py','')
        
    conexion = OpenDatabase(pathfile)

    memoLenDict={}

    isoCountD = {}
    DBInfoL = []
    DBInfoDL = []
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

    PeakNum = -1
    for idxR in idxPairL:
        PeakNum += 1
        iEner = idxR[0]
        fEner = idxR[1]
        DBInfoL.append(GetIntensities(conexion,iEner,fEner))
        DBInfo = DBInfoL[-1]
        DBInfoD = {}
        for e in DBInfo: 
            if e[-1] not in DBInfoD:
                DBInfoD[e[-1]] = [e]
            else:
                DBInfoD[e[-1]].append(e)
        DBInfoDL.append(DBInfoD)   
    
        for Ele in DBInfo:
            iso = Ele[-1]
            if iso not in memoLenDict:
                memoLenDict[iso]=[len(GetIntensities(conexion,tMinE,tMaxE,iso)),1,Ele[10],[PeakNum]]
                
                isoCountD[iso] = [Ele]
            else:
                memoLenDict[iso][1] += 1 
                memoLenDict[iso][2] += Ele[10]
                memoLenDict[iso][3].append(PeakNum)
                isoCountD[iso].append(Ele)

    memoLenDictKeys = memoLenDict.copy().keys()
    for Ele in memoLenDictKeys:
        if memoLenDict[Ele][0] == 0 or memoLenDict[Ele][2] == 0:
            del memoLenDict[Ele]
            del isoCountD[Ele]
            for DBInfoD in DBInfoDL:
                try:
                    del DBInfoD[Ele]
                except KeyError:
                    continue

    memoLenDictKeys = memoLenDict.keys()

    Ranges = []
    rankList = []

    try:
        if rankOp[0] == 1:
            myfilename = infoFile.strip('.info') + '_rank_D.txt'
        
        elif rankOp[0] == 2:
            myfilename = infoFile.strip('.info') + '_rank_E.txt'
        
        elif rankOp[0] == 3:
            myfilename = infoFile.strip('.info') + '_rank_F.txt'

        else:
            myfilename = infoFile.strip('.info') + '_rank_F.txt'
    except:
        myfilename = 'FileNameCouldNotBeRecovered.txt'

    for idxR,DBInfoD in zip(idxPairL,DBInfoDL):
        iEner = idxR[0]
        fEner = idxR[1]
        Ranges.append([iEner,fEner])
        Eg , Ig , Decay, Half , Parent, rank, rank2,rank3 = [],[],[],[],[],[],[],[]
        for Key in DBInfoD:
            for Ele in DBInfoD[Key]:
                Eg.append(Ele[1])
                Ig.append(round(Ele[3],2))
                Decay.append(Ele[5])
                x=halfLifeUnit(Ele)
                if x == 0:
                    y = str(x)
                else:
                    y = str('{0:.2e}'.format(x))
                Half.append(y+ ' [s] ')
                Parent.append(Ele[-1])
                rank.append(memoLenDict[Ele[-1]][1])
                rank2.append(round(memoLenDict[Ele[-1]][1]/memoLenDict[Ele[-1]][0],3))
                rank3.append(round(memoLenDict[Ele[-1]][2],3))
                
        Eg,Ig,Decay,Half,Parent,rank,rank2,rank3 = (list(t) for t in zip(*sorted(zip(Eg,Ig,Decay,Half,Parent,rank,rank2,rank3),key=itemgetter(*rankOp2) ,reverse=True)))

        print('\nThe energy range consulted is between %.2f keV and %.2f keV.\n' % (iEner,fEner))
        
        if allFlag:
            pd.set_option('display.max_rows', None) 
            pd.options.display.float_format = '{:,.5f}'.format
            df = pd.DataFrame(list(zip(Eg,Ig,Decay,Half,Parent,rank,rank2,rank3)),columns=['Eg [keV]','Ig (%)','Decay m','Half Life','Parent','Rank D','Rank E','Rank F'])#crea  la tabla
            print(df)
            
        else:
            pd.set_option('display.max_rows', len(Ele))
            df = pd.DataFrame(list(zip(Eg,Ig,Decay,Half,Parent,rank,rank2,rank3)),columns=['Eg [keV]','Ig (%)','Decay mode','Half Life','Parent','Rank D','Rank E','Rank F'])#crea  la tabla
            print(df)
            
        if wofFlag:
            try:
                if allFlag:
                    WriteOutputFileRR(myfilename,df,iEner,fEner)
                    
                else:
                    WriteOutputFileRR(myfilename,df.head(10),iEner,fEner)    
            
            except IOError:
                sys.stderr.write('ERROR: An unexpected error ocurrs. Data could not be saved.')
                break
    
    if wofFlag:
        print('-----------------------------------------')
        print('The file was saved as:')
        print(myfilename)
        print('-----------------------------------------')  

    return 0
    
