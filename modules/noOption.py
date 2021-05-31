import sys
from matplotlib import pyplot as plt
from modules.energy import energyFun
from myLibs.parsers import isValidSpecFile, functionDictAdv, getDictFromGammaVision,getDictFromMCA,getDictFromSPE
from myLibs.plotting import simplePlot
from modules.Help import helpFun
from myLibs.miscellaneus import getRebinedList
import os

def noOption(ListOpt):
    labels=[]
    List = ListOpt.copy()
    if '--log' in List:
        logFlag = True
        List.remove('--log')
    else:
        logFlag = False

    if '--noCal' in List:
        noCalFlag = True
        List.remove('--noCal')
    else:
        noCalFlag = False

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

    ListAux = List
    for arg in ListAux:
        if arg[0] == '-':
            List.remove(arg)

    plotFlag = False
    exitcode = 0

    if len(ListOpt) == 0:
        exitcode = helpFun(['None'],['.Txt','.SPE','.mca','.info'],extBool=False)
        return exitcode
    else:
        for arg in List:
            if isValidSpecFile(arg):
                if arg.endswith('.info'):
                    exitcode = energyFun(['--energyRanges',arg])
                
                try:
                    if isValidSpecFile(arg):
                        FileExt = arg.split('.')[-1]
                except:
                    sys.stderr.write('ERROR: Unexpected error. Not a valid file used.')
                    return 110

                ######
                fileName = arg

                if noCalFlag:
                    FileDict = functionDictAdv[FileExt](fileName,True)
                else:
                    FileDict = functionDictAdv[FileExt](fileName)
         
                if rebinFlag:
                    
                    if isinstance(rebinNum, int) == False:
                        rebinNum=5
                        sys.stderr.write("There was no rebin integer detected, the default rebin value used was 5")
                

                    if "theRebinedList" not in FileDict:
                        FileDict["theRebinedList"]=getRebinedList(FileDict["theList"],rebinNum)
                        myDataList = FileDict["theRebinedList"]
                        myDataList[0] = list(myDataList[0])
                        myDataList[1] = list(myDataList[1])
                               
                    else:
                        sys.stderr.write("There was no rebin option detected, the rebin option is --rebin")
                    
                    
                    figName=os.path.splitext(arg)[0].split('/')[-1]
                    mySubsList=myDataList
                    plotFlag = True
                    labels.append(figName)
                    simplePlot(mySubsList,logFlag,FileDict['calBoolean'],Label=labels,show=False,Title=fileName,ExpoTime=FileDict['expoTime'],figTitle=figName)
                    
                ######  
                else:
                    figName = os.path.splitext(arg)[0].split('/')[-1]
                    labels.append(figName)
                    myExtension = fileName.split(".")[-1]
                    if myExtension != 'info':
                        mySubsList = FileDict["theList"]
                        plotFlag = True
                        simplePlot(mySubsList,logFlag,FileDict['calBoolean'],Label=labels,show=False,Title=fileName,ExpoTime=FileDict['expoTime'],figTitle=figName)
            else:
                sys.stderr.write('WARNING: The file ' + arg + ' is invalid. Nothing to do with it.')
                return 90
    if plotFlag:
        plt.show()
    return 0
