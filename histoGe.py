#!/usr/bin/python3

import sys

from myLibs.parsers import MultiCommandParser,MainOptD
from myLibs.miscellaneus import TryFork

from modules.autoPeak import autoPeakFun
from modules.Help import helpFun
from modules.query import QueryFun
from modules.test import TestFun
from modules.isotope import isotopeFun
from modules.Sum import SumFun
from modules.rank import rankFun
from modules.Sub import SubFun
from modules.energy import energyFun
from modules.stats import statsFun
from modules.noOption import noOption
from modules.isoparent import Parent
from modules.normintensity import NormIntensity
from modules.DataFile2hgeFile import DataFile2hgeFile
from modules.efficiency import efficencyFun
from modules.rankAdv import rankAdvFun
from modules.fuzzyrank import fuzzyrankFun
from modules.halfSort import halfSortFun
from modules.chainRank import ChainRankFun
from modules.rank_imp import rankImp
from modules.rank_dist import rankDist
from modules.rank_prob import rankProb

def main(argv):

    #------------------------------------------------------
    #Simple instruction parser code
    #Commands = CommandParser(argv)
    #Command = Commands[0]
    #------------------------------------------------------
    #This two lines are the multiinstruction parser code
    #To switch to the Simple parser just comment two lines above
    # and uncomment both lines of the Simple instructions parser code
    Commands = MultiCommandParser(argv)
    lenCommands = len(Commands) - 1
    for ps,Command in enumerate(Commands):
    #------------------------------------------------------
        if 'shorthelp' in Command:
            if Command == 'shorthelp':
                exitcode = helpFun(argv,['.Txt','.SPE', '.spe','.mca','.info'],extBool=False)
            if  ps == lenCommands:
                return exitcode

        elif Command[0] in MainOptD['help']:
            exitcode = helpFun(argv,['.Txt','.SPE','.spe', '.mca','.info'],extBool=True)
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
            print("bandera")
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
