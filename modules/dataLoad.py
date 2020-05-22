import succolib as sl

###############################################################################
###############################################################################

def loadGeneral(fileType, fileNameFormatFull, nRun, descFrac, mirrorMap):
    print("opening %s files... --> data into DataFrame df" % fileType)
    
    # loading -- if raw data files are ASCII...
    if fileType == "ASCII":  
        from settings import asciiMap, nLinesEv
        df, dt = sl.asciiToDfMulti(fileNameFormatFull, list(nRun.keys()), asciiMap, "iRun", nLinesEv, descFrac, mirrorMap, bVerbose=True)

    # loading -- if raw data files are ROOT trees...
    elif fileType == "ROOT":
        from settings import treeMap, treeName
        df, dt = sl.rootToDfMulti(fileNameFormatFull, list(nRun.keys()), treeName, "iRun", descFrac, treeMap, mirrorMap, bVerbose=True)
    
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
    