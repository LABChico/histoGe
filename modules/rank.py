import sys
import os.path
import pandas as pd
from myLibs.miscellaneus import WriteOutputFileRR
from myLibs.parsers import getDictFromInfoFile
from myLibs.miscellaneus import getIdxRangeVals, operatingSystem
from myLibs.QueryDB import OpenDatabase, CloseDatabase, EnergyRange, halfLifeUnit, GetIntensities

def rankFun(ListOpt):
    List = ListOpt.copy()
    List.pop(0)  
    i = 0 #for rank op
    rankOp = []
    
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

    if 'and' in List:
        addFlag = True
        List.remove('and')
    else:
        addFlag = False
 
    for Arg in List:
        try:
            rankOp.append(int(Arg))
            if rankOp[i] > 0 and rankOp[i] < 4:
                
                if type(rankOp[i]) == int:
                    i += 1
            
        except:
            rankOp.append(3)
            continue   

    if len(List) == 0:
        sys.stderr.write("error: --Rank option needs an argument\n")
        return 0

    infoFile=List[0]
    if not os.path.isfile(infoFile):
        sys.stderr.write("error: %s does not exist, are you in the right path?\n" %(infoFile))
        return 100
    if not infoFile.endswith('.info'):
        sys.stderr.write("error: %s needs a .info extension" % (infoFile))
        return 101
    infoDict=getDictFromInfoFile(infoFile)
    minRange = infoDict['Range']['start']
    maxRange = infoDict['Range']['end']
    del infoDict['Range']

    idxPairL = []
    for DictEle in infoDict.values():

        if addFlag :
            if rankOp[2] == 1:
                rankSort = 'Rank'
                
                idxPairL.append([DictEle['start'],DictEle['end']])
            
            elif rankOp[2] == 2:
                rankSort = 'Rank2'
                
                idxPairL.append([DictEle['start'],DictEle['end']])
                
            
            elif rankOp[2] == 3:
                rankSort = 'Rank3'
                
                idxPairL.append([DictEle['start'],DictEle['end']])
            
            else:
                idxPairL.append([DictEle['start'],DictEle['end']])
                sys.stderr.write('there is no rank op {}, please try an option between 1 and 3'.format(rankOp))
                break
        else:
            rankSort = 'Rank3'
            
            idxPairL.append([DictEle['start'],DictEle['end']])
        
    
    DBInfoL = []
    pathfile = os.path.realpath(__file__)
    if operatingSystem == 'Linux' or operatingSystem == 'Darwin':
        pathfile = pathfile.replace('/modules/rank.py','')
    elif operatingSystem == 'Windows':
        pathfile = pathfile.replace('\\modules\\rank.py','')

    conexion = OpenDatabase(pathfile)

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

        if addFlag:
            isoLL.sort(key = lambda x: x[rankOp[1]],reverse = True) # Main Sort of RANK HGE
        else:
            if i:
                isoLL.sort(key = lambda x: x[rankOp[1]],reverse = True) # Main Sort of RANK HGE
            else:
                isoLL.sort(key = lambda x: x[rankOp[0]],reverse = True) # Main Sort of RANK HGE
    
    Ranges = []
    for idxR, isoPeakL, DBInfoD in zip(idxPairL,isoPeakLL,DBInfoDL):
        iEner = idxR[0]
        fEner = idxR[1]
        Ranges.append([iEner,fEner])

        print('\nThe energy range consulted is between %.2f keV and %.2f keV.\n' % (iEner,fEner))
        Eg , Ig , Decay, Half , Parent, rank, rank2,rank3 = [],[],[],[],[],[],[],[]
        for pInfo in isoPeakL:
            iso = pInfo[0]
            Ele = DBInfoD[iso]
            Eg.append(str(Ele[1])+' ('+str(Ele[2])+')')
            Ig.append(round(Ele[3],2))#Normalized Intensity
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

        if allFlag:
            pd.set_option('display.max_rows', None) 
            pd.options.display.float_format = '{:,.5f}'.format
            df = pd.DataFrame(list(zip(Eg,Ig,Decay,Half,Parent,rank,rank2,rank3)),columns=['Eg [keV]','Ig (%)','Decay m','Half Life','Parent','Rank','Rank2','Rank3'])#crea  la tabla
            if addFlag:
                print(df.sort_values(by=[rankSort], ascending=False))
            else:
                print(df)
        else:
            pd.set_option('display.max_rows', len(Ele))
            df = pd.DataFrame(list(zip(Eg,Ig,Decay,Half,Parent,rank,rank2,rank3)),columns=['Eg [keV]','Ig (%)','Decay mode','Half Life','Parent','Rank','Rank2','Rank3'])#crea  la tabla
            if addFlag:
                print(df.head(10).sort_values(by=[rankSort], ascending=False))
            else:
                print(df.head(10))
            
            

        if wofFlag:
            try:
                if rankOp[1] == 1:
                    myfilename = infoFile.strip('.info') + '_rank_B.txt'
                
                elif rankOp[1] == 2:
                    myfilename = infoFile.strip('.info') + '_rank_C.txt'
                
                elif rankOp[1] == 3:
                    myfilename = infoFile.strip('.info') + '_rank_D.txt'

                else:
                    myfilename = infoFile.strip('.info') + '_rank_D.txt'

                if allFlag:
                    if addFlag:
                        WriteOutputFileRR(myfilename,df.sort_values(by=[rankSort], ascending=False),iEner,fEner)
                    else:
                        WriteOutputFileRR(myfilename,df,iEner,fEner)
                else:
                    if addFlag:
                        WriteOutputFileRR(myfilename,df.head(10).sort_values(by=[rankSort], ascending=False),iEner,fEner)
                    else:
                        WriteOutputFileRR(myfilename,df.head(10),iEner,fEner)
                
                print('-----------------------------------------')
                print('The file was saved as:')
                print(myfilename)
                print('-----------------------------------------')        
            

            except IOError:
                sys.stderr.write('ERROR: An unexpected error ocurrs. Data could not be saved.')
                break
    
            
    
    return 0