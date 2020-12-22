"""A simple implementation of the statistical equations that are
presented in Gilmore's book. myDataList is a python list containing
the histogram information lowXVal and uppXVal are values in that can
be floats they are converted to integer indeces so they can be
addressed easely by the closest value on myDataList.

"""

from math import sqrt, pi
import numpy as np
from myLibs.miscellaneus import getIdxRangeVals,fwhm

def gilmoreGrossIntegral(myDataList,lowXVal,uppXVal):
    _,yVals=myDataList
    L,U=getIdxRangeVals(myDataList,lowXVal,uppXVal)
    G=sum(yVals[L:U+1])
    return G

def gilmoreBackground(myDataList,lowXVal,uppXVal):
    xVals,yVals=myDataList
    L,U=getIdxRangeVals(myDataList,lowXVal,uppXVal)
    n=(U-L)+1
    C=yVals
    if U >= len(xVals) - 1:
        U = len(xVals) - 2

    B=n*(C[L-1]+C[U+1])/2 
    return B

def gilmoreNetArea(myDataList,lowXVal,uppXVal): 
    G=gilmoreGrossIntegral(myDataList,lowXVal,uppXVal)
    B=gilmoreBackground(myDataList,lowXVal,uppXVal)
    A=G-B
    return A

def doOutputFile(myFilename,df,dfG):
    myOutputfile=open(myFilename+'_out.put','w')
    myOutputfile.write("Gilmore statistics\n[variables in counts]\n")
    myOutputfile.write(df.to_string())
    myOutputfile.close()
    myOutputfile=open(myFilename+'_out.put','a')
    myOutputfile.write("\nGauss Parameters\n")
    myOutputfile.write(dfG.to_string())
    myOutputfile.close()
    return 0

def gilmoreExtendedBkgExtensionsInt(myDataList,lowXVal,uppXVal,m=1):
    """Takes into account the bins (1 by default) before and after the
region of interest. Default m=1 NetArea=Area+ExtendedBKGD""" 
    _,yVals=myDataList
    L,U=getIdxRangeVals(myDataList,lowXVal,uppXVal)
    n=(U-L)+1                   
    C=yVals
    G=gilmoreGrossIntegral(myDataList,lowXVal,uppXVal)
    A=G-n*(sum(C[L-m:L])+sum(C[U+1:U+m+1]))/(2*m)
    return A

def gilmoreSigma(myDataList,lowXVal,uppXVal):   
    A=gilmoreNetArea(myDataList,lowXVal,uppXVal)
    B=gilmoreBackground(myDataList,lowXVal,uppXVal)
    sigma_A=np.sqrt(A+2*B)
    return sigma_A

def gilmoreExtendedSigma(myDataList,lowXVal,uppXVal,m=5):
    L,U=getIdxRangeVals(myDataList,lowXVal,uppXVal)
    n=U-L
    A=gilmoreNetArea(myDataList,lowXVal,uppXVal)
    B=gilmoreBackground(myDataList,lowXVal,uppXVal)
    extSigma_A=np.sqrt(A+B*(1+n/(2*m)))
    return extSigma_A

def doGilmoreStuff(infoDict,myDataList):
    gilmoreDict={}
    if infoDict == {}:
        return gilmoreDict
    _,yVals=myDataList
    for e in infoDict:
        for i in infoDict[e]:               
            if i == 'start':
                lowXVal=infoDict[e][i]
            elif i == 'end':
                uppXVal=infoDict[e][i]

        minX,maxX=getIdxRangeVals(myDataList,lowXVal,uppXVal)
        max_value = max(yVals[minX:maxX])
        max_index = minX+yVals[minX:maxX].index(max_value)
        G=gilmoreGrossIntegral(myDataList,lowXVal,uppXVal)
        B=gilmoreBackground(myDataList,lowXVal,uppXVal)
        netArea=gilmoreNetArea(myDataList,lowXVal,uppXVal)
        sigma_A=gilmoreSigma(myDataList,lowXVal,uppXVal)

        m=2
        EBA=gilmoreExtendedBkgExtensionsInt(myDataList,lowXVal,uppXVal,m)
        extSigma_A=gilmoreExtendedSigma(myDataList,lowXVal,uppXVal,m)
        myFWHMSigma_A=fwhm(sigma_A)
        myFWHMExtSigma_A=fwhm(extSigma_A)

        gilmoreDict[e]=[e,netArea,EBA,G,B,
                        sigma_A,\
                        extSigma_A,\
                        myFWHMSigma_A,\
                        myFWHMExtSigma_A,\
                        max_index,\
                        max_value]

    return gilmoreDict
