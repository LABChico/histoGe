
from myLibs.parsers import isValidSpectrumFile,getDictFromSPEAdv,getDictFromMCAAdv,getDictFromGammaVisionAdv,functionDictAdv
from myLibs.miscellaneus import WritehgeFile
import sys

def DataFile2hgeFile(ListOpt):
    
    List = ListOpt.copy()
    List.pop(0)
    ValidFileList = []
    for File in List:
        if isValidSpectrumFile(File):
            ValidFileList.append(File)

    if len(ValidFileList) != 0:
        for File in ValidFileList:
            myExtension = File.split('.')[-1]
            mySpecialDict = functionDictAdv[myExtension](File)
            hgeFilename = File.split('.')[0] + '_factor.hge' 
            exitcode = WritehgeFile(hgeFilename,mySpecialDict)
    else:
        sys.stderr.write('There is not a valid file to be converted to .hge file.\n')
        return 1050
    return exitcode






