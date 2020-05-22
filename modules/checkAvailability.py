def dfCheckAvailability(df, baseTrackingMap):

    #####
    # step number -- iStep
    bIStep = False if not ("iStep" in df.columns) else True
    print("scan step number (iStep) availability: %s \n--" % str(bIStep))
    
    #####
    # Unix time -- epoch
    bEpoch = False if not ("epoch" in df.columns) else True
    print("Unix time (epoch) availability: %s \n--" % str(bEpoch))

    #####
    # goniometer DOF -- xGonioRaw...
    lsGonio = [s.replace("xGonioRaw", "") for s in df.columns if "xGonioRaw" in s]  # list of the full raw goniometer DOF names -- without prefix
    bXGonio = False if len(lsGonio) == 0 else True
    printNr = ("(%d)" % len(lsGonio)) if bXGonio else ""
    print("goniometer DOF availability: %s %s" % (str(bXGonio), printNr))
    print("xGonioRaw + %s" % str(lsGonio))
    print("--")

    #####
    # input (all 4) & output (both 2) tracking data...
    print("input modules should be: %s" % str(baseTrackingMap[0]))
    print("output modules should be: %s" % str(baseTrackingMap[1]))

    #####
    # positions -- xRaw...
    bXRaw = {"in": True, "out": True}  
    for iLayer in baseTrackingMap[0]:
        if not ("xRaw"+iLayer in df.columns):
            bXRaw["in"] = False  # input 
    for iLayer in baseTrackingMap[1]:
        if not ("xRaw"+iLayer in df.columns):
            bXRaw["out"] = False  # output
    print("input tracking availability (xRaw...): %s" % str(bXRaw["in"]))
    print("output tracking availability (xRaw...): %s" % str(bXRaw["out"]))

    #####
    # multiplicities -- nHit...
    bNHit = {"in": True, "out": True}
    for iLayer in baseTrackingMap[0]:
        if not ("nHit"+iLayer in df.columns):
            bNHit["in"] = False  # input 
    for iLayer in baseTrackingMap[1]:
        if not ("nHit"+iLayer in df.columns):
            bNHit["out"] = False  # output
    print("input multiplicity availability (nHit...): %s" % str(bXRaw["in"]))
    print("output multiplicity availability (nHit...): %s" % str(bXRaw["out"]))
    print("--")

    #####
    # digitizer data -- digiPHRaw... & digiTime...
    lsDigiRawCh = [s for s in sorted(df.columns) if "digiPHRaw" in s]  # list of the full raw digitizer PH names
    lsDigiCh = [s.replace("digiPHRaw", "") for s in lsDigiRawCh]  # list of the digitizer channel names -- without any prefix

    bDigiPHAny = False if len(lsDigiCh) == 0 else True  # global PH availability -- single channels listed in lsDigiRawCh
    print("digitizer channel availability: %s" % str(bDigiPHAny))
    if bDigiPHAny:
        print("%d channels: digiPHRaw + %s" % (len(lsDigiCh), str(lsDigiCh)))
        bDigiTime = {}
        for i, iCh in enumerate(lsDigiRawCh):
            # digitizer time availability for each of the available PH (listed in lsDigiRawCh)
            bDigiTime.update({iCh.replace("digiPHRaw", ""): True if iCh.replace("PHRaw", "Time") in df.columns else False})
        print("%d with time: digiTime + %s" % (len([s for s in bDigiTime if bDigiTime[s]]), str([s for s in bDigiTime if bDigiTime[s]])))
        
    print("--")
           
    #####
    # forward calorimeter total PH & energy in GeV -- PHCaloFwd & EFwd
    bPHCaloFwd = False if not ("PHCaloFwd" in df.columns) else True
    print("forward calorimeter total signal (PHCaloFwd) availability a priori: %s" % str(bPHCaloFwd))
    
    bEFwd = False if not ("EFwd" in df.columns) else True
    print("forward calorimeter total in GeV (EFwd) availability a priori: %s" % str(bEFwd))
            
    return df, bIStep, bEpoch, bXGonio, bXRaw, bNHit, bDigiPHAny, lsDigiCh, bDigiTime, bPHCaloFwd, bEFwd

###############################################################################
###############################################################################

def zBaseCheckAvailability(z, lsRun, baseTrackingMap):
    for iRun in lsRun:
        if iRun in z:
            bGlobalAvailability = True
        else:
            bGlobalAvailability = False
            z.update({iRun: {}})

        # goniometer
        if not ("gonio" in z[iRun]):
            bGlobalAvailability = False
            print("z[%s][\"gonio\"] unavailable --> setting 0" % iRun)
            z[iRun].update({"gonio": 0})
            
        # forward calorimeter
        if not ("caloFwd" in z[iRun]):
            bGlobalAvailability = False
            print("z[%s][\"caloFwd\"] unavailable --> setting 0" % iRun)
            z[iRun].update({"caloFwd": 0})

        # input/output base tracking layers
        for iLayer in baseTrackingMap[0]+baseTrackingMap[1]:  
            if not (iLayer in z[iRun]):
                bGlobalAvailability = False
                print("z[%s][\"%s\"] unavailable --> setting 0" % (iRun, iLayer))
                z[iRun].update({iLayer: 0})

        if bGlobalAvailability:
            print("all mandatory z[%s] available" % iRun)
            
    return z