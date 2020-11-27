#!/usr/bin/python3

import sys
from os import fork
#import os.path
#from os.path import basename
#import re
import pandas as pd #para imprimir en forma de tabla
from matplotlib import pyplot as plt
#import numpy as np
#from scipy.optimize import curve_fit
#from scipy import asarray as ar,exp
#from math import sqrt, pi
#import time
#import signal
#import keyboard

# mainPath=sys.path[0] # sources dir
from myLibs.parsers import MultiCommandParser,MainOptD
from myLibs.miscellaneus import TryFork
#from myLibs.gilmoreStats import *
#from myLibs.fitting import *
#from myLibs.autoPeakFunk import *
#from myLibs.QueryDB import *
#from myLibs.plotting import *
from autoPeak import autoPeakFun
from Help import helpFun
#from shortHelp import shortHelpFun
from query import QueryFun
from test import TestFun
from isotope import isotopeFun
from Sum import SumFun
from rank import rankFun
from Sub import SubFun
from energy import energyFun
from stats import statsFun
from noOption import noOption
from isoparent import Parent
from normintensity import NormIntensity
from DataFile2hgeFile import DataFile2hgeFile
from efficiency import efficencyFun
from rankAdv import rankAdvFun
from fuzzyrank import fuzzyrankFun
from halfSort import halfSortFun
from chainRank import ChainRankFun
from rank_imp import rankImp
from rank_dist import rankDist
from rank_prob import rankProb

def main(argv):

    #------------------------------------------------------
    #Simple instruction parser code
    #Commands = CommandParser(argv)
    #Command = Commands[0]
    #------------------------------------------------------
    #This two lines are the multiinstruction parser code
    #This code is in a testing phase and should be used with care
    #To switch to the Simple parser just comment two lines above
    # and uncomment both lines of the Simple instructions parser code
    Commands = MultiCommandParser(argv)
    lenCommands = len(Commands) - 1
    for ps,Command in enumerate(Commands):
    #------------------------------------------------------
        if 'shorthelp' in Command:
        #if Command == 'shorthelp':
            exitcode = helpFun(argv,['.Txt','.SPE','.mca','.info'],extBool=False)
            if  ps == lenCommands:
                return exitcode

        elif Command[0] in MainOptD['help']:
            exitcode = helpFun(argv,['.Txt','.SPE','.mca','.info'],extBool=True)
            if  ps == lenCommands:
                return exitcode

        elif Command[0] in MainOptD['autoPeak']:
            pid = TryFork()
            if pid == 0:
                exitcode = autoPeakFun(Command)
            else:
                exitcode = 0
            if  ps == lenCommands:
                return exitcode

        elif Command[0] in MainOptD['query']:
            exitcode = QueryFun(Command)
            if  ps == lenCommands:
                return exitcode

        elif Command[0] in MainOptD['test']:
            pid = TryFork()
            if pid == 0:
                exitcode = TestFun()
            else:
                exitcode = 0
            if  ps == lenCommands:
                return exitcode

        elif Command[0] in MainOptD['isotope']:
            exitcode = isotopeFun(Command)
            if  ps == lenCommands:
                return exitcode

        elif Command[0] in MainOptD['sum']:
            pid = TryFork()
            if pid == 0:
                exitcode = SumFun(Command)
            else:
                exitcode = 0
            if  ps == lenCommands:
                return exitcode

        elif Command[0] in MainOptD['rank']:
            #exitcode = rankFun(Command)
            exitcode = rankImp(Command)
            return exitcode

        elif Command[0] in MainOptD['sub']:
            pid = TryFork()
            if pid == 0:
                exitcode = SubFun(Command)
            else:
                exitcode = 0
            if  ps == lenCommands:
                return exitcode

        elif Command[0] in MainOptD['stats']:
            pid = TryFork()
            if pid == 0:
              exitcode = statsFun(Command)
            else:
                exitcode = 0
            if  ps == lenCommands:
                return exitcode

        elif Command[0] in MainOptD['energy']:
            exitcode = energyFun(Command)
            if  ps == lenCommands:
                return exitcode

        elif Command[0] in MainOptD['parent']:
            exitcode = Parent(Command)
            if  ps == lenCommands:
                return exitcode

        elif Command[0] in MainOptD['normint']:
            exitcode = NormIntensity(Command)
            if  ps == lenCommands:
                return exitcode

        elif Command[0] in MainOptD['2file']:
            exitcode = DataFile2hgeFile(Command)
            if  ps == lenCommands:
                return exitcode

        elif Command[0] in MainOptD['efficiency']:
            pid = TryFork()
            if pid == 0:
                exitcode = efficencyFun(Command)
            else:
                exitcode = 0
            if  ps == lenCommands:
                return exitcode

        elif Command[0] in MainOptD['rankAdv']:
            exitcode = rankAdvFun(Command)
            return exitcode

        elif Command[0] in MainOptD['fuzzy']:
            exitcode = fuzzyrankFun(Command)
            return exitcode

        elif Command[0] in MainOptD['halfSort']:
            exitcode = halfSortFun(Command)
            return exitcode

        elif Command[0] in MainOptD['chainRank']:
            exitcode = ChainRankFun(Command)
            return exitcode

        elif Command[0] in MainOptD['distance']:
            exitcode = rankDist(Command)
            return exitcode
        elif Command[0] in MainOptD['probability']:
            exitcode = rankProb(Command)
            return exitcode


        else:
            pid = TryFork()
            if pid == 0:
                exitcode = noOption(Command)
            else:
                exitcode = 0
            if  ps == lenCommands:
                return exitcode

if __name__ == "__main__":
    argv = sys.argv
    exitcode = main(argv)
    exit(code=exitcode)
