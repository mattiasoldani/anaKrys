import pickle

###############################################################################
###############################################################################

def saveOutData(globDict, pathToMain=""):
    # globDict must be globals() in the main program, which must contain the outData dictionary
    
    outData = globDict["outData"]
    outPath = "./" + pathToMain + "out_data/"
    outFileName = outPath + "outData.pickle"
    print("saving output dictionary outData to %s, with %d entries" % (outFileName, len(outData)))
    outFile = open(outFileName, "wb")
    pickle.dump(outData, outFile)
    outFile.close()