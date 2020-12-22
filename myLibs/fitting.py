"""Curve fitting functions"""
import pandas as pd
import numpy as np
from myLibs.miscellaneus import getIdxRangeVals,fwhm
from math import sqrt, pi
from scipy.optimize import curve_fit
from scipy.stats import norm
import sys

def gaus(x,a,x0,sigma,c=0):
    return a*np.exp(-(x-x0)**2/(2*sigma**2)) + c

def lorentzian(x,x0,w,c):
    return 1/np.pi*(w/2)/((x-x0)**2+(w/2)**2)

def myLine(x,a,b):
    return a*x+b

def getTentParams(x4cal,y4cal):
    C1=x4cal[0]
    C2=x4cal[-1]
    E1=y4cal[0]
    E2=y4cal[-1]
    a=(E2-E1)/(C2-C1)
    b=E1-a*C1
    return a,b

def doInfoFile(Ranges, myFilename):
    lenght = len(Ranges)
    myInfofile=open( myFilename+'.info','w')
    pd.set_option('display.max_rows', lenght)
    df = pd.DataFrame(list(Ranges),columns=['start','end'])
    myInfofile.write(df.to_string())
    myInfofile.close()
    return 0

def doFittingStuff(infoDict,myDataList):
    """Need 2 put this in fitting.py but for some reason fitting fails there"""
    fittingDict={}
    if infoDict == {}: 
        return fittingDict
    for e in infoDict:
        for i in infoDict[e]:               
            if i == 'start':
                xMin=infoDict[e][i]
            elif i == 'end':
                xMax=infoDict[e][i]
        
        mean=(xMin+xMax)*0.5
        minIdx,maxIdx=getIdxRangeVals(myDataList,xMin,xMax)
       
        xVals=myDataList[0]
        sigma=1.0 
        yVals=myDataList[1]
        a=max(yVals[minIdx:maxIdx])
        c=(yVals[minIdx]+yVals[maxIdx])/2
        try:
            popt,_ = curve_fit(gaus,xVals[minIdx:maxIdx],myDataList[1][minIdx:maxIdx],p0=[a,mean,sigma,c])

        except:
            sys.stderr.write("Fit failed for %s in fiting.py" %(e) + "\n")
            fittingDict[e]=[None,None,None,None,None,None,None]
            continue

        a,mean,sigma,c=popt
        myFWHM=fwhm(sigma)
        fittingDict[e]=[a,mean,sigma,c,minIdx,maxIdx,myFWHM]
    return fittingDict

def emptyFittingDict(num):
    fittingDict = {}
    for e in range(0,num,1):
        fittingDict[e]=[None,None,None,None,None,None,None]

    return fittingDict


def Fun1(x,a,b,c,d):
    #return (a*x + b)*np.tanh(c*x + d) + e
    #return (-a*x)/(b+c*np.exp(-d*x)) + e
    return (a*x+b)/(x**2+c*x+d)


def R2Fun1(xdata,ydata,Parm):
    a = Parm[0]
    b = Parm[1]
    c = Parm[2]
    d = Parm[3]
    residuals = ydata- Fun1(xdata,a,b,c,d)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((ydata-np.mean(ydata))**2)
    r_squared = 1 - (ss_res / ss_tot)
    return r_squared


def LinearFun(x,a,b):
    return a*x+b

def R2LinearFun(xdata,ydata,Parm):
    a = Parm[0]
    b = Parm[1]
    residuals = ydata- LinearFun(xdata,a,b)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((ydata-np.mean(ydata))**2)
    r_squared = 1 - (ss_res / ss_tot)
    return r_squared

def PolyFun(x,a,b,c,d,e,f,g,h,i):
    return a*x**8+b*x**7+c*x**6+d*x**5+e*x**4+f*x**3+g*x**2+h*x+i

def R2PolyFun(xdata,ydata,Parm):
    a = Parm[0]
    b = Parm[1]
    c = Parm[2]
    d = Parm[3]
    e = Parm[4]
    f = Parm[5]
    g = Parm[6]
    h = Parm[7]
    i = Parm[8]
    residuals = ydata - PolyFun(xdata,a,b,c,d,e,f,g,h,i)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((ydata-np.mean(ydata))**2)
    r_squared = 1 - (ss_res / ss_tot)
    return r_squared


def MeanDistance(DBInfo,FittingVector):
    Diff = []
    Prob = []
    for Iso in DBInfo:
        try:
            diffVal = Iso[1]-FittingVector[1]
        except:
            return None,None
        else:
            Diff.append([Iso[-1],abs(diffVal)])
            if diffVal > 0:
                diffVal *= -1
            Prob.append([Iso[-1],2*norm.cdf(diffVal,scale=abs(FittingVector[2]))])    
    
    return Diff,Prob
