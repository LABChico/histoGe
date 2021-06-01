import sys
import os.path
import pandas as pd 
from myLibs.miscellaneus import WriteOutputFileRR
from math import sqrt
from myLibs.parsers import getDictFromInfoFile, getMyFileDictRankAdv, functionDictAdv, findRangeInfoDict, isValidSpecFile
from myLibs.miscellaneus import getIdxRangeVals, removeDuplicates
from myLibs.QueryDB import OpenDatabase, CloseDatabase, EnergyRange, halfLifeUnit, GetIntensities
from myLibs.fitting import doFittingStuff,MeanDistance
from myLibs.gilmoreStats import doGilmoreStuff
from operator import itemgetter

def rankProb(ListOpt):
    List = ListOpt.copy()
    List.pop(0)  
    i = 0 #for rank op
    rankOp = []
    rankOp2 = [None,None,None]
    
    if '--noCal' in List:
        noCalFlag = True
        List.remove('--noCal')
    else:
        noCalFlag = False
    
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
            if int(Arg) > 0 and int(Arg) < 4:
                rankOp.append(int(Arg))
            else:
                continue
        except:
            if len(List) <= 1:
                rankOp.append(3)
            continue
    
    if len(rankOp) == 0:
        rankOp.append(3)
        rankOp.append(2) 
    elif len(rankOp) == 1:
        if rankOp[0] == 3:
            rankOp.append(2)
        else:
            rankOp.append(3)

    rankOp = removeDuplicates(rankOp)    
    rankOp2 = [-2,-3,1]
    if len(List) == 0:
        sys.stderr.write("error: --rank option needs an argument\n")
        return 0

    for arg in List:
        if isValidSpecFile(arg):
            if arg.endswith('.info'):
                infoFile = arg
            else:
                FileName = arg
    
    try:
        if isValidSpecFile(FileName):
            FileExt = FileName.split('.')[-1]
    except:
        sys.stderr.write('ERROR: Unexpected error. Not a valid file used.\n')
        return 110

    if not os.path.isfile(infoFile):
        sys.stderr.write("error: %s does not exist, are you in the right path?\n" %(infoFile))
        return 10000
    if not infoFile.endswith('.info'):
        sys.stderr.write("error: %s needs a .info extension\n" % (infoFile))
        return 10001
    infoDict=getDictFromInfoFile(infoFile)
    

    if noCalFlag:
        FileDict = functionDictAdv[FileExt](FileName,False)
    else:
        FileDict = functionDictAdv[FileExt](FileName)

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
    pathfile = pathfile.replace('/modules/rank_prob.py','')
    conexion = OpenDatabase(pathfile)

    memoLenDict={}

    isoCountD = {}
    DBInfoL = []
    DBInfoDL = []
    tMinEL = []
    tMaxEL = []
    ProbLL = []
    DiffLL = []
    ProbDL = {}
    DiffDL = {}
    if True:
        for infoPair in infoDict.values():
            tMinEL.append(infoPair['start'])
            tMaxEL.append(infoPair['end'])
        tMinE = min(tMinEL)
        tMaxE = max(tMaxEL)
    else:
        tMinE = minRange
        tMaxE = maxRange

    myDataList = FileDict['theList']
    
    fittingDict=doFittingStuff(infoDict,myDataList)
    fittingDictKeys = list(fittingDict.keys())

    PeakNum = -1
    IdxRemove=[]
    
    for idxR in idxPairL:
        PeakNum += 1
        iEner = idxR[0]
        fEner = idxR[1]
        DBInfo = GetIntensities(conexion,iEner,fEner)
        DiffL, ProbL = MeanDistance(DBInfo,fittingDict[fittingDictKeys[PeakNum]])
        if DiffL == None or ProbL == None:
            continue
        else:
            IdxRemove.append(PeakNum)
            DBInfoL.append(DBInfo)
            DiffLL.append(DiffL)
            ProbLL.append(ProbL)
            DBInfoD = {}
            for e,fs,gs in zip(DBInfo,DiffL,ProbL): 
                if e[-1] not in DBInfoD:
                    DBInfoD[e[-1]] = [e]
                    ProbDL[gs[0]] = [gs]
                    DiffDL[fs[0]] = [fs]
                else:
                    DBInfoD[e[-1]].append(e)
                    ProbDL[gs[0]].append(gs)
                    DiffDL[fs[0]].append(fs)
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
    
    idxPairL=list(map(idxPairL.__getitem__,IdxRemove))
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
            myfilename = infoFile.strip('.info') + '_rank_B.txt'
        
        elif rankOp[0] == 2:
            myfilename = infoFile.strip('.info') + '_rank_C.txt'
        
        elif rankOp[0] == 3:
            myfilename = infoFile.strip('.info') + '_rank_B.txt'

        else:
            myfilename = infoFile.strip('.info') + '_rank_B.txt'
    except:
        myfilename = 'FileNameCouldNotBeRecovered.txt'

    for idxR,DBInfoD in zip(idxPairL,DBInfoDL):
        iEner = idxR[0]
        fEner = idxR[1]
        Ranges.append([iEner,fEner])
        Eg , Ig , Decay, Half , Parent, rank, rank2, rank3, ProbRank, DiffRank  = [],[],[],[],[],[],[],[],[],[]
        for Key in DBInfoD:
            for Ele,DiffEle,ProbEle in zip(DBInfoD[Key],DiffDL[Key],ProbDL[Key]):
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
                ProbRank.append(ProbEle[1])
                DiffRank.append(DiffEle[1])

        Eg,Ig,Decay,Half,Parent,rank3,ProbRank,DiffRank = (list(t) for t in zip(*sorted(zip(Eg,Ig,Decay,Half,Parent,rank3,ProbRank,DiffRank),key=itemgetter(*rankOp2) ,reverse=True)))

        print('\nThe energy range consulted is between %.2f keV and %.2f keV.\n' % (iEner,fEner))
        
        if allFlag:
            pd.set_option('display.max_rows', None)
            pd.options.display.float_format = '{:,.5f}'.format
            df = pd.DataFrame(list(zip(Eg,Ig,Decay,Half,Parent,rank3,ProbRank,DiffRank)),columns=['Eg [keV]','Ig (%)','Decay m','Half Life','Parent','Rank F','Probability','Distance'])#crea  la tabla
            print(df)
            
        else:
            pd.set_option('display.max_rows', len(Ele))
            df = pd.DataFrame(list(zip(Eg,Ig,Decay,Half,Parent,rank3,ProbRank,DiffRank)),columns=['Eg [keV]','Ig (%)','Decay mode','Half Life','Parent','Rank F','Probability','Distance'])#crea  la tabla
            print(df.head(10))
            
        if wofFlag:
            try:
                if allFlag:
                    WriteOutputFileRR(myfilename,df,iEner,fEner)
                    
                else:
                    WriteOutputFileRR(myfilename,df.head(10),iEner,fEner)    
            
            except IOError:
                sys.stderr.write('ERROR: An unexpected error ocurrs. Data could not be saved.\n')
                break
    
    if wofFlag:
        print('-----------------------------------------')
        print('The file was saved as:')
        print(myfilename)
        print('-----------------------------------------')  

    return 0
    
