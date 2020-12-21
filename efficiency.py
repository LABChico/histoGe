import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from myLibs.parsers import isValidSpectrumFile,getDictFromSPEAdv,getDictFromMCAAdv,getDictFromGammaVisionAdv,functionDictAdv
from myLibs.miscellaneus import WritehgeFile
from myLibs.fitting import Fun1, R2Fun1, LinearFun, R2LinearFun, PolyFun, R2PolyFun
import sys

def efficencyFun(Command):
    List = Command.copy()
    List.pop(0)
    PlotFlag = False
    if '--Plot' in List or '--plot' in List:
        PlotFlag = True
        List.remove('--Plot')
    
    ValidFileList = []
    EffFile = ''
    for File in List:
        if isValidSpectrumFile(File):
            ValidFileList.append(File)
        elif '.eff' in File:
            EffFile = File

    if EffFile == '':
        sys.stderr.write('An efficiency file for the detector is required.\n')
        return 2000
    else:
        try:
            Effdf = pd.read_csv(EffFile,header=None,names=['energy','eff'])
        except IOError:
            sys.stderr.write('ERROR: The .eff file could not be read.\n')
            return 2001
        else:
            Effenernp = Effdf['energy'].values
            Effnp = Effdf['eff'].values
            PolyCoeff = curve_fit(PolyFun,Effenernp,Effnp,absolute_sigma=True)
            R2PolyCoeff = R2PolyFun(Effenernp,Effnp,PolyCoeff[0])
            Fun1Coeff = curve_fit(Fun1,Effenernp,Effnp,absolute_sigma=True,bounds=([-np.inf,-np.inf,-np.inf,-np.inf],[np.inf,np.inf,np.inf,np.inf]))
            R2Fun1Coeff = R2Fun1(Effenernp,Effnp,Fun1Coeff[0])
            LinearCoeff = curve_fit(LinearFun,Effenernp,Effnp,absolute_sigma=True)
            R2LinearCoeff = R2LinearFun(Effenernp,Effnp,LinearCoeff[0]) 
                
    if PlotFlag:
        XPoly = np.linspace(min(Effenernp),max(Effenernp),num=len(Effenernp)*50)
        R2List = [R2PolyCoeff,R2Fun1Coeff,R2LinearCoeff]
        R2max = max(R2List)
        if R2max == R2PolyCoeff:
            Ypoly = np.polyval(PolyCoeff[0],XPoly)
        elif R2max == R2Fun1Coeff:
            Ypoly = Fun1(XPoly,Fun1Coeff[0][0],Fun1Coeff[0][1],Fun1Coeff[0][2],Fun1Coeff[0][3])
        elif R2max == R2LinearCoeff:
            Ypoly = LinearFun(XPoly,LinearCoeff[0][0],LinearCoeff[0][1])
        plt.plot(XPoly,Ypoly,label='Curve fitting')
        plt.scatter(Effenernp,Effnp,label='Data')
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Energy/keV')
        plt.ylabel('Efficiency')
        plt.title('Detector Efficiency')
        plt.legend(loc='upper right')
        if R2max == R2PolyCoeff:
            textstr = f'Eight grade polynomial.\na1={str(PolyCoeff[0][0])},a2={str(PolyCoeff[0][1])}\na3={str(PolyCoeff[0][2])},a4={str(PolyCoeff[0][3])}\na5={str(PolyCoeff[0][4])},a6={str(PolyCoeff[0][5])}\na7={str(PolyCoeff[0][6])},a8={str(PolyCoeff[0][7])}\nR²={str(R2PolyCoeff)}'
        elif R2max == R2Fun1Coeff:
            textstr = f'f(x) = (ax+b)/(x²+cx+d)\na={str(Fun1Coeff[0][0])}\nb={str(Fun1Coeff[0][1])}\nc={str(Fun1Coeff[0][2])}\nd={str(Fun1Coeff[0][3])}\nR²={str(R2Fun1Coeff)}'
        elif R2max == R2LinearCoeff:
            textstr = f'f(x) = (ax+b)\na={str(LinearCoeff[0][0])}\nb={str(LinearCoeff[0][1])}\nR²={str(R2LinearCoeff)}'
        plt.annotate(textstr,xy=(0, 0.1), xytext=(12, -12),va='bottom',xycoords='axes fraction', textcoords='offset points',fontsize=10)
        plt.show()
        return 0
        
    elif not PlotFlag:
        for File in ValidFileList:
            myExtension = File.split('.')[-1]
            mySpecialDict = functionDictAdv[myExtension](File)
            xVals = np.array(mySpecialDict['theList'][0])
            yVals = np.array(mySpecialDict['theList'][1])
            R2List = [R2PolyCoeff,R2Fun1Coeff,R2LinearCoeff]
            R2max = max(R2List)
            if R2max == R2PolyCoeff:
                EffGe = np.polyval(PolyCoeff[0],xVals)
            elif R2max == R2Fun1Coeff:
                EffGe = Fun1(xVals,Fun1Coeff[0][0],Fun1Coeff[0][1],Fun1Coeff[0][2],Fun1Coeff[0][3])
            elif R2max == R2LinearCoeff:
                EffGe = LinearFun(xVals,LinearCoeff[0][0],LinearCoeff[0][1])
            
            CorrectedSpec = mySpecialDict.copy()
            CorrectedSpec['theList'][1] = yVals/EffGe
            filename = File.split('.')[0] + '_corrected.hge'
            exitcode = WritehgeFile(filename,CorrectedSpec)



        return exitcode






