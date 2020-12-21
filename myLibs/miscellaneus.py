"""Just a set of useful functions"""
from os import fork
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import sys
#from myLibs.fitting import gaus
#from myLibs.fitting import gaus
###### MATPLOTLIB CONF #########################
SMALL_SIZE = 15
MEDIUM_SIZE = 22
BIGGER_SIZE = 30

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title



#################################################

def TryFork():
    try:
        pid = fork()
    except:
        pid = 0
    return pid

def is_float(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return True

def getIdxRangeVals(myDataList,xMin,xMax):
    xVals=myDataList[0]
    xMinIdx=xVals[0]
    xMaxIdx=xVals[-1]
    MinFlag = True
    MaxFlag = True
    for i,x in enumerate(xVals):
        if xMin <= x:
            xMinIdx = i
            MinFlag = False
            break
    #This needs to be optimized!
    for i,x in enumerate(xVals):
        if xMax <= x:
            xMaxIdx = i
            MaxFlag = False
            break
    if MinFlag:
        xMinIdx = 0

    if MaxFlag:
        xMaxIdx = len(xVals) - 1

    return [xMinIdx,xMaxIdx]

def fwhm(sigma):
    return 2*np.sqrt(2*np.log(2))*sigma

def getRescaledList(myDataList,tRatio):
    newYVals=[yVal*tRatio for yVal in myDataList[1]]
    newDataList=[myDataList[0],newYVals]
    return newDataList

def getSubstractedList(myDataList,myRescaledList):
    dataYVals=myDataList[1]
    rescaledYVals=myRescaledList[1]
    subsYVals=[datY-rescY for datY,rescY in zip(dataYVals,rescaledYVals)]
    return [myDataList[0],subsYVals]

def getRebinedList(myDataList,rebInt):
    xVals,yVals=myDataList
    assert (len(xVals) == len(yVals)), "Can't continue if arrays are not the same size!!"
    newYVals = np.add.reduceat(yVals, np.arange(0, len(yVals), rebInt))
    newXVals = xVals[rebInt//2::rebInt] #numpy slice.
    if len(newYVals) != len(newXVals):
        #If here then only 1 xValue was truncated.
        res=len(xVals)%rebInt
        theIdx=(len(xVals)//rebInt)*rebInt+res//2
        newXVals=np.append(newXVals,[xVals[theIdx]])
    return [newXVals,newYVals]

def closest(lst, K): 
    value = lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]
    return value

def WriteOutputFile(mySubsDict,myFilename,Title):
    try:
        X1 = mySubsDict['theList'][0]
        Y1 = mySubsDict['theList'][1]
    except TypeError:
        X1 = mySubsDict[0]
        Y1 = mySubsDict[1]
    File = open(myFilename,'a+')
    File.write('#-------------------------------------\n# This is the sum of spectra: ' + Title + '\n--------------------------------------------\n\n')
    try:
        if mySubsDict['calBoolean']:
            DataDict = {'Energy (keV)':X1,'Counts':Y1}
        else:
            DataDict = {'Channels':X1,'Counts':Y1}
    except TypeError:
            DataDict = {'Channels':X1,'Counts':Y1}

    df = pd.DataFrame(DataDict)
    File.write(df.to_string())
    File.close()

def WriteOutputFileRR(myFilename,df,iEner,fEner):
    File = open(myFilename,'a+')
    File.write('#-------------------------------------\n# These are the results of searching energies between: ' + str(iEner) + 'keV and ' + str(fEner) +' keV.\n--------------------------------------------\n\n')
    File.write(df.to_string()+'\n')
    File.close()

def WritehgeFile(myFilename,myDict):
    #CategoryList = ['DATE','EQUIPMENT','EXPOSURETIME','CALIBRATION','CHANNELS','GAIN','DATA']

    #------------------------------------------------------------
    #Write header of .hge file
    #------------------------------------------------------------
    FileStr = '#--------------------------------------------------------\n# .hge file format is the stantard type file to be used \n# with histoGe software.\n#--------------------------------------------------------\n'
    myFilename = myFilename.split('.')[0]
    #------------------------------------------------------------
    #Write aquisition parameters of .hge file
    #------------------------------------------------------------
    try:
        DataStr = 'DATE: ' + List2str(myDict['date']) + '\n'
    except:
        DataStr = 'DATE: Not Available\n' 
    finally:
        FileStr += DataStr
    
    try:
        DataStr = 'EQUIPMENT: ' + List2str(myDict['equipment']) + '\n'   
    except:
        DataStr = 'EQUIPMENT: Not Available\n'
    finally:
        FileStr += DataStr

    try:
        DataStr = 'EXPOSURETIME: ' + List2str(myDict['expoTime']) + '\n'
    except:
        DataStr = 'EXPOSURETIME: Not Available\n' 
    finally:        
        FileStr += DataStr

    try:
        DataStr = 'CALIBRATION: ' + List2str(myDict['calBoolean']) + '\n'
    except:
        DataStr = 'CALIBRATION: Not Available\n' 
    finally:
        FileStr += DataStr

    try:
        DataStr = 'CHANNELS: ' + List2str(myDict['channel']) + '\n'
    except:
        DataStr = 'CHANNELS: Not Available\n'
    finally:
        FileStr += DataStr

    try:
        DataStr = 'GAIN: ' + List2str(myDict['gain']) + '\n'
    except:
        DataStr = 'GAIN: Not Available\n'
    finally:
        FileStr += DataStr

    try:
        DataStr = 'CALIBRATIONPOINTS: ' + List2str(myDict['calpoints']) + '\n'
    except:
        DataStr = 'CALIBRATIONPOINTS: Not Available\n'
    else:
        FileStr += DataStr

    try:
        Data = myDict['theList']
    except:
        sys.stderr.write('ERROR while loading the data.')
        FileStr += 'ERROR loading the DATA. This file was generated but it is useless.\nPlease check your original file.'
        FileObj = open(myFilename + '.bad','w+')
        FileObj.write(FileStr)
        FileObj.close()
        return 1001
    else:
        FileStr += 'DATA\n'
        Count = 1
        X = Data[0]
        Y = Data[1]
        for Xo, Yo in zip(X,Y):
            DataStr = str(Count)+','+str(Xo)+','+str(Yo)+'\n'
            FileStr += DataStr
            Count += 1
        FileStr += 'ENDDATA'
    try:
        Data = myDict['theRebinedList']
        
    except:
        pass
    else:
        FileStr += 'REBINNEDDATA\n'
        Count = 1
        X = Data[0]
        Y = Data[1]
        for Xo, Yo in zip(X,Y):
            DataStr = str(Count)+','+str(Xo)+','+str(Yo)+'\n'
            FileStr += DataStr
            Count += 1
        FileStr += 'ENDREBINEDDATA'
        try:
            RebinFactor = myDict['REBINFACTOR']
        except:
            FileStr += 'REBINFACTOR: Not Available'
        else:
            try:
                FileStr += 'REBINFACTOR: ' + int(RebinFactor) + '\n'
            except:
                FileStr += 'REBINFACTOR: Lost during saving'
    #------------------------------------------------------------
    #Write and close data to .hge file
    #------------------------------------------------------------

    FileObj = open(myFilename +'.hge','w+')
    FileObj.write(FileStr)
    FileObj.close()
    return 0

def List2str(List):
    String = ''
    for idx,ele in enumerate(List):
        if idx == len(List)-1:
            String += str(ele) + '\n'
        else:
            String += str(ele) + ', '
    
    return String

def findminPos(List):
    flag = False
    for ele in List:
        if ele >= 0:
            flag = True
            break        
    if not flag:
        ele = 0
    return ele 

def removeDuplicates(listofElements):
    
    # Create an empty list to store unique elements
    uniqueList = []
    
    # Iterate over the original list and for each element
    # add it to uniqueList, if its not already there.
    for elem in listofElements:
        if elem not in uniqueList:
            uniqueList.append(elem)
    
    # Return the list of unique elements        
    return uniqueList

####### Some basic database values taken from the isonav #######
####### Will probably use in the future the whole database #####

listStuff=['n','H','He','Li','Be','B','C','N','O','F','Ne',
           'Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca',
           'Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn',
           'Ga','Ge','As','Se','Br','Kr','Rb','Sr','Y','Zr',
           'Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn',
           'Sb','Te','I','Xe','Cs','Ba','La','Ce','Pr','Nd',
           'Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb',
           'Lu','Hf','Ta','W','Re','Os',
           'Ir','Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn',
           'Fr','Ra','Ac','Th','Pa','U','Np','Pu','Am','Cm',
           'Bk','Cf','Es','Fm','Md','No','Lr',
           'Rf','Db','Sg','Bh','Hs','Mt','Ds','Rg',
           'Cn','Ed','Fl','Ef','Lv','Eh','Ei']

nameDict={'n':"neutron",'H':"Hydrogen","He":"Helium","Li":"Lithium",
          "Be":"Berillium","B":"Boron","C":"Carbon","N":"Nitrogen",
          "O":"Oxygen","F":"Fluorine","Ne":"Neon","Na":"Sodium",
          "Mg":"Magnesium","Al":"Aluminum","Si":"Silicon",
          "P":"Phosphorus","S":"Sulfur","Cl":"Chlorine","Ar":"Argon",
          "K":"Potassium","Ca":"Calcium","Sc":"Scandium",
          "Ti":"Titanium","V":"Vanadium","Cr":"Chromium",
          "Mn":"Manganese","Fe":"Iron","Co":"Cobalt","Ni":"Nickel",
          "Cu":"Copper","Zn":"Zinc","Ga":"Gallium","Ge":"Germanium",
          "As":"Arsenic","Se":"Selenium","Br":"Bromine","Kr":"Krypton",
          "Rb":"Rubidium","Sr":"Strontium","Y":"Yttrium","Zr":"Zirconium",
          "Nb":"Niobium","Mo":"Molybdenum","Tc":"Technetium",
          "Ru":"Ruthenium","Rh":"Rhodium","Pd":"Palladium","Ag":"Silver",
          "Cd":"Cadmium","In":"Indium","Sn":"Tin","Sb":"Antimony",
          "Te":"Tellurium","I":"Iodine","Xe":"Xenon","Cs":"Cesium",
          "Ba":"Barium","La":"Lanthanum","Ce":"Cerium","Pr":"Praseodymium",
          "Nd":"Neodymium","Pm":"Promethium","Sm":"Samarium",
          "Eu":"Europium","Gd":"Gadolinium","Tb":"Terbium","Dy":"Dysprosium",
          "Ho":"Holmium","Er":"Erbium","Tm":"Thulium","Yb":"Ytterbium",
          "Lu":"Lutetium","Hf":"Hafnium","Ta":"Tantalum","W":"Tungsten",
          "Re":"Rhenium","Os":"Osmium","Ir":"Iridium","Pt":"Platinum",
          "Au":"Gold","Hg":"Mercury","Tl":"Thallium","Pb":"Lead",
          "Bi":"Bismuth","Po":"Polonium","At":"Astatine","Rn":"Radon",
          "Fr":"Francium","Ra":"Radium","Ac":"Actinium","Th":"Thorium",
          "Pa":"Protactinium","U":"Uranium","Np":"Neptunium","Pu":"Plutonium",
          "Am":"Americium","Cm":"Curium","Bk":"Berkellium",
          "Cf":"Californium","Es":"Einsteinium","Fm":"Fermium","Md":"Mendelevium",
          "No":"Nobelium","Lr":"Lawrencium","Rf":"Rutherfordium",
          "Db":"Dubnium","Sg":"Seaborgium","Bh":"Bohrium","Hs":"Hassium",
          "Mt":"Meitnerium","Ds":"Darmstadtium","Rg":"Roentgenium",
          "Cn":"Copernicium","Ed":"Ununtrium","Fl":"Flerovium","Ef":"Ununpentium",
          "Lv":"Livermorium","Eh":"Ununseptium","Ei":"Ununoctium"}

#######################################
