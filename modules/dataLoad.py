import succolib as sl
import pickle

###############################################################################
###############################################################################

def loadGeneral(fileType, fileNameFormatFull, nRun, descFrac, mirrorMap, globDict, bProgress):
    # globDict must be globals() in the main program --> used to get filetype-specific info from imported settings
    
    print("opening %s files... --> data into DataFrame df" % fileType)
    if not bProgress:
        print("progressbars won't be visualized...")
    
    # loading -- if raw data files are ASCII...
    if fileType == "ASCII":  
        asciiMap, nLinesEv = globDict["asciiMap"], globDict["nLinesEv"]
        df, dt = sl.asciiToDfMulti(fileNameFormatFull, list(nRun.keys()), asciiMap, "iRun", nLinesEv, descFrac, mirrorMap, bVerbose=True, bProgress=bProgress)

    # loading -- if raw data files are ROOT trees...
    elif fileType == "ROOT":
        treeMap, treeName = globDict["treeMap"], globDict["treeName"]
        df, dt = sl.rootToDfMulti(fileNameFormatFull, list(nRun.keys()), treeName, "iRun", descFrac, treeMap, mirrorMap, bVerbose=True, bProgress=bProgress)
    
    # neither ASCII nor ROOT --> not loading anything --> error!
    else:
        print("%s is not a valid filetype --> execution won't work..." % fileType)
        
    print("--")
        
    # also create typeRun column using the descriptions set within nRun0 (--> nRun)
    for iRun in df["iRun"].unique():
        df.loc[df["iRun"] == iRun, "typeRun"] = nRun[iRun]
    print("typeRun added to df")

    return df, dt

###############################################################################
###############################################################################

def loadSkipPrint(df):
    print("skipping data loading (boolLoad = False)...")
    if df.shape[0] == 0:
        print("no events found --> execution won't work...")
    else:
        print("df already exists with")
        print("--> (events, variables) = " + str(df.shape))
        print("--> runs = " + str(df.iRun.unique()))
        print("--> run types = " + str(df.typeRun.unique()))
        
###############################################################################
###############################################################################
        
def loadDonePrint(df, dt):
    if df.shape[0] == 0:
        print("no events found --> execution won't work...")
    else:
        print("done (in %.2f s) --> raw data have (events, variables) = %s" % (dt, str(df.shape)))
        
###############################################################################
###############################################################################

def readOutData(pathToMain=""):
    with open("./" + pathToMain + "/out_data/outData.pickle",'rb') as inFile:
        outData = pickle.load(inFile)
    return outData
    
    
