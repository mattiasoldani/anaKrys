import pickle

###############################################################################
###############################################################################

def saveOutData(globDict):
    # globDict must be globals() in the main program, which must contain the outData dictionary
    
    outData = globDict["outData"]
    outPath = "./out_data/"
    outFileName = outPath + "outData.pickle"
    print("saving output dictionary outData to %s, with %d entries" % (outFileName, len(outData)))
    outFile = open(outFileName, "wb")
    pickle.dump(outData, outFile)
    outFile.close()