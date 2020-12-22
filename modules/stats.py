import sys
import os.path
import pandas as pd 
from matplotlib import pyplot as plt
from myLibs.parsers import getDictFromInfoFile,getDictFromMCA,getDictFromSPE,getDictFromGammaVision,functionDictAdv,isValidSpecFile
from myLibs.fitting import doFittingStuff,gaus
from myLibs.gilmoreStats import doGilmoreStuff,doOutputFile
from myLibs.plotting import complexPlot
from myLibs.miscellaneus import getRebinedList
import sys

def statsFun(ListOpt):
    List = ListOpt.copy()
    List.pop(0)
    if '--noCal' in List:
        noCalFlag = True
        List.remove('--noCal')
    else:
        noCalFlag = False

    if '--noPlot' in List:
        noPlotFlag = True
        List.remove('--noPlot')
    else:
        noPlotFlag = False
    
    if '--wof' in List:
        wofFlag = True
        List.remove('--wof')
    else:
        wofFlag = False
    
    if '--log' in List:
        logFlag = True
        List.remove('--log')
    else:
        logFlag = False

    if '--rebin' in List:
        rebinFlag = True
        List.remove('--rebin')
        rebinNum = None
        for Arg in List:
            try:
                rebinNum = int(Arg)
                List.remove(Arg)
                break
            except:
                continue

    else:
        rebinFlag = False

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
        sys.stderr.write('\nERROR: Unexpected error. Not a valid file used.\n')
        return 110

    if not os.path.isfile(infoFile):
        sys.stderr.write("\nERROR: %s does not exist, are you in the right path?" %(infoFile)+"\n")
        return 111
    if not infoFile.endswith('.info'):
        sys.stderr.write("\nERROR: %s needs a .info extension" % (infoFile)+"\n")
        return 112   
    
    infoDict=getDictFromInfoFile(infoFile)
    try:
         del infoDict['Range']
    except:
        pass
   
    
    if noCalFlag:
        FileDict = functionDictAdv[FileExt](FileName,False)
    else:
        FileDict = functionDictAdv[FileExt](FileName)

    #####
    if rebinFlag:
            
            if isinstance(rebinNum, int) == False:
                rebinNum=5
                sys.stderr.write("\nThere was no rebin integer detected, the default rebin value used was 5\n")
                

            if "theRebinedList" not in FileDict:
                FileDict["theRebinedList"]=getRebinedList(FileDict["theList"],rebinNum)
                myDataList = FileDict["theRebinedList"]
                myDataList[0] = list(myDataList[0])
                myDataList[1] = list(myDataList[1])
                               
    else:
        sys.stderr.write("\nThere was no rebin option detected, the rebin option is --rebin\n")
        myDataList = FileDict['theList']
    
    #####
    
    print("")
    print("Gilmore statistics\n[variables in counts]")
    fittingDict=doFittingStuff(infoDict,myDataList)
    gaussData4Print=[]
    for e in fittingDict:
        a,mean,sigma,c=fittingDict[e][:-3]
        if a == None:
            sys.stderr.write("Fit failed for "+e+" in fiting.py"+"\n")
            continue
        gaussData4Print.append([e,a,mean,sigma,c])
        
    myGaussRows=['#tags','a','mean','sigma','c']
    pd.set_option('display.max_rows', None)
    dfG = pd.DataFrame(gaussData4Print, columns = myGaussRows)

    gilmoreDict=doGilmoreStuff(infoDict,myDataList)
    data4print=[]
    for e in gilmoreDict:
        gL=gilmoreDict[e]
        data4print.append(gL[0:6])
    realXVals=myDataList[0]

    myHStr4=['Tags','NetArea','Area+ExtBkgd','GrossInt','Background','Sigma_A']
    pd.set_option('display.max_rows', len(data4print))
    df = pd.DataFrame([data for data in data4print], columns = myHStr4)
    print(df)
    print('\nGauss Parameters')
    print(dfG)
    
    if wofFlag:
        doOutputFile(FileName,df,dfG)

    count = 0
    AnnotateArg = []
    idxPairL = []
    for e in gilmoreDict:
        a,mean,sigma,c,_,_=[str(val) for val in fittingDict[e][:-1]]
        max_index = gilmoreDict[e][-2]
        max_value = gilmoreDict[e][-1]
        floatMean=fittingDict[e][1]
        idxPairL.append([infoDict[e]['start'],infoDict[e]['end']])
        try:
            AnnotateArg.append(["%s,%2.1f"%(e,floatMean),[realXVals[max_index],max_value]])
        except:
            pass
    
        count += 1
    
    complexPlot(FileDict,idxPairL,fittingDict,AnnotateArg,logFlag=logFlag,noCalFlag=noCalFlag,Show=not(noPlotFlag),FitCurve=True, rebinFlag=rebinFlag)

    return 0