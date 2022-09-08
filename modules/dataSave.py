import pickle

###############################################################################
###############################################################################

def saveOutData(globDict, pathToMain=""):
    # globDict must be globals() in the main program, which must contain the outData dictionary
    
    outData = globDict["outData"]
    outPath = "./" + pathToMain + "out_data/"
    outFileName = outPath + "outData.pickle"
    print("saving output dictionary outData to %s, with %d entries" % (outFileName, len(outData)))
    with open(outFileName, "wb") as outFile:
        pickle.dump(outData, outFile)
