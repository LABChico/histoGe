from os.path import basename

def helpFun(argv, functionDict, extBool=False):
    if not extBool:
        print("\n----------------------------------------------------------------------\nhistoGe's SYNTAX\n----------------------------------------------------------------------\n")
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
        StrHelp = ('----------------------------------------------------------------------\n'
        'EXTENDED HELP OF histoGe\n---------------------------------------------------------'
        '-------------\n\nMAIN OPTIONS\n\nIf no main option are provided then histoGe perfor'
        'ms a query to \ndatabase if extension of the file is .info, in other case, performs'
        '\na multiplot with the files provided,e.g.:\n\nhistoGe file1.extension [file2.exten'
        'sion ...]\n\nThe histoGe\'s main option are:\n\n\t-q|--query: Query the database to'
        ' find isotopes that\n\t\tradiate gammas in the range from initial energy\n\t\t(iEner'
        ') to final energy (fEner) both in KeV, e.g.:\n\t\t\thistoGe -q 100 101\n\n\t-i|--iso'
        'tope: Query the database to find gammas of each\n\t\tisotopes, e.g.:\n\t\t\thistoGe '
        '-i 60Co 241Am\n\n\t-p|--parent: Query the database looking for the parent \n\t\tisot'
        'ope and the child or children isotopes, e.g.:\n\t\t\thistoGe -p 60Co 241Am\n\n\t-r|-'
        '-sub: Substraction of two sprectra, i.e., File2 is \n\t\tsubstracted to File1.ext, e'
        '.g.:\n\t\t\thistoGe -r File1.ext File2.ext\n\n\t--rebin: Channels of the spectrum ar'
        'e rebined, it is just \n\t\tneed necessary to specify how many channels do you \n\t\t'
        'want to rebin. In any case if the rebin number is \n\t\tnot specified the default reb'
        'in number is 5. e.g.:\n\t\t\thistoGe File.ext --rebin 6\n\n\t-s|--sum: Sumation of sp'
        'ectra. The option can sum all the\n\t\tspectra that the user need, e.g.:\n\t\t\thist'
        'oGe -s File1.ext File2.ext\n\n\t-t|--test: Performs a test. If histoGe was installed'
        ' \n\t\tsuccessfully, then, test actions are executed\n\t\twithout errors, e.g.:\n\t'
        '\t\thistoGe -t\n\n\t-P|--autoPeak: Look for peaks in a spectrum and generates\n\t\ta '
        '.info file which includes the ranges of the peaks\n\t\tfound. It works better if the '
        'spectrum is rebinned,\n\t\te.g.:\n\t\t\thistoGe --autoPeak File1.ext\n\n\t-e|--energy'
        'Ranges: Look for all the isotopes that are in the\n\t\tranges specified for each peak'
        ' in the .info file,\n\t\te.g.:\n\t\t\thistoGe -e File1.info\n\n\t-c|--stats: Calculat'
        'e the Gilmore\'s statistics for each peak\n\t\tin the .info file, e.g.:\n\t\t\thistoG'
        'e -c File1.info File1.ext *\n\n    -f|--hge: Converts the SPE, Txt or mca files to hg'
        'e format.\n            histoGe -f File1.ext\n\n    -n,--normInt: Displays relative em'
        'ission probability from\n        database.\n            histoGe -n 60Co 241Am\n    \n'
        '    -R|--Rank|--rank: Performs a ranking for each peak contained\n\t\tin the .info fi'
        'le in order to find the most probable\n\t\tisotopes that explain the peaks observed i'
        'n the\n\t\tspectrum, e.g:\n\t\t\thistoGe -R File1.info\n\n    --halfSort|--halfRank|-'
        '-halfrank: Performs ranking using the\n        half-life of the isotopes.\n          '
        '  histoGe --halfSort File1.info\n\n    --RA|--RankAdv|--rankAdv: Performs ranking usi'
        'ng total net area\n        and the relative emission probability.\n            histoG'
        'e  File1.info File1.ext * \n\n    --fuzzy|--fuzzyRank|--fuzzyrank|-z: Performs rankin'
        'g using fuzzy\n        logic. It needs to run an .info and valid spectrum, e.g.:\n   '
        '         histoGe -z File1.info File1.ext *\n    \n    --chainRank|--ChainRank|-x\': P'
        'erforms ranking using decay\n        chains.\n            histoGe -x File1.info\n\n\t'
        '--distance|-d: Performs ranking calculating the deviation between\n        the mean v'
        'alue of peaks and the energy of the γ-lines.\n    \t\thistoGe -b File1.info File1.ext'
        ' *\n\n\t--probability|-b: Performs ranking using γ-line calculating \n\t\tthe cumulat'
        'ive distribution function for the Gaussian \n\t\tdistribution. It needs an .info file'
        ' and valid spectrum, e.g.:\n\t\t\thistoGe -b File1.info File1.ext *\n\n*This option n'
        'eeds and .info file and the spectrum.\n\nSUBOPTIONS OF MAIN OPTIONS\n\n\tOPTIONS\t\tS'
        'UBOPTIONS\n\n\t-h|--help\tNone\t\n\t\n\t-q|--query:\t--all:\tShows all the results fo'
        'und in a \n\t\t\t\tquery.\n\n\t-i|--isotope:\tNone\n\n\t-p|--parent:\tNone\n\n\t-r|--'
        'sub:\t--noCal: Indicates that the file is not\n\t\t\t\t calibrated.\n\t\t\t\n\t\t\t--'
        'log:\tLogarithmic scale in plot.\n\n\t\t\t--noPlot: No plot of the substraction.\n\n\t'
        '\t\t--wof:\tWrite output file with result.\n\n\t\t\t--rebin: Channels are rebined.\n\n'
        '\t-s|--sum: \t--noCal: Indicates that the file is not\n\t\t\t\t calibrated.\n\n\t\t\t'
        '--log:\tLogarithmic scale in plot. \n\n\t\t\t--noPlot: No plot of the substraction.\n'
        '\n\t\t\t--wof:\tWrite output file with result.\n\n\t-t|--test:\tNone\n\n\t-P|--autoPe'
        'ak:\t--rebin: Channels are rebined.\n\n\t\t\t--wof:\tWrite output file with result.\n'
        '\n\t\t\t--noPlot: No plot of the substraction.\n\n\t\t\t--log:\tLogarithmic scale in '
        'plot.\n\n\t\t\t--noCal: Indicates that the file is not\n\t\t\t\t calibrated.\n\n\t-e|'
        '--energyRanges: --all: Shows all the results found in a \n\t\t\t\tquery. \n\n\t\t\t  '
        ' --wof: Write output file with result.\n\n\t-c|--stats: \t--wof:\tWrite output file w'
        'ith result.\n\n\t\t\t--noPlot: No plot of the substraction.\n\n\t\t\t--noCal: Indicat'
        'es that the file is not\n\t\t\t\t calibrated.\n\n\t\t\t--log:\tLogarithmic scale in p'
        'lot.\n\n\t\t\t--rebin: Channels are rebined.\t\t\t\n\n    -f|--hge: None\n\n    -n,--'
        'normInt: None\n    \n    -R|--Rank|--rank: --wof: Write output file with result.\n\n'
        '\t\t\tC|D|E: \tThese options allow the user to choose\n\t\t\t\t\ta rank to sort the ou'
        'tput isotope list giving\n                    priority. The output table will display'
        ' three\n                    columns of different rankings and they will be\n         '
        '           ordered according to the rank that has been \n                    chosen b'
        'etween options C, D or E. In case no \n                    option has been selected, '
        'the default ordering\n                    used in the case that it does not be indica'
        'ted\n                    is rank E.\t\t\n\n\t\t\t--all: Shows all the results found i'
        'n a \n\t\t\t\tquery.\n    \n    --halfSort|--halfRank|--halfrank: --all: Displays all'
        '\n                isotopes in the list.\n            \n            --wof: Write outpu'
        't file with result.\n    \n    --RA|--RankAdv|--rankAdv: --wof: Write output \n      '
        '          file with result.\n\n            --all: displays all isotopes in the list.'
        '\n\n            --filter: removes those isotopes with relative\n                emiss'
        'ion probability smaller than 0.05. \n\n    --fuzzy|--fuzzyRank|--fuzzyrank|-z: --wof:'
        ' Write output \n                file with result.\n\n            --all: displays all '
        'isotopes in the list.\n\n            --filter: removes those isotopes with relative\n'
        '                emission probability smaller than 0.05.\n\n\n    --chainRank|--ChainR'
        'ank|-x: --wof: Write output \n                file with result.\n    \n            --'
        'all: displays all isotopes in the list.\n    \n            --peak: uses relative emis'
        'sion probability to\n                make ranking.\n\n\t--distance|-d:  --all: Shows '
        'all the results found in a \n\t\t\t\tquery. \n\n\t\t\t   --wof: Write output file wit'
        'h result.\n\n\t--probability|-b:  --all: Shows all the results found in a \n\t\t\t\tq'
        'uery. \n\n\t\t\t   --wof: Write output file with result.\n\nRANKING RESULT DISPLAY\n'
        '\nWhen a ranking method is chosen, a dataframe is displayed and \nits ordering shows '
        'its best results. Notice that the columns \nare labeled with letters from A to J, thi'
        's labels refer to \na rank method described in the manuscript titled "Contextual \nis'
        'otope ranking criteria for peak identification in gamma \nspectroscopy using a large '
        'database", and the rank method \ncorresponding to each label will be show as follows.'
        ' \n\n\tLabel: Ranking method\t\n\t\n\tA:\tGamma-line distance from mean\n\tB:\tGamma-'
        'line coincidence probability\n\tC:\tHalf-life sorting\n\tD:\tPeak Explanation Power\n'
        '\tE:\tImproved Peak Explanation Power\n\tF:\tRelative Emission Probability\n\tG:\tRel'
        'ative Emission Probability with Gilmore\'s Statistics\n\tH:\tRanking With a Fuzzy Inf'
        'erence System\n\tI:\tChain using Peak Explanation criterion\n\tJ:\tChain using Relati'
        've Emission Probability\n\nThe manuscript is in preparation now, once it is published'
        ', \nplease look for it using the title.\n\nVALID FILES\n\nValid extensions are: .Txt,'
        ' .SPA, .mca and .info\n\n\t.Txt files: Format file of gammavision software.\n\n\t.SPA'
        ' files:  Format file developed and used in Boulby \n\t\t\tLaboratory.\n\t\n\t.mca fil'
        'es:  File format of micro-mca or px5 hardware.\n\n\t.info files: File used to store t'
        'he ranges of peaks. Usually,\n\t\t\tis generated with --autoPeak main option.\n\t\t\t'
        '\t\n\nDOWNLOADABLE FILES\n\n\tA tutorial file can be consulted in:\n\n\t\thttps://bit'
        '.ly/2QL8FYj\n\n\tSome .mca files to try histoGe can be downloaded from:\n\n\t\thttps:'
        '//bit.ly/2WNS36h\n\n\tDatabase can be downloaded from:\n\n\t\thttps://bit.ly/38ip7c1 '
        '\n\nEXECUTION OF MULTIPLE COMMANDS\n\nhistoGe can execute several commands in a singl'
        'e run. \nCommands must be separated by "!" character, for example:\n\n        histoGe'
        ' Command_1 ! Command_2 ! ... ! Command_N\n\n\n\n')
        print(StrHelp)

    return 0
