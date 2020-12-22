import sys
import pandas as pd #para imprimir en forma de tabla
from matplotlib import pyplot as plt
import math
from myLibs.parsers import functionDictAdv, getDictFromSPE, getDictFromMCA, getDictFromGammaVision,isValidSpecFile, getMyFileDict
from myLibs.plotting import complexPlot
from myLibs.miscellaneus import getRebinedList,findminPos
from scipy.signal import savgol_filter

def isFloat(myStr):
    try:
        float(myStr)
    except ValueError:
        return False
    return True


def peakRangeFinder(theList):
    energy,counts=theList
    maxIdx=len(energy)
    sg = savgol_filter(counts, 5, 1)

    indRange=[]

    data = [0]*len(counts)
    filtered = [0]*len(counts)
    std = [0]*len(counts)
    sub = [0]*len(counts)

    overT=False
    start=0
    end=0
    
    i=0

    for i in range(0,len(counts),1):
        data[i]=float(counts[i])
        filtered[i]=float(sg[i])
        sub[i] = data[i] - filtered[i]
        if filtered[i] > 0:
            std[i] = math.sqrt(filtered[i])
        else:
            std[i] = 0
        if sub[i] > 3*std[i]  and not overT:
            start=i
            overT = True
        elif sub[i] < 3*std[i] and overT:
            overT = False
            end = i-1

            if start != 0:
                start-=1
            if end < maxIdx:
                end+=1
            indRange.append([start,end])

    return indRange

def autoPeakFun(Command):

    noCalFlag = False
    logFlag = False
    noPlotFlag = False
    rebinFlag = False
    List = Command.copy()
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


    myFileDict=getMyFileDict(List)
    
    myFilename=myFileDict['specFiles'][0]
              
    if len(myFileDict['specFiles']) > 1:
       
        sys.stderr.write(' Error: to many files to do autopeak\n')
       
    else:   
        myExtension = myFilename.split(".")[-1] #verifies the file extention
        if myExtension == 'info':
            sys.stderr.write('The file cannot be an info file.\n')
            return 120

        
        mySpecialDict = functionDictAdv[myExtension](myFilename,noCalFlag) #fill de dictionary
                                                                   #from data file
        
        if (noCalFlag == False) and (mySpecialDict["calBoolean"] == False):
            noCalFlag = True
            sys.stderr.write("Note: the file " + myFilename + " is not calibrated, please don't forget use --noCal option\n")

        if rebinFlag:
            
            if isinstance(rebinNum, int) == False:
                rebinNum=5
                sys.stderr.write("There was no rebin integer detected, the default rebin value used was 5\n")
                

            if "theRebinedList" not in mySpecialDict:
                mySpecialDict["theRebinedList"]=getRebinedList(mySpecialDict["theList"],rebinNum)
                myDataList = mySpecialDict["theRebinedList"]
                
                idxPairL = peakRangeFinder(myDataList)
                energyArr = myDataList[0]
                Ranges=[]
                for idxR in idxPairL:
                    start,end = idxR
                    iEner = energyArr[start]
                    fEner = energyArr[end]
                    Ranges.append([iEner,fEner])
                                    
        else:
            sys.stderr.write("There was no rebin option detected, the rebin option is --rebin\n")
            myDataList = mySpecialDict["theList"]
                
            idxPairL = peakRangeFinder(myDataList)
            energyArr = myDataList[0]
            Ranges=[]
            for idxR in idxPairL:
                start,end = idxR
                iEner = energyArr[start]
                fEner = energyArr[end]
                Ranges.append([iEner,fEner])
        if wofFlag:              
            minX = findminPos(myDataList[0])
            maxX = max(myDataList[0])
            myInfofile=open(myFilename+'.info','w')
            RangeStr = '#SPECRANGE: ' + str(minX) + ',' + str(maxX) + '\n' 
            pd.set_option('display.max_rows', len(Ranges))
            df = pd.DataFrame(list(Ranges),columns=['start','end'])
            myInfofile.write(RangeStr + df.to_string())
            myInfofile.close()
            print('\n'+myFilename+'.info was created\n')
            print('\n-----------------------------------\nThe information of the .info file is the next:\n')
            print(RangeStr + df.to_string())

        else:
            df = pd.DataFrame(list(Ranges),columns=['start','end'])
            print(df.to_string())

        PlotTitle = 'Peaks in '+ myFilename.split('/')[-1]
        PlotLabel = myFilename.split('/')[-1]

        if noPlotFlag == False: 
            complexPlot(mySpecialDict,Ranges,logFlag=logFlag,noCalFlag=noCalFlag,Label=PlotLabel,Title=PlotTitle,FitCurve=False,rebinFlag=rebinFlag)
               
        return 0