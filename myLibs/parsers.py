"""A series of parser functions for different ascii files that contain
spectrum information from germanium detectors. They accept a filename
parses the data accordinly and returns a dictionary with all the
internal values (it tries) including the spectrum and the exposition
time.

"""
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from myLibs.fitting import myLine,getTentParams
from myLibs.miscellaneus import List2str


MainOptD = {'help':['-h','--help'],'autoPeak':['-P','--autoPeak'],'query':['-q','--query'],'test':['-t','--test'],\
        'isotope':['-i','--isotope'],'sum':['-s','--sum'],'rank':['-R','--Rank','--rank'],'sub':['-r','--sub'],'stats':['-c','--stats'],'energy':['--energyRanges','-e'],\
        'parent':['--parent','-p'],'normint':['--normInt','-n'],'2file':['--hge','-f'], 'efficiency':['--eff','-e'],'rankAdv':['-RA','--RankAdv','--rankAdv'],\
            'fuzzy':['--fuzzy','--fuzzyRank','--fuzzyrank','-f'],'halfSort':['--halfSort','--halfRank','--halfrank'],\
            'chainRank':['--chainRank','--ChainRank','-x']}

SubOptD = {'help':[],'autoPeak':['--rebin','--wof','--noPlot','--log','--noCal'],'query':['--all'],'test':[],'isotope':[],'sum':['--noCal','--log','--noPlot','--wof'],\
        'rank':['--wof','--all'],'sub':['--noCal','--log','--noPlot','--wof','--rebin'],'stats':['--wof','--noPlot','--noCal','--log'],'energy':['--all','--wof'],'parent':[],\
            'normint':[],'2file':[],'efficiency':['--Plot','--plot'],'rankAdv':['--wof','--all','--filter'],'fuzzy':['--wof','--all','--filter'],'halfSort':['--all','--wof'],\
            'chainRank':['--wof','--all','--peak']}

def isValidSpectrumFile(strVal):
    if strVal.endswith('.Txt') or strVal.endswith('.SPE') or strVal.endswith('.mca') or strVal.endswith('.hge'):
        return True
    return False

def isValidSpecFile(strVal):
    if strVal.endswith('.Txt') or\
       strVal.endswith('.SPE') or\
       strVal.endswith('.mca') or\
       strVal.endswith('.info') or\
       strVal.endswith('.hge'):
        return True
    return False

def getDictFromSPE(speFile,nocalFlag=False):
    """Parses the .SPE file format that is used in Boulby"""
    calFlag = not nocalFlag
    internDict = {}
    #myCounter=0
    _,bCoef,_=[0.0,0.0,0.0]
    #aCoef,bCoef,cCoef=[0.0,0.0,0.0]
    myXvals=[]
    myYvals=[]
    #calBool=False
    internDict['calBoolean']=False
    #appendBool=False

    #str2init = "DATA"
    for line in open(speFile):
        iFound = line.find("$")
        if iFound != -1: #iFound == 0
            fFound=line.find(":")
            newEntry=line[iFound+1:fFound] #Avoiding the :
            internDict[newEntry]=[]
            continue
        internDict[newEntry].append(line)

    myXvals=list(range(len(internDict["DATA"][1:])))
    myYvals=[float(yVal) for yVal in internDict["DATA"][1:]]

    if "ENER_FIT" in internDict and calFlag:
        _,bCoef,_=[float(e) for e in internDict['ENER_FIT'][0].split()]
        #aCoef,bCoef,cCoef=[float(e) for e in internDict['ENER_FIT'][0].split()]
        #Assuming E=bCoef*bin+aCoef, as I understood aCoef is
        #always zero (I'm reading it anyway) and I don't know
        #what's cCoef for.

    #Creating calibrated in Energy bins
    if bCoef != 0:
        eBins=np.array([bCoef*xVal+bCoef for xVal in myXvals])
        internDict["theList"]=[eBins,myYvals]
        internDict['calBoolean']=True
    else:
        print("No calibration info, weird. Using normal bins.")
        internDict["theList"]=[myXvals,myYvals]

    tStr="MEAS_TIM"
    if tStr in internDict:
        internDict["expoTime"]=float(internDict[tStr][0]\
                                     .split()[0])

    return internDict

def getDictFromMCA(mcaFilename,noCalFlag=False):
    #"""Parses the .mca file format comming from either the micro mca or the px5."""
    internDict={}
    mcaList=[]
    str2init = "<<DATA>>"
    str2end = "<<END>>"
    strCal = "<<CALIBRATION>>"
    strIgn = "LABEL"
    strCalEnd = "<<"
    strExpTime= "REAL_TIME"
    appendBool = False
    internDict['calBoolean']=False
    calBool = False
    Calibrated = False
    internDict["noCalFlag"] = False

    x4cal=[]
    y4cal=[]

    #Ignoring errors for now, however bins are not skipped
    for line in open(mcaFilename, errors='ignore'):
        if line.find(strExpTime) != -1:  #"REAL_TIME"
            tempList = line.split("-")
            internDict["expoTime"]=float(tempList[1])

        if line.find(strCal) != -1:  #"<<CALIBRATION>>"
            Calibrated = True
            if noCalFlag == True:
                calBool = False
            else:
                calBool = True
            continue
        

        if line.find(str2init) != -1:  #"<<DATA>>"
            appendBool = True
            calBool = False
            continue
        
        if calBool:
            if line.find(strIgn) != -1:  #"LABEL"
                continue

            if line.find(strCalEnd) != -1:  #"<<"
                calBool = False
            x4cal.append(float(line.split()[0]))
            y4cal.append(float(line.split()[1]))
        
        if line.find(str2end) != -1: #"<<END>>"
            appendBool = False
            break #stopping here for now


        if appendBool :
            mcaList.append(float(line))
    
    if len(x4cal) > 1:
        a,b=getTentParams(x4cal,y4cal)
        popt,_ = curve_fit(myLine,x4cal, y4cal, p0=[a,b])
        #popt,pcov = curve_fit(myLine,x4cal, y4cal, p0=[a,b])
        a,b=popt
        #Do the calibration etc
        xCalibrated = [a*ch+b for ch in range(len(mcaList))]
        totalList = [xCalibrated, mcaList]
        internDict['calBoolean']=True
    else:
        totalList=[range(len(mcaList)),mcaList]

    internDict["theList"]=totalList
    
    if (noCalFlag == False) and (Calibrated == False):
            internDict["noCalFlag"] = True

    return internDict

def getDictFromGammaVision(gvFilename,nocalFlag=True):
    """Parses the .Txt files from gammaVision"""
    internDict = {}
    gvList=[]
    str2init = "SPECTRUM"
    appendBool = False
    internDict['calBoolean']=False
    for line in open(gvFilename):
        if not appendBool:
            semicolonI = line.find(":")
            if semicolonI != -1:
                newKey=line[:semicolonI]
                newVal=line[semicolonI+1:]
                internDict[newKey]=newVal.strip()
        if line.find(str2init) != -1:
            appendBool = True
        if appendBool:
            lineList=line.split()
            if len(lineList) == 5:
                gvList +=[float(e) for e in lineList[1:]]
    totalList=[range(len(gvList)),gvList]
    internDict["theList"]=totalList
    tStr="Real Time"
    if tStr in internDict:
        internDict["expoTime"]=float(internDict[tStr])
    return internDict

def CommandParser(lista):
    argvcp = lista.copy()
    argvcp.pop(0)
    FileList = []
    InstList = []
    NumList = []
    NameList = []
    if len(argvcp) != 0:
        for MainOpt in MainOptD:
            
            for arg in argvcp:
                if arg in MainOptD[MainOpt]:
                    InstList.append([arg])
                    for arg2 in argvcp:
                        if arg2 in SubOptD[MainOpt]:
                            InstList[-1].append(arg2)
                        elif isValidSpecFile(arg2):
                            FileList.append(arg2)
                        else:
                            try:
                                float(arg)
                                NumList.append(arg2)
                            except ValueError:
                                if arg2[0] != '-':
                                    NameList.append(arg2)

        if len(InstList) > 0:
            InstList[-1].extend(FileList)
            InstList[-1].extend(NumList)
            InstList[-1].extend(NameList)
        else:
            InstList = [argvcp.copy()]
    else:
        return ['shorthelp'] 

    return InstList


def MultiCommandParser(lista):
    SeparatorChars = ['!']
    argvcp = lista.copy()
    argvcp.pop(0)
    CommandL = []
    CommandLL = []

    for ps,argu in enumerate(argvcp):
        if (argu in SeparatorChars):
            CommandLL.append(CommandL)
            CommandL = []
        elif (argu[-1] in SeparatorChars):
            CommandL.append(argu[:-1])
            CommandLL.append(CommandL)
            CommandL = []
        
        elif ps == len(argvcp) - 1:
            if argu not in SeparatorChars:
                CommandL.append(argu)
                CommandLL.append(CommandL)
                CommandL = []
            else:
                CommandLL.append(CommandL)

        else:
            CommandL.append(argu)

    InstListL = []
    for Command in CommandLL:
        FileList = []
        InstList = []
        NumList = []
        NameList = []
        if len(Command) != 0:
            for MainOpt in MainOptD:
                for arg in Command:
                    if arg in MainOptD[MainOpt]:
                        InstList.append([arg])
                        for arg2 in Command:
                            if arg2 in SubOptD[MainOpt]:
                                InstList[-1].append(arg2)
                            elif isValidSpecFile(arg2):
                                FileList.append(arg2)
                            else:
                                try:
                                    float(arg)
                                    NumList.append(arg2)
                                except ValueError:
                                    if arg2[0] != '-':
                                        NameList.append(arg2)

            if len(InstList) > 0:
                InstList[-1].extend(FileList)
                InstList[-1].extend(NumList)
                InstList[-1].extend(NameList)
            else:
                InstList = [Command.copy()]
            InstListL.append(InstList[-1]) 
    if InstListL == []:   
        return ['shorthelp'] 
    else:
        return InstListL

def getDictFromInfoFile(infoFileName,noCalFlag=None):
    infoDict={}
    newTable=pd.read_table(infoFileName, delim_whitespace=True, index_col=0,comment='#',skip_blank_lines=True)
    infoDict=newTable.to_dict('index')
    ObjFile = open(infoFileName)
    Line = ObjFile.readline()
    if '#SPECRANGE: ' in Line:
        Line = Line.strip('#SPECRANGE: ')
        Line = Line.strip('\n')
        RangeList = Line.split(',')
        infoDict['Range'] = {'start':float(RangeList[0]),'end':float(RangeList[1])}
    return infoDict


def getDictFromSPEAdv(speFile, nocalFlag=False):
    """Parses the .SPE file format that is used in Boulby"""
    calFlag = not nocalFlag
    internDict = {}
    #myCounter=0
    _,bCoef,_=[0.0,0.0,0.0]
    #aCoef,bCoef,cCoef=[0.0,0.0,0.0]
    myXvals=[]
    myYvals=[]
    #calBool=False
    internDict['calBoolean']=False
    #appendBool=False

    #str2init = "DATA"
    for line in open(speFile):
        iFound = line.find("$")
        if iFound != -1: #iFound == 0
            fFound=line.find(":")
            newEntry=line[iFound+1:fFound] #Avoiding the :
            internDict[newEntry]=[]
            continue
        internDict[newEntry].append(line)

    myXvals=list(range(len(internDict["DATA"][1:])))
    myYvals=[float(yVal) for yVal in internDict["DATA"][1:]]

    if "ENER_FIT" in internDict and calFlag:
        _,bCoef,_=[float(e) for e in internDict['ENER_FIT'][0].split()]
        #aCoef,bCoef,cCoef=[float(e) for e in internDict['ENER_FIT'][0].split()]
        #Assuming E=bCoef*bin+aCoef, as I understood aCoef is
        #always zero (I'm reading it anyway) and I don't know
        #what's cCoef for.

    #Creating calibrated in Energy bins
    if bCoef != 0:
        eBins=np.array([bCoef*xVal+bCoef for xVal in myXvals])
        internDict["theList"]=[eBins,myYvals]
        internDict['calBoolean']=True
    else:
        print("No calibration info, weird. Using normal bins.")
        internDict["theList"]=[myXvals,myYvals]

    tStr="MEAS_TIM"
    if tStr in internDict:
        internDict["expoTime"]=float(internDict[tStr][0]\
                                     .split()[0])

    return internDict


def getDictFromMCAAdv(mcaFilename,noCalFlag=False):
    #"""Parses the .mca file format comming from either the micro mca or the px5."""
    internDict={}
    mcaList=[]
    str2init = "<<DATA>>"
    str2end = "<<END>>"
    strCal = "<<CALIBRATION>>"
    strIgn = "LABEL"
    strCalEnd = "<<"
    strExpTime= "REAL_TIME"
    appendBool = False
    internDict['calBoolean']=False
    calBool = False
    Calibrated = False
    internDict["noCalFlag"] = False

    x4cal=[]
    y4cal=[]

    #Ignoring errors for now, however bins are not skipped
    for line in open(mcaFilename, errors='ignore'):
        if line.find(strExpTime) != -1:  #"REAL_TIME"
            tempList = line.split("-")
            internDict["expoTime"]=float(tempList[1])

        if line.find(strCal) != -1:  #"<<CALIBRATION>>"
            Calibrated = True
            if noCalFlag == True:
                calBool = False
            else:
                calBool = True
            continue
        

        if line.find(str2init) != -1:  #"<<DATA>>"
            appendBool = True
            calBool = False
            continue
        
        if calBool:
            if line.find(strIgn) != -1:  #"LABEL"
                continue

            if line.find(strCalEnd) != -1:  #"<<"
                calBool = False
            x4cal.append(float(line.split()[0]))
            y4cal.append(float(line.split()[1]))
        
        if line.find(str2end) != -1: #"<<END>>"
            appendBool = False
            break #stopping here for now


        if appendBool :
            mcaList.append(float(line))
    
    if len(x4cal) > 1:
        a,b=getTentParams(x4cal,y4cal)
        popt,_ = curve_fit(myLine,x4cal, y4cal, p0=[a,b])
        #popt,pcov = curve_fit(myLine,x4cal, y4cal, p0=[a,b])
        a,b=popt
        #Do the calibration etc
        xCalibrated = [a*ch+b for ch in range(len(mcaList))]
        totalList = [xCalibrated, mcaList]
        internDict['calBoolean']=True
    else:
        totalList=[range(len(mcaList)),mcaList]

    internDict["theList"]=totalList
    
    if (noCalFlag == False) and (Calibrated == False):
            internDict["noCalFlag"] = True

    return internDict

def getDictFromGammaVisionAdv(gvFilename, calFlag=True):
    """Parses the .Txt files from gammaVision"""
    internDict = {}
    gvList=[]
    str2init = "SPECTRUM"
    appendBool = False
    internDict['calBoolean']=False
    for line in open(gvFilename):
        if not appendBool:
            semicolonI = line.find(":")
            if semicolonI != -1:
                newKey=line[:semicolonI]
                newVal=line[semicolonI+1:]
                internDict[newKey]=newVal.strip()
        if line.find(str2init) != -1:
            appendBool = True
        if appendBool:
            lineList=line.split()
            if len(lineList) == 5:
                gvList +=[float(e) for e in lineList[1:]]
    totalList=[range(len(gvList)),gvList]
    internDict["theList"]=totalList
    tStr="Real Time"
    if tStr in internDict:
        internDict["expoTime"]=float(internDict[tStr])
    return internDict

def getDictFromHGE(myFilename,calFlag=True):
    try:
        FileObj = open(myFilename,'r')
    except:
        pass
    else:
        FileLines = FileObj.readlines()
        FileObj.close()
        hgeDict = {'DATE':[],'EQUIPMENT':[],'EXPOSURETIME':[],'CALIBRATION':[],'CHANNELS':[],'GAIN':[],'CALIBRATIONPOINTS':[],'DATA':[],'REBINEDDATA':[],'REBINFACTOR':[]}
        DATAflag = False
        rebinDATAflag = False
        AuxListXData = []
        AuxListYData = []
        for Line in FileLines:
            if Line[0] != '#':
                if 'DATE' in Line:
                    Idx = Line.find(':')
                    Idx += 2
                    try:
                        hgeDict['DATE'] = Line[Idx:-1]
                    except:
                        hgeDict['DATE'] = 'Not Available'

                elif 'EQUIPMENT' in Line:
                    Idx = Line.find(':')
                    Idx += 2
                    try:
                        hgeDict['EQUIPMENT'] = Line[Idx:-1]
                    except:
                        hgeDict['EQUIPMENT'] = 'Not Availabe'

                elif 'EXPOSURETIME' in Line:
                    Idx = Line.find(':')
                    Idx += 2
                    try:
                        hgeDict['EXPOSURETIME'] = float(Line[Idx:-1])
                    except:
                        hgeDict['EXPOSURETIME'] = 'Not Availabe'

                elif 'CALIBRATION' in Line:
                    Idx = Line.find(':')
                    Idx += 2
                    try:
                        hgeDict['CALIBRATION'] = bool(Line[Idx:-1])
                    except:
                        hgeDict['CALIBRATION'] = 'Not Availabe'

                elif 'CHANNELS' in Line:
                    Idx = Line.find(':')
                    Idx += 2
                    try:
                        hgeDict['CHANNELS'] = int(Line[Idx:-1])
                    except:
                        hgeDict['CHANNELS'] = 'Not Available'

                elif 'GAIN' in Line:
                    Idx = Line.find(':')
                    Idx += 2
                    try:
                        hgeDict['GAIN'] = float(Line[Idx:-1])
                    except:
                        hgeDict['GAIN'] = 'Not Available'
                elif 'CALIBRATIONPOINTS' in Line:
                    Idx = Line.find(':')
                    Idx += 2
                    try:
                        hgeDict['CALIBRATIONPOINTS'] = Line[Idx:-1]
                    except:
                        hgeDict['CALIBRATIONPOINTS'] = 'Not Available'
                elif (Line[:-1] == 'DATA' or DATAflag) and 'ENDDATA' not in Line:
                    if DATAflag == False:
                        DATAflag = True
                    elif DATAflag == True:
                        ListStr = Line[:-1].split(',')
                        List = [float(ele) for ele in ListStr]
                        AuxListXData.append(List[1])
                        AuxListYData.append(List[2])
                elif 'ENDDATA' in Line:
                    DATAflag = False
                    hgeDict['DATA'] = [AuxListXData,AuxListYData]
                    AuxListXData = []
                    AuxListYData = []
                    if not hgeDict['CHANNELS'] or hgeDict['CHANNELS'] == 'Not Available':
                        hgeDict['CHANNELS'] = len(hgeDict['DATA'])
                elif ('REBINEDDATA' in Line or rebinDATAflag) and 'ENDREBINEDDATA' not in Line:
                    if rebinDATAflag == False:
                        rebinDATAflag = True
                    elif rebinDATAflag == True:
                        ListStr = Line[:-1].split(',')
                        List = [float(ele) for ele in ListStr]
                        AuxListXData.append(List[1])
                        AuxListYData.append(List[2])
                elif 'ENDREBINEDDATA' in Line:
                    rebinDATAflag = False
                    hgeDict['REBINEDDATA'] = [AuxListXData,AuxListYData]
                elif 'REBINFACTOR' in Line:
                    try:
                        hgeDict['REBINFACTOR'] = int(Line.strip('REBINFACTOR: '))
                    except:
                        hgeDict['REBINFACTOR'] = 'Not Available'

    hgeDict['theList'] = hgeDict['DATA']
    if hgeDict['REBINEDDATA']:
        hgeDict['theRebinedList'] = hgeDict['REBINEDDATA']
    hgeDict['noCalFlag'] = not hgeDict['CALIBRATION']
    hgeDict['calBoolean'] = hgeDict['CALIBRATION'] 
    hgeDict["expoTime"] = hgeDict['EXPOSURETIME']
    return hgeDict

def getMyFileDictRankAdv(myArg):  #check if is a valid 
    myFileDict={}
    myFileDict['specFiles']=[]
    for Arg in myArg:    
        
        if isValidSpecFile(Arg):
            if not Arg.endswith('.info'):
                myFileDict['specFiles'].append(Arg)
       
    return myFileDict

def getMyFileDict(myArg):  #check if is a valid 
    myFileDict={}
    myFileDict['specFiles']=[]
    
    #tmpOpt=''
    for i in range(len(myArg)):
        e=myArg[i]
        # if e.endswith('.Txt') or e.endswith('.SPE') or e.endswith('.mca'):
        if isValidSpecFile(e):
            myFileDict['specFiles'].append(e)

        if e.endswith('.info'):
            print("\n Error: The argument is an Info File. \n --autoPeak option needs an spectrum file to generates the ranges\n")
       
    return myFileDict


functionDict = {"SPE": getDictFromSPE,"mca": getDictFromMCA,"Txt": getDictFromGammaVision,"info":getDictFromInfoFile}

functionDictAdv = {"SPE": getDictFromSPEAdv,"mca": getDictFromMCAAdv,"Txt": getDictFromGammaVisionAdv,"info":getDictFromInfoFile,'hge':getDictFromHGE}
