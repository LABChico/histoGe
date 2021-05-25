import sys
import os.path
import pandas as pd
from myLibs.miscellaneus import WriteOutputFileRR
from math import sqrt
from myLibs.parsers import getDictFromInfoFile, getMyFileDictRankAdv, functionDictAdv, findRangeInfoDict,isValidSpecFile
from myLibs.miscellaneus import getIdxRangeVals, removeDuplicates, operatingSystem
from myLibs.QueryDB import OpenDatabase, CloseDatabase, EnergyRange, halfLifeUnit, GetIntensities
from myLibs.fitting import doFittingStuff
from myLibs.gilmoreStats import doGilmoreStuff

def rankAdvFun(ListOpt):
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
#####    
    if '--filter' in List:
        filterFlag = True
        List.remove('--filter')
        IntensityFilter = 5/100
    else:
        filterFlag = False
        
#####

    if '--op1' in List:
        op1Flag = True
        List.remove('--op1')
    else:
        op1Flag = False

    if len(List) == 0:
        sys.stderr.write("error: --energyRanges option needs an argument\n")
        return 0

    for arg in List:
        if isValidSpecFile(arg):
            if arg.endswith('.info'):
                infoFile = arg
            else:
                myFilename = arg
    
    try:
        if isValidSpecFile(myFilename):
            myExtension = myFilename.split('.')[-1]
    except:
        sys.stderr.write('ERROR: Unexpected error. Not a valid file used.\n')
        return 120


    if not os.path.isfile(infoFile):
        sys.stderr.write("error: %s does not exist, are you in the right path?\n" %(infoFile))
        return 10000
    if not infoFile.endswith('.info'):
        sys.stderr.write("error: %s needs a .info extension\n" % (infoFile))
        return 10001
    infoDict=getDictFromInfoFile(infoFile)
    try:
        minRange = infoDict['Range']['start']
        maxRange = infoDict['Range']['end']
        del infoDict['Range']
    except:
        minRange, maxRange = findRangeInfoDict(infoDict)
    
    myFileDict=getMyFileDictRankAdv(List)

    noCalFlag = False
    mySpecialDict = functionDictAdv[myExtension](myFilename,noCalFlag) 
    myDataList = mySpecialDict['theList']
    
    gilmoreDict = doGilmoreStuff(infoDict,myDataList)
    gilmoreDictKeys = list(gilmoreDict.keys())

    idxPairL = []
    for DictEle in infoDict.values():
        ####
        if op1Flag:
            deltaEle = (DictEle['end']-DictEle['start'])*.1 
            meanEle = (DictEle['start']+DictEle['end'])/2
            DictEle['start'] = meanEle - deltaEle
            DictEle['end'] = meanEle + deltaEle
            idxPairL.append([DictEle['start'],DictEle['end']])
        else:
            idxPairL.append([DictEle['start'],DictEle['end']])
        ####
    #Energy range of the histogram
    
    DBInfoL = []
    pathfile = os.path.realpath(__file__)
    if operatingSystem == 'Linux' or operatingSystem == 'Darwin':
        pathfile = pathfile.replace('/modules/rankAdv.py','')
    elif operatingSystem == 'Windows':
        pathfile = pathfile.replace('\\modules\\rankAdv.py','')

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
            #Filling dict with isotope name each isotope has only one tupple
            if e[-1] not in DBInfoD:
                DBInfoD[e[-1]] = [e]
            else:
                DBInfoD[e[-1]].append(e)
        DBInfoDL.append(DBInfoD)   
    
        for Ele in DBInfo:
            iso = Ele[-1]
            if iso not in memoLenDict:
                if filterFlag:
                    IntInRange = GetIntensities(conexion,tMinE,tMaxE,iso)
                    Count = 0
                    for Element in IntInRange:
                        if Element[10] >= IntensityFilter:
                            Count += 1
                    if Ele[10] >= IntensityFilter:
                        memoLenDict[iso]=[Count,1,Ele[10],[PeakNum]]
                    else:
                        memoLenDict[iso]=[Count,1,0,[PeakNum]]

                else:
                    memoLenDict[iso]=[len(GetIntensities(conexion,tMinE,tMaxE,iso)),1,Ele[10],[PeakNum]]
                
                isoCountD[iso] = [Ele]
            else:
                if filterFlag:
                    if Ele[10] >= IntensityFilter:
                        memoLenDict[iso][1] += 1 
                        memoLenDict[iso][2] += Ele[10]
                        memoLenDict[iso][3].append(PeakNum)
                        isoCountD[iso].append(Ele)
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
    
    if filterFlag:
        DBInfoDLshort = []
        for DBInfoD in DBInfoDL:
            DBInfoDKeys = DBInfoD.copy().keys()
            for KeyDB in DBInfoDKeys:
                if KeyDB not in memoLenDictKeys:
                    del DBInfoD[KeyDB]
            DBInfoDLshort.append(DBInfoD)

    else:
        DBInfoDLshort = DBInfoDL.copy()
    
    DevRankD = {}

    for Key in memoLenDictKeys:
        NetAreaTot = 0
        NormPeakIntensity = 0
        for Peak in removeDuplicates(memoLenDict[Key][3]):    
            NetAreaTot += gilmoreDict[gilmoreDictKeys[Peak]][1]
            for MultiPeak in DBInfoDLshort[Peak][Key]:
                NormPeakIntensity += MultiPeak[10]

        ECM = 0
        
        if len(removeDuplicates(memoLenDict[Key][3])) == 1:
            DevRankD[Key] = (memoLenDict[Key][0]/memoLenDict[Key][1])
        else:

            for Peak in removeDuplicates(memoLenDict[Key][3]):
                MultiPeakIntensity = 0
                for MultiPeak in DBInfoDLshort[Peak][Key]:
                    MultiPeakIntensity += MultiPeak[10]
                ECM += ((MultiPeakIntensity/NormPeakIntensity)-(gilmoreDict[gilmoreDictKeys[Peak]][1]/NetAreaTot))**2
    
            DevRankD[Key] = (memoLenDict[Key][0]/memoLenDict[Key][1])*sqrt(ECM/len(memoLenDict[Key][3]))

    Ranges = []
    for idxR, DBInfoD in zip(idxPairL,DBInfoDL):
        iEner = idxR[0]
        fEner = idxR[1]
        Ranges.append([iEner,fEner])
        Eg , Ig , Decay, Half , Parent, rank = [],[],[],[],[],[]
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
                rank.append(DevRankD[Key])


        print('\nThe energy range consulted is between %.2f keV and %.2f keV.\n' % (iEner,fEner))
        
        if allFlag:
            pd.set_option('display.max_rows', None)
            if filterFlag:
                df = pd.DataFrame(sorted(list(zip(Eg,Ig,Decay,Half,Parent,rank)), key=lambda x:(x[5],-x[1]) ),index = None,columns=['Eg [keV]','Ig (%)','Decay m','Half Life','Parent','Rank G Filter'])#crea  la tabla
            else: 
                df = pd.DataFrame(sorted(list(zip(Eg,Ig,Decay,Half,Parent,rank)), key=lambda x:(x[5],-x[1]) ),index = None,columns=['Eg [keV]','Ig (%)','Decay m','Half Life','Parent','Rank G'])#crea  la tabla
            
            print(df)
        else:
            pd.set_option('display.max_rows', 10)
            if filterFlag:
                df = pd.DataFrame(sorted(list(zip(Eg,Ig,Decay,Half,Parent,rank)), key=lambda x:(x[5],-x[1]) ),index = None,columns=['Eg [keV]','Ig (%)','Decay m','Half Life','Parent','Rank G Filter'])#crea  la tabla
            else:
                df = pd.DataFrame(sorted(list(zip(Eg,Ig,Decay,Half,Parent,rank)), key=lambda x:(x[5],-x[1]) ),index = None ,columns=['Eg [keV]','Ig (%)','Decay mode','Half Life','Parent','Rank G'])#crea  la tabla
            print(df.head(10))
            
        if wofFlag:
            try:
                if filterFlag:
                    myfilename = infoFile.strip('.info') + '_rank_G_filter.txt'
                else:
                    myfilename = infoFile.strip('.info') + '_rank_G.txt'

                WriteOutputFileRR(myfilename,df,iEner,fEner)
                print('-----------------------------------------')
                print('The file was saved as:')
                print(myfilename)
                print('-----------------------------------------')
            except IOError:
                sys.stderr.write('ERROR: An unexpected error ocurrs. Data could not be saved.\n')
    
    return 0
    
