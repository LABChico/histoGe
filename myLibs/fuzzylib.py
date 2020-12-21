import numpy as np
from scipy import integrate
import sys

def TriangularSet(x,a,b,c):
    if type(x) is list:
        x = np.array(x)

    y = np.copy(x)*0
    if a<b and a<c and b<c:
        for count,valx in enumerate(x):
            if valx >= c:
                y[count] = 0
            elif valx<c and valx>=b:
                y[count] = (-1/(c-b))*(valx-c)
            elif valx<b and valx>=a:
                y[count] = (1/(b-a))*(valx-a)
            else:
                y[count] = 0

    else:
        sys.stderr.write('ERROR: Parameters should satisfy that c>b>a.')
        return 21000

    return y

def TrapezoidalSet(x,a,b,c,d):
    if type(x) is list:
        x = np.array(x)

    y = np.copy(x)*0

    if a<b and a<c and b<c and c<d:
        for count,valx in enumerate(x):
            if valx >= d:
                y[count] = 0
            elif valx<d and valx>=c:
                y[count] = (-1/(d-c))*(valx-d)
            elif valx<c and valx>=b:
                y[count] = 1
            elif valx<b and valx>=a:
                y[count] = (1/(b-a))*(valx-a)
            else:
                y[count] = 0

    else:
        sys.stderr.write('ERROR: Parameters should satisfy that c>b>a.')
        return 21001

    return y

def SigmoidalSet(x,ko,xo):
    if type(x) is list:
        x = np.array(x)

    y = 1/(1+np.exp(-ko*(x-xo)))    
    return y

def GaussianSet(x,mu,sigma):
    if type(x) is list:
        x = np.array(x)

    y = np.exp((-(x-mu)**2)/(2*sigma**2))
    return y


def fuzzyMax(List):
    for count, fuzzySet in enumerate(List):
        if count == 0:
            Out = fuzzySet
        else:
            Out = np.min(Out,fuzzySet)

def fuzzyMin(List):
    for count, fuzzySet in enumerate(List):
        if count == 0:
            Out = fuzzySet
        else:
            Out = np.min(Out,fuzzySet)


def fuzzyinference(PeakRatio,IgR,ECM,numPoints=1e3):
#-------------------------------------------------------------
#The input values are limited to a certain range 
#-------------------------------------------------------------    

    if PeakRatio > 1:
        PeakRatio = 1
    elif PeakRatio < 0:
        PeakRatio = 0

    if IgR > 1:
        IgR = 1
    elif IgR < 0:
        IgR = 0
    
    if ECM > 10:
        ECM = 10
    elif ECM < 0:
        ECM = 0

#-------------------------------------------------------------
#Conjuntos difusos de entrada
#-------------------------------------------------------------    
    
    PeakRatioLow = SigmoidalSet(PeakRatio,-50.0,0.55)
    PeakRatioMed = GaussianSet(PeakRatio,0.7,0.125)
    PeakRatioHigh = SigmoidalSet(PeakRatio,50.0,0.85)

    IgRLow = SigmoidalSet(IgR,-50.0,0.35)
    IgrMed = GaussianSet(IgR,0.5,0.125)
    IgrHigh = SigmoidalSet(IgR,50.0,0.65)

    ECMLow = SigmoidalSet(ECM,-100.0,0.1)
    ECMMed = GaussianSet(ECM,0.2,0.08)
    ECMHigh = SigmoidalSet(ECM,100.0,0.3)

#-------------------------------------------------------------
#Conjuntos difusos de salida
#-------------------------------------------------------------    
    minval = 0
    maxval = 1
    
    Range = np.linspace(minval,maxval,num=int(numPoints))
    ProbVLow = SigmoidalSet(Range,-100.0,0.2)
    ProbLow = GaussianSet(Range,0.3,0.085)
    ProbMed = GaussianSet(Range,0.5,0.085)
    ProbHigh = GaussianSet(Range,0.7,0.085)
    ProbVHigh = SigmoidalSet(Range,100.0,0.8)

#-------------------------------------------------------------
#Reglas difusas
#-------------------------------------------------------------    

    A1 = min(ECMLow,IgrHigh,PeakRatioHigh)
    A2 = min(ECMLow,IgrHigh,PeakRatioMed)
    A3 = min(ECMLow,IgrHigh,PeakRatioLow)
    A4 = min(ECMLow,IgrMed,PeakRatioHigh)
    A5 = min(ECMLow,IgrMed,PeakRatioMed)
    A6 = min(ECMLow,IgrMed,PeakRatioLow)
    A7 = min(ECMLow,IgRLow,PeakRatioHigh)
    A8 = min(ECMLow,IgRLow,PeakRatioMed)
    A9 = min(ECMLow,IgRLow,PeakRatioLow)

    A10 = min(ECMMed,IgrHigh,PeakRatioHigh)
    A11 = min(ECMMed,IgrHigh,PeakRatioMed)
    A12 = min(ECMMed,IgrHigh,PeakRatioLow)
    A13 = min(ECMMed,IgrMed,PeakRatioHigh)
    A14 = min(ECMMed,IgrMed,PeakRatioMed)
    A15 = min(ECMMed,IgrMed,PeakRatioLow)
    A16 = min(ECMMed,IgRLow,PeakRatioHigh)
    A17 = min(ECMMed,IgRLow,PeakRatioMed)
    A18 = min(ECMMed,IgRLow,PeakRatioLow)

    A19 = min(ECMHigh,IgrHigh,PeakRatioHigh)
    A20 = min(ECMHigh,IgrHigh,PeakRatioMed)
    A21 = min(ECMHigh,IgrHigh,PeakRatioLow)
    A22 = min(ECMHigh,IgrMed,PeakRatioHigh)
    A23 = min(ECMHigh,IgrMed,PeakRatioMed)
    A24 = min(ECMHigh,IgrMed,PeakRatioLow)
    A25 = min(ECMHigh,IgRLow,PeakRatioHigh)
    A26 = min(ECMHigh,IgRLow,PeakRatioMed)
    A27 = min(ECMHigh,IgRLow,PeakRatioLow)
    
#-----------------------------------------------------
#Se calculan los consecuentes
#-----------------------------------------------------
    
    C1 = np.fmin(A1,ProbVHigh)
    C2 = np.fmin(A2,ProbHigh)
    C3 = np.fmin(A3,ProbMed)
    C4 = np.fmin(A4,ProbHigh)
    C5 = np.fmin(A5,ProbMed)
    C6 = np.fmin(A6,ProbLow)
    C7 = np.fmin(A7,ProbMed)
    C8 = np.fmin(A8,ProbLow)
    C9 = np.fmin(A9,ProbVLow)

    C10 = np.fmin(A10,ProbHigh)
    C11 = np.fmin(A11,ProbMed)
    C12 = np.fmin(A12,ProbLow)
    C13 = np.fmin(A13,ProbMed)
    C14 = np.fmin(A14,ProbLow)
    C15 = np.fmin(A15,ProbVLow)
    C16 = np.fmin(A16,ProbLow)
    C17 = np.fmin(A17,ProbVLow)
    C18 = np.fmin(A18,ProbVLow)

    C19 = np.fmin(A19,ProbMed)
    C20 = np.fmin(A20,ProbLow)
    C21 = np.fmin(A21,ProbVLow)
    C22 = np.fmin(A22,ProbLow)
    C23 = np.fmin(A23,ProbVLow)
    C24 = np.fmin(A24,ProbVLow)
    C25 = np.fmin(A25,ProbVLow)
    C26 = np.fmin(A26,ProbVLow)
    C27 = np.fmin(A27,ProbVLow)

    CList = [C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,C13,C14,C15,C16,C17,C18,C19,C20,C21,C22,C23,C24,C25,C26,C27]
    Ctot = np.copy(C1)*0
    for Carg in CList:
        Ctot = np.fmax(Ctot,Carg)

    #---------------------------------------------
    #Se hace la desdifusión
    #---------------------------------------------

    IntNum = integrate.simps(Range * Ctot, Range)
    IntDen = integrate.simps(Ctot, Range)

    CrispVal = IntNum/IntDen

    return CrispVal