from matplotlib import pyplot as plt
import numpy as np
from myLibs.miscellaneus import closest
from myLibs.fitting import gaus,emptyFittingDict
import sys

def plotCos():
    t2 = np.arange(0.0, 5.0, 0.02)
    plt.plot(t2, np.cos(2*np.pi*t2), 'r--')
    plt.show()


def myPlotF(myDataList):
    plt.plot(myDataList[0],myDataList[1])
    
def simplePlot(mySubsList,logFlag,noCalFlag,Label=None,show=False,Title=None,ExpoTime=None):
    plt.plot(mySubsList[0],mySubsList[1],label=Label)
    plt.title('Exposure time = ' + str(ExpoTime) + ' s', fontsize='large')
    if logFlag:
        plt.yscale('log')
    if noCalFlag:
            plt.xlabel('Energies [KeV]', fontsize='large')
    else:
            plt.xlabel('Channels', fontsize='large')
    plt.ylabel('Counts', fontsize='large')
    if show == True:
        plt.title(Title, fontsize='large')
        plt.show()

def complexPlot(mySpecialDict,idxPairL,gausdata=None,Anotation=True,logFlag=False,noCalFlag=False,Label=None,Show=True,Title = None,Fill=True,showPeaks=True,FitCurve=True,rebinFlag=False):
    
    if rebinFlag:
        mySpecialList = []
        mySpecialList.append(list(mySpecialDict['theRebinedList'][0]))
        mySpecialList.append(list(mySpecialDict['theRebinedList'][1]))
    else:
        mySpecialList = mySpecialDict['theList']

    if noCalFlag:
        mySpecialDict['calBoolean'] = True

    if mySpecialDict['calBoolean']:
        idxPairLAux = []
        for idx in idxPairL:
            idxL = []
            for idele in idx:
                idxL.append(closest(mySpecialList[0],idele))
            idxPairLAux.append(idxL)
    else:
        idxPairLAux = idxPairL
    
    try:
        if Fill:
            _, ax = plt.subplots()
            for iPV in idxPairLAux:
                if mySpecialDict['calBoolean']:
                    start = mySpecialList[0].index(iPV[0])
                    end = mySpecialList[0].index(iPV[1])
                else:
                    start, end = iPV
                
                ax.fill_between(mySpecialList[0][start:end+1],mySpecialList[1][start:end+1],facecolor='red')
    except:
        sys.stderr.write('\n ERROR: Unexpected error during plotting. try to use --rebin option ')
        pass


    if Title == None:
        Title = ''
    else:
        Title += ', '
    if Label != None:
        plt.gcf().canvas.set_window_title(Label.split('.')[0])
    plt.title(Title + 'Exposure time = ' + str(mySpecialDict["expoTime"]) + ' s', fontsize='large')
    plt.plot(mySpecialList[0],mySpecialList[1],label=Label)
    plt.ylabel('Counts', fontsize='large')

    if logFlag:
        plt.yscale('log')
    if not noCalFlag and mySpecialDict['calBoolean'] == True:
        plt.xlabel('Energies [keV]', fontsize='large')
    else:
        plt.xlabel('Channels', fontsize='large')
    
    if gausdata == None:
        gausdata = emptyFittingDict(len(idxPairLAux))

    try:
        for iPV,gd,e in zip(idxPairLAux,gausdata.values(),gausdata.keys()):
            if mySpecialDict['calBoolean']:
                start = mySpecialList[0].index(iPV[0])
                end = mySpecialList[0].index(iPV[1])
            else:
                #start, end = indexiPV/
                start = mySpecialList[0].index(iPV[0])
                end = mySpecialList[0].index(iPV[1])
            xVals = mySpecialList[0][start:end+1]    
            yVals = mySpecialList[1][start:end+1]    
            NoneFlag = all([ps != None for ps in gd])
            if FitCurve == True and NoneFlag:
                xNpArray = np.array(xVals)
                GausFun = gaus(xNpArray,gd[0],gd[1],gd[2],gd[3])
                plt.plot(xNpArray,GausFun,color='green')
                peakYVals = max(GausFun)
                peakXVals = xVals[list(GausFun).index(peakYVals)]
            else:
                peakYVals = max(yVals)
                peakXVals = xVals[yVals.index(peakYVals)]
            if NoneFlag:
                floatMean = gausdata[e][1]
            else:
                floatMean = peakXVals
            if showPeaks:
                plt.plot(peakXVals, peakYVals, 'ro', markersize=8)
            if Anotation:
                plt.annotate("%s,%2.1f" %(e,floatMean),xy=[peakXVals,peakYVals], fontsize='large', rotation=0)
            else:
                plt.annotate(e, xy=[peakXVals,peakYVals], fontsize='large', rotation=0)
    except:
        sys.stderr.write('\n ERROR: Unexpected error during plotting 2. ')
        if mySpecialDict['calBoolean'] == False:
            sys.stderr.write('\n The File is not calibrated, remember use --noCal options in non calibrated files')
        return 300

    if Show:
        if Label != None:
            plt.legend(loc='best')
        plt.show()
    return 0
