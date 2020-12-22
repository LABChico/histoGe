import sys
import os.path
import pandas as pd
from myLibs.QueryDB import OpenDatabase, EnergyRange, CloseDatabase


def QueryFun(ListOpt):
    List = ListOpt.copy()
    List.pop(0)
    pathfile = os.path.realpath(__file__)
    pathfile = pathfile.replace('/modules/query.py','')
    conexion = OpenDatabase(pathfile)
    if '--all' in List:
        allflag = True
        List.remove('--all')
    else:
        allflag = False
    if len(List) == 2:
        iEner = List[0]
        fEner = List[1]
    else:
        print('')
        return 30
    
    try:
        iEner=float(iEner)
        fEner=float(fEner)
    except ValueError:
        sys.stderr.write('ERROR: Argument or arguments cannot be converted to float.')
        return 31
    if iEner > fEner:
        iEnerAux = iEner
        iEner = fEner
        fEner = iEnerAux
        del iEnerAux

    DBInfo = EnergyRange(conexion,iEner,fEner)
    print('\nThe energy range consulted is %.2f keV to %.2f keV.\n' % (iEner,fEner))
    if len(DBInfo) != 0:
        Eg , Ig , Decay, Half , Parent = [],[],[],[],[]
        for Ele in DBInfo:
            Eg.append(str(Ele[1])+' ('+str(Ele[2])+')')
            Ig.append(str(Ele[3])+' ('+str(Ele[4])+')')
            Decay.append(Ele[5])
            Half.append(str(Ele[6]) +' ' +str(Ele[7]) + ' ('+str(Ele[8])+')')
            Parent.append(Ele[10])
        pd.set_option('display.max_rows', 30)

        if allflag:
            pd.set_option('display.max_rows', None)
        else:
            pd.set_option('display.max_rows', len(Ele))

        df = pd.DataFrame(list(zip(Eg,Ig,Decay,Half,Parent)),columns=['Eg [keV]','Ig (%)','Decay mode','Half Life','Parent'])#crea  la tabla
        print(df)

    print("\n%d results were found" %(len(DBInfo)))
    CloseDatabase(conexion)
    return 0
