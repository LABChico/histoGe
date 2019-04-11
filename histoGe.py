from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
from math import sqrt, pi

import sys
import os.path

def is_float(n):
    try:
        float_n = float(n)
    except ValueError:
        return False
    else:
        return True

def parseCalData(calStringData):
    myStrArray=calStringData.split(" ")
    myValueArray=[float(val) for val in myStrArray]
    return myValueArray

# def gaus(x,a,x0,sigma):
#     return a*exp(-(x-x0)**2/(2*sigma**2))

def gaus(x,a,x0,sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

def getDictFromInfoFile(infoFileName):
    infoDict={}
    for line in open(infoFileName):
        print(line)
        if line[0] == "#":
            print("skipping comment")
            continue
        newList=line.split()
        infoDict[newList[2]]=[float(val)\
                              for val in newList[0:2]]
        print("newList = ")
        print(newList)
    return infoDict

def getSPEDataList(speFile):
    myCounter=0
    aCoef,bCoef,cCoef=[0.0,0.0,0.0]
    myXvals=[]
    myYvals=[]
    calBool=False

    for line in open(speFile):
        if is_float(line):
            myCounter+=1
            myYvals.append(float(line))
            myXvals.append(myCounter)
        if line.find("$ENER_FIT") != -1:
            calBool=True
            continue
        if calBool:
            #The next line should have calibration data
            calStringData=line
            myValueArray=parseCalData(calStringData)
            print("myValueArray = ", myValueArray)
            aCoef,bCoef,cCoef=myValueArray
            #Assuming E=bCoef*bin+aCoef, as I understood aCoef is
            #always zero (I'm reading it anyway) and I don't know
            #what's cCoef for.
            calBool=False

    #Creating calibrated in Energy bins
    if bCoef != 0:
        eBins=np.array([bCoef*xVal+bCoef for xVal in myXvals])
        return [eBins,myYvals]
    else:
        print("No calibration info, weird. Using normal bins.")
        return [myXvals,myYvals]

def getListFromMCA(mcaFilename):
    mcaList=[]
    str2init = "<<DATA>>"
    str2end = "<<END>>"
    appendBool = False

    for line in open(mcaFilename):
        if line.find(str2init) != -1:
            appendBool = True
            continue

        if line.find(str2end) != -1:
            appendBool = False
            continue

        if appendBool :
            mcaList.append(float(line))

    totalList=[range(len(mcaList)),mcaList]
    return totalList

def getListFromGammaVision(gvFilename):
    gvList=[]
    str2init = "SPECTRUM"
    appendBool = False
    for line in open(gvFilename):
        if line.find(str2init) != -1:
            appendBool = True
        if appendBool:
            lineList=line.split()
            if len(lineList) == 5:
                gvList +=[float(e) for e in lineList[1:]]
    totalList=[range(len(gvList)),gvList]
    return totalList

def getIdxRangeVals(myDataList,xMin,xMax):
    xVals=myDataList[0]
    xMinIdx=myDataList[0]
    xMaxIdx=myDataList[-1]
    for i,x in enumerate(xVals):
        if xMin <= x:
            xMinIdx=i
            break
    #This needs to be optimized!
    for i,x in enumerate(xVals):
        if xMax <= x:
            xMaxIdx=i
            break

    return [xMinIdx,xMaxIdx]

def doFittingStuff(infoDict,myDataList):
    fittingDict={}
    if infoDict == {}: #minor optimization
        return fittingDict
    for e in infoDict:
        xMin,xMax=infoDict[e]
        mean=(xMin+xMax)*0.5
        print("calculated mean = ",mean)

        # mean=1460.68
        print("xMin,xMax = ",xMin,xMax)
        minIdx,maxIdx=getIdxRangeVals(myDataList,\
                                      xMin,xMax)
        xVals=myDataList[0]
        print("minIdx,maxIdx = ",minIdx,maxIdx)
        print("xVals[minIdx],xVals[maxIdx] = ",\
              xVals[minIdx],xVals[maxIdx])
        sigma=1.0 #need to automate this!!
        # a=150
        yVals=myDataList[1]
        a=max(yVals[minIdx:maxIdx])
        print("a = ",a)
        #need to handle cases where fit fails
        popt,pcov = curve_fit(gaus,myDataList[0],\
                          myDataList[1],\
                          p0=[a,mean,sigma])
        print("popt,pcov = ",popt,pcov)
        a,mean,sigma=popt
        print("a,mean,sigma = ",a,mean,sigma)
        myIntegral=a*sigma*sqrt(2*pi)
        fittingDict[e]=[a,mean,sigma,minIdx,maxIdx]
        print("myIntegral = ", myIntegral)
        # return fittingDict
    return fittingDict

def main(args):
    infoDict={}
    #Here put the command line argument
    print("The number of arguments is ", len(args))
    if len(args) == 1:
        print("usage: %s file.SPE [-c data4fits.info]" %(args[0]))
        return 1

    if len(args) == 4:
        print("There are 4 arguments")
        print(args)
        if args[2] != '-c':
            print("error: second argument should be -c")
            return False
        if not os.path.isfile(args[3]):
            print("error: %s does not exist" %(args[3]))
            return False
        infoDict=getDictFromInfoFile(args[3])
        print("infoDict = ")
        print(infoDict)

    # myDataList=getSPEDataList(args[1])
    # myDataList=getListFromMCA(args[1])
    myDataList=getListFromGammaVision(args[1])
    plt.plot(myDataList[0],myDataList[1])

    print()
    print("Entering fittingDict part")
    fittingDict=doFittingStuff(infoDict,myDataList)
    for e in fittingDict:
        a,mean,sigma,minIdx,maxIdx=fittingDict[e]
        xVals=myDataList[0][minIdx:maxIdx]
        plt.plot(xVals,gaus(xVals,a,mean,sigma),\
                 'r:',label=e)
        plt.annotate(e, xy=[mean,a])

    #erase this part?
    # plt.hist(myArr, bins=16384)
    # plt.bar(np.arange(len(li)),li)
    # plt.yscale('log', nonposy='clip')

    plt.show()

if __name__ == "__main__":
   main(sys.argv)
