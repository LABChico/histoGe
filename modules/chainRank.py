import sys
import os.path
import pandas as pd

from myLibs.parsers import getDictFromInfoFile
from myLibs.QueryDB import OpenDatabase, CloseDatabase, GetChainAndChild, GetMainChain, EnergyRange, halfLifeUnit, GetIntensities, chaintoList
from myLibs.miscellaneus import WriteOutputFileRR
from myLibs.parsers import getDictFromInfoFile
from myLibs.miscellaneus import getIdxRangeVals
from myLibs.QueryDB import OpenDatabase, CloseDatabase, EnergyRange, halfLifeUnit, GetIntensities

def ChainRankFun(ListOpt):
    List = ListOpt.copy()
    List.pop(0)  
    i = 0 

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

    if len(List) == 0:
        sys.stderr.write("error: --Rank option needs an argument\n")
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
    pathfile = os.path.realpath(__file__)
    pathfile = pathfile.replace('/modules/chainRank.py','')
    conexion = OpenDatabase(pathfile)
    
    ChainDict = {}

    memoLenDict={}
    isoPeakLL = []
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


    for idxR in idxPairL:
        iEner = idxR[0]
        fEner = idxR[1]
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
            Eg.append(str(Ele[1]))#+' ('+str(Ele[2])+')')
            Ig.append(round(Ele[3],2)) 
            Decay.append(Ele[5])
            x=halfLifeUnit(Ele)
            if x == 0:
                y = str(x)
            else:
                y = str('{0:.2e}'.format(x))
            Half.append(y+ ' [s] ')
            Parent.append(Ele[-1])
            rank.append(pInfo[1])
            rank2.append(round(pInfo[2],3))
            rank3.append(round(pInfo[-1],3))

            pd.set_option('display.max_rows', None) 
            pd.options.display.float_format = '{:,.5f}'.format
            df = pd.DataFrame(sorted(list(zip(Eg,Ig,Decay,Half,Parent,rank,rank2,rank3,CR2,CR3)), key=lambda x: (x[xId],x[1]), reverse= True),columns=['Eg [keV]','Ig (%)','Decay m','Half Life','Parent','Rank C','Rank D','Rank E','Rank I','Rank J'])#crea  la tabla
        
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
                sys.stderr.write('ERROR: An unexpected error ocurrs. Data could not be saved.\n')
                break
        
    return 0
        