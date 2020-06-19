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
    print("\n----------------------------------------------------------------------\nSINTAXIS OF histoGe\n----------------------------------------------------------------------\n")
    print("usage:\t%s (-h|--help) #for extended help"%(basename(argv[0])))
    print("\t%s file1.extension [file2.extension ...] #Multifile plot or query database depending of extension"%(basename(argv[0])))
    print("\t%s (-q|--query) iEner fEner #Gammas in range iEner to fEner"%(basename(argv[0])))
    print("\t%s (-i|--isotope) Isotope1 Isotope2 ... #Gammas of Isotopes"%(basename(argv[0])))
    print("\t%s (-p|--parent) Isotope1 Isotope2 ... #Parent and childs isotopes"%(basename(argv[0])))
    print("\t%s (-r|--sub) file1.extension file2.extension  #Substraction of file1 minus file2"%(basename(argv[0])))
    print("\t%s (-s|--sum) file1.extension file2.extension ...  #Addition of all files"%(basename(argv[0])))
    print("\t%s (-t|--test) #Runs a test to probe histoGe"%(basename(argv[0])))
    print("\t%s (-P|--autoPeak) file1.extension #Find automatically the peaks of spectrum"%(basename(argv[0])))
    print("\t%s (-R|--Rank|--rank) file1.info #Performs ranking to find most probable isotope"%(basename(argv[0])))
    print("\t%s (-e|--energyRanges) file1.info #Consult all the isotopes found for each peak"%(basename(argv[0])))
    print("\t%s (-c|--stats) file1.info file2.extension #Calculates Gilmore statistics for each peak"%(basename(argv[0])))
    if not extBool:
        print("Valid extensions are:")
        for ext in functionDict:
            print("\t\t%s" %(ext))

    if extBool:
        StrHelp = ("\n\n----------------------------------------------------------------------\n"
        "EXTENDED HELP OF histoGe\n----------------------------------------------------------------------\n\n"
        "MAIN OPTIONS\n\nIf no main option are provided then histoGe performs a query to \ndatabase if extensi"
        "on of the file is .info, in other case, performs\na multiplot with the files provided,e.g.:\n\nhistoG"
        "e file1.extension [file2.extension ...]\n\nThe histoGe's main option are:\n\n\t-q|--query: Query the "
        "database to find isotopes that\n\t\tradiate gammas in the range from initial energy\n\t\t(iEner) to f"
        "inal energy (fEner) both in KeV, e.g.:\n\t\t\thistoGe -q 100 101\n\n\t-i|--isotope: Query the databas"
        "e to find gammas of each\n\t\tisotopes, e.g.:\n\t\t\thistoGe -i 60Co 241Am\n\n\t-p|--parent: Query th"
        "e database looking for the parent \n\t\tisotope and the child or children isotopes, e.g.:\n\t\t\thist"
        "oGe -p 60Co 241Am\n\n\t-r|--sub: Substraction of two sprectra, i.e., File2 is \n\t\tsubstracted to Fi"
        "le1.ext, e.g.:\n\t\t\thistoGe -r File1.ext File2.ext\n\n\t-s|--sum: Sumation of spectra. The option c"
        "an sum all the\n\t\tspectra that the user need, e.g.:\n\t\t\thistoGe -s File1.ext File2.ext\n\n\t-t|-"
        "-test: Performs a test. If histoGe was installed \n\t\tsuccessfully, then, test actions are executed"
        "\n\t\twithout errors, e.g.:\n\t\t\thistoGe -t\n\n\t-P|--autoPeak: Look for peaks in a spectrum and ge"
        "nerates\n\t\ta .info file which includes the ranges of the peaks\n\t\tfound. It works better if the s"
        "pectrum is rebinned,\n\t\te.g.:\n\t\t\thistoGe --autoPeak File1.ext\n\n\t-R|--Rank|--rank: Performs a"
        " ranking for each peak contained\n\t\tin the .info file in order to find the most probable\n\t\tisoto"
        "pes that explain the peaks observed in the\n\t\tspectrum, e.g:\n\t\t\thistoGe -R File1.info\n\n\t-e|-"
        "-energyRanges: Look for all the isotopes that are in the\n\t\tranges specified for each peak in the ."
        "info file,\n\t\te.g.:\n\t\t\thistoGe -e File1.info\n\n\t-c|--stats: Calculate the Gilmore's statistic"
        "s for each peak\n\t\tin the .info file, e.g.:\n\t\t\thistoGe -c File1.info File1.ext * \n\n*This opti"
        "on needs and .info file and the spectrum.\n\nSUBOPTIONS OF MAIN OPTIONS\n\n\tOPTIONS\t\tSUBOPTIONS\n\n\t"
        "-h|--help\tNone\t\n\t\n\t-q|--query:\t--all:\tShows all the results found in a \n\t\t\t\tquery.\n\n\t"
        "-i|--isotope:\tNone\n\n\t-p|--parent:\tNone\n\n\t-r|--sub:\t--noCal: Indicates that the file is not\n\t\t\t\t"
        " calibrated.\n\t\t\t\n\t\t\t--log:\tLogarithmic scale in plot.\n\n\t\t\t--noPlot: No plot of the subs"
        "traction.\n\n\t\t\t--wof:\tWrite output file with result.\n\n\t\t\t--rebin: Channels are rebined.\n\n\t"
        "-s|--sum: \t--noCal: Indicates that the file is not\n\t\t\t\t calibrated.\n\n\t\t\t--log:\tLogarithmi"
        "c scale in plot. \n\n\t\t\t--noPlot: No plot of the substraction.\n\n\t\t\t--wof:\tWrite output file "
        "with result.\n\n\t-t|--test:\tNone\n\n\t-P|--autoPeak:\t--rebin: Channels are rebined.\n\n\t\t\t--wof"
        ":\tWrite output file with result.\n\n\t\t\t--noPlot: No plot of the substraction.\n\n\t\t\t--log:\tLo"
        "garithmic scale in plot.\n\n\t\t\t--noCal: Indicates that the file is not\n\t\t\t\t calibrated.\n\n\t"
        "-R|--Rank|--rank: --wof: Write output file with result.\n\n\t\t\t  --all: Shows all the results found"
        " in a \n\t\t\t\tquery.\n\n\t-e|--energyRanges: --all: Shows all the results found in a \n\t\t\t\tquer"
        "y. \n\n\t\t\t   --wof: Write output file with result.\n\n\t-c|--stats: \t--wof:\tWrite output file wi"
        "th result.\n\n\t\t\t--noPlot: No plot of the substraction.\n\n\t\t\t--noCal: Indicates that the file "
        "is not\n\t\t\t\t calibrated.\n\n\t\t\t--log:\tLogarithmic scale in plot.\n\nVALID FILES\n\nValid exte"
        "nsions are: .Txt, .SPA, .mca and .info\n\n\t.Txt files: Format file of gammavision software.\n\n\t.SP"
        "A files:  Format file developed and used in Boulby \n\t\t\tLaboratory.\n\t\n\t.mca files:  File forma"
        "t of micro-mca or px5 hardware.\n\n\t.info files: File used to store the ranges of peaks. Usually,\n\t\t\t"
        "is generated with --autoPeak main option.\n\t\t\t\t\n\nDOWNLOADABLE FILES\n\n\tA tutorial file can be"
        " consulted in:\n\n\t\thttps://bit.ly/2QL8FYj\n\n\tSome .mca files to try histoGe can be downloaded fr"
        "om:\n\n\t\thttps://bit.ly/2WNS36h\n\n\tDatabase can be downloaded from:\n\n\t\thttps://bit.ly/2YbVYKm"
        "\n\n*Database is encrypted. To obtain password sent a message to developers.\n\n")
        print(StrHelp)

    return 0