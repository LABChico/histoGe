import sqlite3
import os

def OpenDatabase(pathfile):
    dbpath = pathfile + '/myDatabase/RadioactiveIsotopes.db'
    conexion = sqlite3.connect(dbpath)
    return conexion

def EnergyRange(conexion,min,max,element = None,order = None):
    Command = 'SELECT ID,Energy,ExEnergy,IgA,ExIntensity,DecayMode,HalfLife,HalfLifeUnit,ExHalfLife,Address,Element FROM Isotopes WHERE Energy >= ' + str(min) + ' and Energy < ' + str(max)
    if element != None:
        Command += ' and Element = ' + "'" + element + "'" 
    
    if order == None:
        cursor = conexion.cursor()
        cursor.execute(Command)
        Isotopes = cursor.fetchall()
        return Isotopes

    elif order == 'ASC' or order == 'DESC':
        cursor = conexion.cursor()
        Command += ' ORDER BY Energy ' + order
        cursor.execute(Command)
        Isotopes = cursor.fetchall()
        return Isotopes

def LookForElement(conexion,element,Field = None,order = None):
    Command = 'SELECT * FROM Isotopes WHERE Element = ' + "'" + element + "'"
    if order == None:
        cursor = conexion.cursor()
        cursor.execute(Command)
        Isotopes = cursor.fetchall()
        return Isotopes

    if (order == 'ASC' or order == 'DESC') and Field == None:
        cursor = conexion.cursor()
        Command += ' ORDER BY Energy ' + order
        cursor.execute(Command)
        Isotopes = cursor.fetchall()
        return Isotopes

    if (order == 'ASC' or order == 'DESC') and Field != None:
        cursor = conexion.cursor()
        Command += ' ORDER BY ' + "'" + Field + "'" + order
        cursor.execute(Command)
        Isotopes = cursor.fetchall()
        return Isotopes

def CloseDatabase(conexion):
    conexion.close()

def Energy2Dict(Dict,Isotope):
    pass
    
def halfLifeUnit(Ele):
    y=31536000
    d=8640
    h=3600
    m=60
    Ele=list(Ele)
    Ele[6]=str(Ele[6])
    if Ele[6].isnumeric() == False:
        x=Ele[6].split('~')
        Ele[6]=x[len(x)-1]
        if Ele[6] == '':
            Ele[6]=0
    Ele[6]=float(Ele[6])

    if Ele[7] == 'y':
        halfLifeInSecs=Ele[6]*y
    elif Ele[7] == 'd':
        halfLifeInSecs=Ele[6]*d
    elif Ele[7] == 'h':
        halfLifeInSecs=Ele[6]*h
    elif Ele[7] == 'm':
        halfLifeInSecs=Ele[6]*m
    elif Ele[7] == 'ms':
        halfLifeInSecs=Ele[6]/1000
    else: halfLifeInSecs=Ele[6]
    
    return halfLifeInSecs 

def stripList(ListDB):
    ListRC = ['*','<','~']
    index = 3
    
    for Element,i in zip(ListDB,range(len(ListDB))):    
        Element = list(Element)
        for character in ListRC:
            Element[index] = Element[index].strip(character)
        Element = tuple(Element)
        ListDB[i] = Element
    return ListDB

def getNormalizedEmissionList(IsoList):
    IsoList = stripList(IsoList)


def GetIntensities(conexion,min,max,element= None,order= None):
    Command = 'SELECT ID,Energy,ExEnergy,IgA,ExIntensity,DecayMode,HalfLife,HalfLifeUnit,ExHalfLife,Address,IgR,Element FROM Isotopes WHERE Energy >= '+ str(min) + ' and Energy < '+ str(max)
    if  element != None:
        Command += ' and Element = '+ "'"+ element + "'"

    if  order == None:
        cursor = conexion.cursor()
        cursor.execute(Command)
        Isotopes = cursor.fetchall()
        return Isotopes
    elif order == 'ASC' or order == 'DESC':
        cursor = conexion.cursor()
        Command += ' ORDER BY Energy '+ order
        cursor.execute(Command)
        Isotopes = cursor.fetchall()
        return  Isotopes

def GetChainAndChild(conexion,Isotope):
    Command = 'SELECT MainChain,ChildIsotopes FROM Isotopes WHERE Element = '+ "'"+ Isotope + "'"
    cursor = conexion.cursor()
    cursor.execute(Command)
    Isotopes = cursor.fetchone()
    if Isotopes == None:
        Isotopes = [Isotope,Isotope]
    return Isotopes

def GetMainChain(conexion,MainChainIso):

    Command = 'SELECT DecayChain FROM DecayChains WHERE Isotope = ' + "'"+ MainChainIso + "'"
    cursor = conexion.cursor()
    cursor.execute(Command)
    MainChain = cursor.fetchone()
    if MainChain == None:
        MainChain = MainChainIso
    return MainChain

def GetIntensities2(conexion,element,order= None):
    Command = 'SELECT ID,Energy,ExEnergy,IgA,ExIntensity,IgR,Element FROM Isotopes WHERE Element = '+ "'"+ element + "'"

    if  order == None:
        cursor = conexion.cursor()
        cursor.execute(Command)
        Isotopes = cursor.fetchall()
        return Isotopes
    elif order == 'ASC' or order == 'DESC':
        cursor = conexion.cursor()
        Command += ' ORDER BY Energy '+ order
        cursor.execute(Command)
        Isotopes = cursor.fetchall()
        return  Isotopes

def chaintoList(ChainStr):
    writeFlag = True
    ChainList = []
    AuxStr = ''
    for Char in ChainStr:
        if Char == '#':
            ChainList.append(AuxStr)
            AuxStr = ''
            writeFlag = False
        elif Char == '&':
            if writeFlag == False:
                writeFlag = True
        else:
            if writeFlag == True:
                AuxStr += Char
    return ChainList


