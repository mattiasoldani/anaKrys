import time
from settings import *

###############################################################################
###############################################################################

def settingsSelect(boolTest, whichInput):
    t = time.strftime("%Y-%m-%d %H:%M:%S GMT", time.gmtime(time.time()))
    if not boolTest:
        print("looking for files with label %s in ./settings/" % whichInput)
        settingsFile = open("./settings/__init__.py", "w")
        print("# rewritten automatically by anaKrys.ipynb", file=settingsFile)
        print("# last recreation: %s" % t, file=settingsFile)
        print("from .%s_runList import *" % whichInput, file=settingsFile)
        print("from .%s_inputFileFormat import *" % whichInput, file=settingsFile)
        print("from .%s_settings import *" % whichInput, file=settingsFile)
        settingsFile.close()
    else:
        if whichInput:
            print("test mode: will operate with test settings & ROOT files")
            settingsFileInner = open("./settings/test/__init__.py", "w")
            print("# rewritten automatically by anaKrys.ipynb -- test mode with ROOT files", file=settingsFileInner)
            print("# last recreation: %s" % t, file=settingsFileInner)
            print("from .y20Test_runList import *", file=settingsFileInner)
            print("from .y20TestRoot_inputFileFormat import *", file=settingsFileInner)
            print("from .y20Test_settings import *", file=settingsFileInner)
            settingsFileInner.close()
        else:
            print("test mode: will operate with test settings & ASCII files")
            settingsFileInner = open("./settings/test/__init__.py", "w")
            print("# rewritten automatically by anaKrys.ipynb -- test mode with ASCII files", file=settingsFileInner)
            print("# last recreation: %s" % t, file=settingsFileInner)
            print("from .y20Test_runList import *", file=settingsFileInner)
            print("from .y20TestAscii_inputFileFormat import *", file=settingsFileInner)
            print("from .y20Test_settings import *", file=settingsFileInner)
            settingsFileInner.close()
        settingsFileOuter = open("./settings/__init__.py", "w")
        print("# rewritten automatically by anaKrys.ipynb -- test mode", file=settingsFileOuter)
        print("# last recreation: %s" % t, file=settingsFileOuter)
        print("from .test import *", file=settingsFileOuter)
        settingsFileOuter.close()

###############################################################################
###############################################################################

def boolControlPrint(boolLoad, boolPlot, boolTest):
    print("execution control booleans:")
    print("data reload controller: %s" % str(boolLoad))
    print("base plots controller: %s" % str(boolPlot))
    whichInput = (" (ROOT)" if boolTest[1] else " (ASCII)") if boolTest[0] else ""
    print("test mode controller: %s%s" % (str(boolTest[0]), whichInput))
    
###############################################################################
###############################################################################

def settingsPrint():
    
    #####
    # I/O-related
    print("will work with run numbers(s)/type(s) in %s with format %s" % (filePath, fileNameFormat))
    iRun = []
    iType = []
    for i, iKey in enumerate(nRunToOpen):
        if iKey in nRun0:
            iRun.append(iKey)
            iType.append(nRun0[iKey])
        elif iKey in nRun0.values():
            lsRuns = [s for s in nRun0 if iKey==nRun0[s]]
            for j in range(len(lsRuns)):
                iRun.append(lsRuns[j])
                iType.append(iKey)
    for i in range(len(iRun)):
        print("(%d/%d) %s %s" % (i+1, len(iRun), iRun[i], iType[i]))