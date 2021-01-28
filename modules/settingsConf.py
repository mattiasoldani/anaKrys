from settings import *

###############################################################################
###############################################################################

def settingsSelect(boolTest, whichInput):
    
    if not boolTest:  # physics files -- either ROOT or ASCII
        print("looking for files with label %s in ./settings/" % whichInput)
        return "settings.%s_runList" % whichInput, "settings.%s_settings" % whichInput

    else:  # test files -- either ROOT or ASCII
        print("test mode: will operate with test settings & %s files" % whichInput)
        return "settings.test.y20Test_runList", "settings.test.y20Test_settings"


###############################################################################
###############################################################################

def boolControlPrint(boolLoad, boolTest, fileType):
    print("execution control booleans:")
    print("data reload controller: %s" % str(boolLoad))
    whichInput = (" (%s)" % fileType) if boolTest else ""
    print("test mode controller: %s%s" % (str(boolTest), whichInput))
    
###############################################################################
###############################################################################

def settingsPrint(filePath, fileNameFormat, nRunToOpen, nRun0):
    
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
    if len(iRun)>0:
        for i in range(len(iRun)):
            print("(%d/%d) %s %s" % (i+1, len(iRun), iRun[i], iType[i]))
    else:
        print("no runs selected for opening -- execution will only work if test mode is selected")