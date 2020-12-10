#import sys
#import os.path
from os.path import basename
#import re
#import pandas as pd #para imprimir en forma de tabla
#from matplotlib import pyplot as plt
#import numpy as np
#from scipy.optimize import curve_fit
#from scipy import asarray as ar,exp
#from math import sqrt, pi
#import time
#import signal
#import keyboard

# mainPath=sys.path[0] # sources dir
#from myLibs.parsers import *
#from myLibs.gilmoreStats import *
#from myLibs.fitting import *
#from myLibs.autoPeakFunk import *
#from myLibs.QueryDB import *
#from myLibs.plotting import *



def helpFun(argv, functionDict, extBool=False):
    if not extBool:
        print("\n----------------------------------------------------------------------\nSINTAXIS OF histoGe\n----------------------------------------------------------------------\n")
        print("usage:\t%s (-h|--help) #for extended help"%(basename(argv[0])))
        print("\t%s file1.ext [file2.ext ...] #Multifile plot or query database depending of ext"%(basename(argv[0])))
        print("\t%s (-q|--query) iEner fEner #Gammas in range iEner to fEner"%(basename(argv[0])))
        print("\t%s (-i|--isotope) Isotope1 Isotope2 ... #Gammas of Isotopes"%(basename(argv[0])))
        print("\t%s (-p|--parent) Isotope1 Isotope2 ... #Parent and childs isotopes"%(basename(argv[0])))
        print("\t%s (-r|--sub) file1.ext file2.ext  #Substraction of file1 minus file2"%(basename(argv[0])))
        print("\t%s (-s|--sum) file1.ext file2.ext ...  #Addition of all files"%(basename(argv[0])))
        print("\t%s (-t|--test) #Runs a test to probe histoGe"%(basename(argv[0])))
        print("\t%s (-P|--autoPeak) file1.ext #Find automatically the peaks of spectrum"%(basename(argv[0])))
        print("\t%s (-e|--energyRanges) file1.info #Consult all the isotopes found for each peak"%(basename(argv[0])))
        print("\t%s (-c|--stats) file1.info file2.ext #Calculates Gilmore statistics for each peak"%(basename(argv[0])))
        print("\t%s (-f|--hge) file2.ext #Converts the SPE, Txt or mca files to hge format"%(basename(argv[0])))
        print("\t%s (-n,--normInt) Isotope1 Isotope2 ... #isplays relative emission probability from database"%(basename(argv[0])))
        print("\t%s (-R|--Rank|--rank) file1.info #Performs ranking to find most probable isotope"%(basename(argv[0])))
        print("\t%s (--halfSort|--halfRank|--halfrank) file1.info #Performs ranking using half-life"%(basename(argv[0])))
        print("\t%s (--RA|--RankAdv|--rankAdv) File1.info File1.ext #Performs ranking using total net area and the relative emission probability"%(basename(argv[0])))
        print("\t%s (--fuzzy|--fuzzyRank|--fuzzyrank|-z) File1.info File1.ext #Performs ranking using fuzzy logic"%(basename(argv[0])))
        print("\t%s (--chainRank|--ChainRank|-x) File1.info #Performs ranking using decay chains"%(basename(argv[0])))
        print("\t%s (--distance|-d) File1.info File1.ext #Performs ranking calculating the deviation between the mean value of peaks and the energy of the γ-lines"%(basename(argv[0])))
        print("\t%s (--distance|-d) File1.info File1.ext #Performs ranking using γ-line calculating the cumulative distribution function"%(basename(argv[0])))
        print("Valid extensions are:")
        for ext in functionDict:
            print("\t\t%s" %(ext))

    if extBool:
        StrHelp = ("----------------------------------------------------------------------\nEXTENDED HELP "
        "OF histoGe\n----------------------------------------------------------------------\n\nMAIN OPTIONS"
        "\n\nIf no main option are provided then histoGe performs a query to \ndatabase if extension of the "
        "file is .info, in other case, performs\na multiplot with the files provided,e.g.:\n\nhistoGe file1"
        ".extension [file2.extension ...]\n\nThe histoGe\'s main option are:\n\n\t-q|--query: Query the dat"
        "abase to find isotopes that\n\t\tradiate gammas in the range from initial energy\n\t\t(iEner) to f"
        "inal energy (fEner) both in KeV, e.g.:\n\t\t\thistoGe -q 100 101\n\n\t-i|--isotope: Query the data"
        "base to find gammas of each\n\t\tisotopes, e.g.:\n\t\t\thistoGe -i 60Co 241Am\n\n\t-p|--parent: Qu"
        "ery the database looking for the parent \n\t\tisotope and the child or children isotopes, e.g.:\n"
        "\t\t\thistoGe -p 60Co 241Am\n\n\t-r|--sub: Substraction of two sprectra, i.e., File2 is \n\t\tsub"
        "stracted to File1.ext, e.g.:\n\t\t\thistoGe -r File1.ext File2.ext\n\n\t-s|--sum: Sumation of spe"
        "ctra. The option can sum all the\n\t\tspectra that the user need, e.g.:\n\t\t\thistoGe -s File1.e"
        "xt File2.ext\n\n\t-t|--test: Performs a test. If histoGe was installed \n\t\tsuccessfully, then, "
        "test actions are executed\n\t\twithout errors, e.g.:\n\t\t\thistoGe -t\n\n\t-P|--autoPeak: Look f"
        "or peaks in a spectrum and generates\n\t\ta .info file which includes the ranges of the peaks\n\t"
        "\tfound. It works better if the spectrum is rebinned,\n\t\te.g.:\n\t\t\thistoGe --autoPeak File1."
        "ext\n\n\t-e|--energyRanges: Look for all the isotopes that are in the\n\t\tranges specified for e"
        "ach peak in the .info file,\n\t\te.g.:\n\t\t\thistoGe -e File1.info\n\n\t-c|--stats: Calculate th"
        "e Gilmore\'s statistics for each peak\n\t\tin the .info file, e.g.:\n\t\t\thistoGe -c File1.info "
        "File1.ext *\n\n    -f|--hge: Converts the SPE, Txt or mca files to hge format.\n            histo"
        "Ge -f File1.ext\n\n    -n,--normInt: Displays relative emission probability from\n        databas"
        "e.\n            histoGe -n 60Co 241Am\n    \n    -R|--Rank|--rank: Performs a ranking for each pe"
        "ak contained\n\t\tin the .info file in order to find the most probable\n\t\tisotopes that explain"
        " the peaks observed in the\n\t\tspectrum, e.g:\n\t\t\thistoGe -R File1.info\n\n    --halfSort|--h"
        "alfRank|--halfrank: Performs ranking using the\n        half-life of the isotopes.\n            h"
        "istoGe --halfSort File1.info\n\n    --RA|--RankAdv|--rankAdv: Performs ranking using total net ar"
        "ea\n        and the relative emission probability.\n            histoGe  File1.info File1.ext * \n"
        "\n    --fuzzy|--fuzzyRank|--fuzzyrank|-z: Performs ranking using fuzzy\n        logic. It needs to"
        " run an .info and valid spectrum, e.g.:\n            histoGe -z File1.info File1.ext *\n    \n    "
        "--chainRank|--ChainRank|-x\': Performs ranking using decay\n        chains.\n            histoGe -x"
        " File1.info\n\n\t--distance|-d: Performs ranking calculating the deviation between\n        the mean"
        " value of peaks and the energy of the γ-lines.\n    \t\thistoGe -b File1.info File1.ext *\n\n\t--pro"
        "bability|-b: Performs ranking using γ-line calculating \n\t\tthe cumulative distribution function f"
        "or the Gaussian \n\t\tdistribution. It needs an .info file and valid spectrum, e.g.:\n\t\t\thistoGe"
        " -b File1.info File1.ext *\n\n*This option needs and .info file and the spectrum.\n\nSUBOPTIONS OF "
        "MAIN OPTIONS\n\n\tOPTIONS\t\tSUBOPTIONS\n\n\t-h|--help\tNone\t\n\t\n\t-q|--query:\t--all:\tShows all"
        " the results found in a \n\t\t\t\tquery.\n\n\t-i|--isotope:\tNone\n\n\t-p|--parent:\tNone\n\n\t-r|-"
        "-sub:\t--noCal: Indicates that the file is not\n\t\t\t\t calibrated.\n\t\t\t\n\t\t\t--log:\tLogarit"
        "hmic scale in plot.\n\n\t\t\t--noPlot: No plot of the substraction.\n\n\t\t\t--wof:\tWrite output f"
        "ile with result.\n\n\t\t\t--rebin: Channels are rebined.\n\n\t-s|--sum: \t--noCal: Indicates that t"
        "he file is not\n\t\t\t\t calibrated.\n\n\t\t\t--log:\tLogarithmic scale in plot. \n\n\t\t\t--noPlot"
        ": No plot of the substraction.\n\n\t\t\t--wof:\tWrite output file with result.\n\n\t-t|--test:\tNone"
        "\n\n\t-P|--autoPeak:\t--rebin: Channels are rebined.\n\n\t\t\t--wof:\tWrite output file with result."
        "\n\n\t\t\t--noPlot: No plot of the substraction.\n\n\t\t\t--log:\tLogarithmic scale in plot.\n\n\t\t"
        "\t--noCal: Indicates that the file is not\n\t\t\t\t calibrated.\n\n\t-e|--energyRanges: --all: Shows"
        " all the results found in a \n\t\t\t\tquery. \n\n\t\t\t   --wof: Write output file with result.\n\n\t"
        "-c|--stats: \t--wof:\tWrite output file with result.\n\n\t\t\t--noPlot: No plot of the substraction.\n"
        "\n\t\t\t--noCal: Indicates that the file is not\n\t\t\t\t calibrated.\n\n\t\t\t--log:\tLogarithmic s"
        "cale in plot.\n\n    -f|--hge: None\n\n    -n,--normInt: None\n    \n    -R|--Rank|--rank: --wof: "
        "Write output file with result.\n\n\t\t\t--all: Shows all the results found in a \n\t\t\t\tquery.\n "
        "   \n    --halfSort|--halfRank|--halfrank: --all: Displays all\n                isotopes in the list"
        ".\n            \n            --wof: Write output file with result.\n    \n    --RA|--RankAdv|--rank"
        "Adv: --wof: Write output \n                file with result.\n\n            --all: displays all "
        "isotopes in the list.\n\n            --filter: removes those isotopes with relative\n           "
        "     emission probability smaller than 0.05. \n\n    --fuzzy|--fuzzyRank|--fuzzyrank|-z: --wof: Wr"
        "ite output \n                file with result.\n\n            --all: displays all isotopes in the "
        "list.\n\n            --filter: removes those isotopes with relative\n                emission proba"
        "bility smaller than 0.05.\n\n\n    --chainRank|--ChainRank|-x: --wof: Write output \n             "
        "   file with result.\n    \n            --all: displays all isotopes in the list.\n    \n         "
        "   --peak: uses relative emission probability to\n                make ranking.\n\nVALID FILES\n\n"
        "Valid extensions are: .Txt, .SPE, .spe, .mca and .info\n\n\t.Txt files: Format file of gammavision softw"
        "are.\n\n\t.SPE files:  Format file used in Boulby and Snolab \n\t\t\tLaboratories.\n\t\n\t.mca fi"
        "les:  File format of micro-mca or px5 hardware.\n\n\t.info files: File used to store the ranges of"
        " peaks. Usually,\n\t\t\tis generated with --autoPeak main option.\n\t\t\t\t\n\nDOWNLOADABLE FILES\n"
        "\n\tA tutorial file can be consulted in:\n\n\t\thttps://bit.ly/2QL8FYj\n\n\tSome .mca files to try "
        "histoGe can be downloaded from:\n\n\t\thttps://bit.ly/2WNS36h\n\n\tDatabase can be downloaded from:"
        "\n\n\t\thttps://bit.ly/38ip7c1 \n\nEXECUTION OF MULTIPLE COMMANDS\n\nhistoGe can execute several co"
        "mmands in a single execution. \nCommands must be separated by '!' character, for example:\n\n      "
        "  histoGe Command_1 ! Command_2 ! ... ! Command_N\n\n\n\n")
        print(StrHelp)

    return 0
