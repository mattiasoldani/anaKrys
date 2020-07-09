import pandas as pd
import numpy as np
import succolib as sl
import inspect

###############################################################################
###############################################################################

def peakedDistMode(series):
    if len(series.unique()) <= 1:
        centre = 0
    else:
        cat0 = pd.cut(series, bins=np.arange(-0.5, 0.5, 0.0001)).value_counts()
        centre0 = cat0.index[0].mid
        range0 = 5*series.std()
        binning0 = 0.00005*series.std()
        cat = pd.cut(series, bins=np.arange(centre0-range0, centre0+range0, binning0)).value_counts()
        centre = cat.index[0].mid
    return centre

###############################################################################
###############################################################################

def aveVar(df, listInVar, nameAveVar):
    ls = [df[s] for s in listInVar]
    lsAve = sum(ls) / len(ls)
    df[nameAveVar] = lsAve
    print("%s added to df -- (mean, std) = (%f, %f)" % (nameAveVar, df[nameAveVar].mean(), df[nameAveVar].std()))
    return df

###############################################################################
###############################################################################

def inHitCuts(df, layerMap):
    df["boolSingleHitIn"] = (df[layerMap[0]] == 1) & (df[layerMap[1]] == 1) & (df[layerMap[2]] == 1) & (df[layerMap[3]] == 1)
    # note: single-hit selection is not based on nHitIn but rather on input layers individually
    print("boolSingleHitIn added to df")
    return df

###############################################################################
###############################################################################

def outHitCuts(df, layerMap, outMultCut):
    
    df["boolSingleHitOut"] = (df[layerMap[0]] == 1) & (df[layerMap[1]] == 1)
    # note: single-hit selection is not based on nHitOut but rather on output layers individually
    print("boolSingleHitOut added to df")
    print("--")
    
    for iRun in df["iRun"].unique():
        print("run %s:" % iRun)
        if iRun in outMultCut:
            df.loc[df["iRun"]==iRun, "boolLowHitOut"] = df["nHitOut"] <= outMultCut[iRun][0]
            df.loc[df["iRun"]==iRun, "boolHighHitOut"] = df["nHitOut"] >= outMultCut[iRun][1]
            print("boolLowHitOut: output multiplicity lower window @ <= %f" % (outMultCut[iRun][0]))
            print("boolHighHitOut: output multiplicity upper window @ >= %f" % (outMultCut[iRun][1]))
        else:
            df.loc[df["iRun"]==iRun, "boolLowHitOut"] = True
            df.loc[df["iRun"]==iRun, "boolHighHitOut"] = True
            print("no cuts defined on output multiplicity --> booleans always True")

    return df

###############################################################################
###############################################################################

def trackingAngleAlign(df, trackingMap, thCentres, thName, z, bThCut, thCut = {}):
    for iRun in df["iRun"].unique():
        dfBool = df["iRun"] == iRun
        print("run %s:" % iRun)
        for i in range(2):
            axis = ["x", "y"]
            zU = z[iRun][trackingMap[i].replace("xRaw", "").replace("xCry"+str(i), "gonio")]  # replace arguments to deal with both input/output cases
            zD = z[iRun][trackingMap[i+2].replace("xRaw", "")]
            xRawU = df[dfBool][trackingMap[i]]
            xRawD = df[dfBool][trackingMap[i+2]]
            
            # raw angles
            df.loc[dfBool, thName+"Raw"+str(i)] = sl.zAngle(xRawD, zD, xRawU, zU)
            print("%sRaw%d added to df" % (thName, i))
            
            # shift value?
            if thCentres[iRun][i] is None:  # if no shift value is given (None), single-run angle distribution mode is used (function in .modules)
                centre = peakedDistMode(df[dfBool][thName+"Raw"+str(i)])
                print("trying to align %s layers (%s & %s) with %sRaw%d mode: %.10f" % (axis[i], trackingMap[i], trackingMap[i+2], thName, i, centre))
            else:
                centre = thCentres[iRun][i]
                print("aligning %s layers (%s & %s) with the value given in the settings: %.10f" % (axis[i], trackingMap[i], trackingMap[i+2], centre))
                
            # shift downstream modules
            df.loc[dfBool, xRawU.name.replace("Raw", "")] = xRawU  # actually upstream module is not shifted -- copied with new name (trivially in itself) in input (output) analysis
            df.loc[dfBool, xRawD.name.replace("Raw", "")] = xRawD - centre*(zD - zU)
            
            # shift raw angles
            df.loc[dfBool, thName+str(i)] = df[thName+"Raw"+str(i)] - centre
            
        # input angle selection (if required)
        # name of the variable is "bool" + thName.replace("th", "") + "Aligned"
        if bThCut:
            if iRun in thCut:
                if len(thCut[iRun]) == 4:  # rectangular cut
                    xCutL = thCut[iRun][0]
                    xCutR = thCut[iRun][1]
                    yCutL = thCut[iRun][2]
                    yCutR = thCut[iRun][3]
                    cutX = (df[thName+"0"] > xCutL) & (df[thName+"0"] < xCutR)
                    cutY = (df[thName+"1"] > yCutL) & (df[thName+"1"] < yCutR)
                    df.loc[dfBool, "bool%sAligned" % thName.replace("th", "")] = cutX & cutY
                    print("bool%sAligned: rectangle centered in 0 with hor. (ver.) side %f (%f) (edges excluded)" % (thName.replace("th", ""), abs(xCutR-xCutL), abs(yCutR-yCutL)))
                elif len(thCut[iRun]) == 2:  # elliptical cut (different x & y axes)
                    xCut = thCut[iRun][0]
                    yCut = thCut[iRun][1]
                    df.loc[dfBool, "bool%sAligned" % thName.replace("th", "")] = (df[thName+"0"] / xCut)**2 + (df[thName+"1"] / yCut)**2 < 1
                    print("bool%sAligned: ellipse centered in 0 with hor. (ver.) half-axis %f (%f) (edge excluded)" % (thName.replace("th", ""), xCut, yCut))
                elif len(thCut[iRun]) == 1:  # circular cut -- radius as only parameter
                    df.loc[dfBool, "bool%sAligned" % thName.replace("th", "")] = (df[thName+"0"] / thCut[iRun])**2 + (df[thName+"1"] / thCut[iRun])**2 < 1
                    print("bool%sAligned: circle centered in 0 with radius %f (edge excluded)" % (thName.replace("th", ""), thCut[iRun]))
                else:
                    df.loc[dfBool, "bool%sAligned" % thName.replace("th", "")] = True
                    print("no cut defined for %s angle (cut list size mismatch) --> bool%sAligned always True" % (thName, thName.replace("th", "")))
            else:
                df.loc[dfBool, "bool%sAligned" % thName.replace("th", "")] = True
                print("no cut defined for %s angle (run not in th%sCut) --> bool%sAligned always True" % (thName, thName.replace("th", ""), thName.replace("th", "")))
            
    return df

###############################################################################
###############################################################################

def inputTrackingProj(df, inTrackingMap, z, xCryCut):
    for iRun in df["iRun"].unique():
        dfBool = df["iRun"] == iRun
        for i in range(2):
            zU = z[iRun][inTrackingMap[i]]
            zD = z[iRun][inTrackingMap[i+2]]
            xU = df[dfBool]["x" + inTrackingMap[i]]
            xD = df[dfBool]["x" + inTrackingMap[i+2]]
            
            # input beam @ crystal
            df.loc[dfBool, "xCry%d"%i] = sl.zProj(xD, zD, xU, zU, z[iRun]["gonio"])
            
            # input beam @ forward calorimeter
            df.loc[dfBool, "xCaloFwd%d"%i] = sl.zProj(xD, zD, xU, zU, z[iRun]["caloFwd"])
            
        # crystal fiducial selection
        if iRun in xCryCut:
            xCut = [xCryCut[iRun][0], xCryCut[iRun][1]]
            yCut = [xCryCut[iRun][2], xCryCut[iRun][3]]
            df.loc[dfBool, "boolInCry0"] = (df["xCry0"]>xCut[0]) & (df["xCry0"]<xCut[1])
            df.loc[dfBool, "boolInCry1"] = (df["xCry1"]>yCut[0]) & (df["xCry1"]<yCut[1])
            df.loc[dfBool, "boolInCry"] = df["boolInCry0"] & df["boolInCry1"]
            print("run %s: boolInCry(0/1): (%f < x < %f) &  (%f < y < %f)" % (iRun, xCut[0], xCut[1], yCut[0], yCut[1]))
        else:
            df.loc[dfBool, "boolInCry0"] = True
            df.loc[dfBool, "boolInCry1"] = True
            df.loc[dfBool, "boolInCry"] = True
            print("run %s: no cut defined on crystal fiducial area --> boolInCry(0/1) always True" % iRun)
            
    print("--")
            
    # print input beam info -- once for the whole dataset
    for i in range(2):
        axis = ["x", "y"]
        print("%s axis" % axis[i])
        print("final input angle %s: (mean, std) = (%f, %f)" % (df["thIn%d"%i].name, df["thIn%d"%i].mean(), df["thIn%d"%i].std()))
        print("final beam projections: x%s, x%s, xCry%d, xCaloFwd%d" % (inTrackingMap[i], inTrackingMap[i+2], i, i))
            
    return df

###############################################################################
###############################################################################

def outputTrackingPrint(df, outTrackingMap):
    for i in range(2):
        axis = ["x", "y"]
        print("%s axis" % axis[i])
        print("final output angle %s: (mean, std) = (%f, %f)" % (df["thOut%d"%i].name, df["thOut%d"%i].mean(), df["thOut%d"%i].std()))
        print("final beam projections: xCry%d, x%s" % (i, outTrackingMap[i]))

###############################################################################
###############################################################################
        
def gonioPair(df, gonioMap):
    for iDof in [s.replace("xGonioRaw", "") for s in df.columns if "xGonioRaw" in s]:
        if iDof in gonioMap:  # if selected DOF is listed in gonioMap...
            if gonioMap[iDof][0] in df.columns:  # if variable coupled to selected DOF exists in df...
                if gonioMap[iDof][1]:  # if variable shifting (via mean) is selected...
                    df["xGonio%s" % iDof] = df["xGonioRaw%s" % iDof] + (df[gonioMap[iDof][0]] - df[gonioMap[iDof][0]].mean()) * gonioMap[iDof][2]
                    print("xGonioRaw%s paired to %s (shifted via its mean) with factor %E --> xGonio%s" % (iDof, gonioMap[iDof][0], gonioMap[iDof][2], iDof))
                else:  # if variable shifting (via mean) is not selected...
                    df["xGonio%s" % iDof] = df["xGonioRaw%s" % iDof] + df[gonioMap[iDof][0]] * gonioMap[iDof][2]
                    print("xGonioRaw%s paired to %s (as it is in df) with factor %E --> xGonio%s" % (iDof, gonioMap[iDof][0], gonioMap[iDof][2], iDof))
                    
            # recall: a xGonio variable is always created for each xGonioRaw variable -- if no shifting can be performed, simply xGonioX=xGonioRawX
            else:
                df["xGonio%s" % iDof] = df["xGonioRaw%s" % iDof]
                print("xGonioRaw%s copied into xGonio%s with no modifications (%s not in df)" % (iDof, iDof, gonioMap[iDof][0]))
        else:
            df["xGonio%s" % iDof] = df["xGonioRaw%s" % iDof]
            print("xGonioRaw%s copied into xGonio%s with no modifications (not in gonioMap)" % (iDof, iDof))
            
    return df

###############################################################################
###############################################################################

def equalise(df, lsDigiCh, equalMap):
    for iRun in df["iRun"].unique():
        dfBool = df["iRun"] == iRun
        print("run %s:" % iRun)
        if iRun in equalMap:
            for iCh in lsDigiCh:
                if iCh in equalMap[iRun]:
                    func = equalMap[iRun][iCh][0]
                    args = [df["digiPHRaw" + iCh]] + equalMap[iRun][iCh][1]
                    funcSrc = inspect.getsource(func)
                    funcStr = (funcSrc.partition("lambda ")[1]+funcSrc.partition("lambda ")[2]).partition(", 'end'")[0]
                    print("digiPHRaw%s --> digiPH%s via %s" % (iCh, iCh, funcStr))
                    df.loc[dfBool + iCh] = func(*args)

                else:
                    print("digiPH%s = digiPHRaw%s, i.e. not equalised (not in equalMap)" % (iCh, iCh))
                    df.loc[dfBool, "digiPH" + iCh] = df["digiPHRaw" + iCh]
        else:
            print("digiPH* = digiPHRaw* (all var. in lsDigiCh), i.e. not equalised (run not in equalMap)")
            for iCh in lsDigiCh:
                df.loc[dfBool, "digiPH" + iCh] = df["digiPHRaw" + iCh]
            
    return df

###############################################################################
###############################################################################

def defineDigiBooleans(df, lsDigiCh, digiPHCut, digiTimeCut, bDigiTime):
    for iRun in df["iRun"].unique():
        dfBool = df["iRun"] == iRun
        print("run %s:" % iRun)
        lsPHCuts = []
        lsTimeCuts = []
        
        # PH interval boolean
        if iRun in digiPHCut:
            for iCh in lsDigiCh:
                if iCh in digiPHCut[iRun]:
                    chMin = digiPHCut[iRun][iCh][0]
                    chMax = digiPHCut[iRun][iCh][1]
                    df.loc[dfBool, "boolDigiPH" + iCh] = (df["digiPH" + iCh] > chMin) & (df["digiPH" + iCh] < chMax)
                    lsPHCuts.append(iCh)
                else:
                    df.loc[dfBool, "boolDigiPH" + iCh] = True
            print("cuts added to df: boolDigiPH + %s" % str(lsPHCuts))
            
        else:
            print("run not in digiPHCut --> boolDigiPH... always True for all the channels")
            for iCh in lsDigiCh:
                df.loc[dfBool, "boolDigiPH" + iCh] = True

        # time interval boolean
        if iRun in digiTimeCut:
            for iCh in lsDigiCh:
                if bDigiTime[iCh]:
                    if iCh in digiTimeCut[iRun]:
                        chMin = digiTimeCut[iRun][iCh][0]
                        chMax = digiTimeCut[iRun][iCh][1]
                        df.loc[dfBool, "boolDigiTime" + iCh] = (df["digiTime" + iCh] > chMin) & (df["digiTime" + iCh] < chMax)
                        lsTimeCuts.append(iCh)
                    else:
                        df.loc[dfBool, "boolDigiTime" + iCh] = True
            print("cuts added to df: boolDigiTime + %s" % str(lsTimeCuts))
            
        else:
            print("run not in digiTimeCut --> boolDigiTime... always True for all the channels whose time is available")
            for iCh in lsDigiCh:
                if bDigiTime[iCh]:
                    df.loc[dfBool, "boolDigiTime" + iCh] = True
                    
    return df

###############################################################################
###############################################################################

def caloSum(df, bPHCalo0, lsDigiChCalo, caloName, bOverwrite=True):
    bPHCalo = {}
    for iRun in df["iRun"].unique():
        dfBool = df["iRun"] == iRun
        print("run %s:" % iRun)

        if not bPHCalo0:
            print("PHCalo%s not already in df --> can be created" % caloName)
            strChange = "added to"
        else:
            if bOverwrite:
                print("PHCalo%s already in df with (mean, std) = (%f, %f) --> can be overwritten" % (caloName, df[dfBool]["PHCalo"+caloName].mean(), df[dfBool]["PHCalo"+caloName].std()))
                strChange = "overwritten in"
            else:
                print("PHCalo%s already in df with (mean, std) = (%f, %f) --> keeping it" % (caloName, df[dfBool]["PHCalo"+caloName].mean(), df[dfBool]["PHCalo"+caloName].std()))
        
        # PHCalo... (according to caloName) only created if
        #     - not already in df
        #     - a priori existing in df, but overwriting is required (True by default)
        if (not bPHCalo0) | (bPHCalo0 & bOverwrite):
            if iRun in lsDigiChCalo:
                if len(lsDigiChCalo[iRun])>0:
                    df.loc[dfBool, "PHCalo"+caloName] = sum([df["digiPH" + s] for s in lsDigiChCalo[iRun]])
                    bPHCalo.update({iRun: True})
                    print("PHCalo%s %s df" % (caloName, strChange))
                else:
                    bPHCalo.update({iRun: False})
                    print("PHCalo%s not %s df (list of calo. channels empty for this run)" % (caloName, strChange))
                    if bPHCalo0:
                        print("(despite raw PHCalo%s not being removed from df)" % caloName)
            else:
                bPHCalo.update({iRun: False})
                print("PHCalo%s not %s df (run not in list of calo. channels)" % (caloName, strChange))
                if bPHCalo0:
                    print("(despite raw PHCalo%s not being removed from df)" % caloName)
        else:
            bPHCalo.update({iRun: True})
            
    # note: if PHCalo... already in df + bOverwrite=True + computation not doable for some reason
    #     --> original raw df variable not removed from df, but bPHCalo=False (run by run)
    return df, bPHCalo
    
###############################################################################
###############################################################################
            
def calibrate(df, bE0, calibMap, caloName, bOverwrite=True):
    bE = {}
    for iRun in df["iRun"].unique():
        dfBool = df["iRun"] == iRun
        print("run %s:" % iRun)
            
        if not bE0:
            print("E%s not already in df --> can be created" % caloName)
            strChange = "added to"
        else:
            if bOverwrite:
                print("E%s already in df with (mean, std) = (%f, %f) --> can be overwritten" % (caloName, df[dfBool]["E"+caloName].mean(), df[dfBool]["E"+caloName].std()))
                strChange = "overwritten in"
            else:
                print("E%s already in df with (mean, std) = (%f, %f) --> keeping it" % (caloName, df[dfBool]["E"+caloName].mean(), df[dfBool]["E"+caloName].std()))

        # E... (according to caloName) only created if
        #     - not already in df or a priori existing in df, but overwriting is required (True by default)
        #     - calibration function is defined (for each run)
        #     - total detector PH is available in df
        if (not bE0) | (bE0 & bOverwrite):
            if iRun in calibMap:
                if "PHCalo"+caloName in df.columns:
                    func = calibMap[iRun][0]
                    args = [df["PHCalo" + caloName]] + calibMap[iRun][1]
                    funcSrc = inspect.getsource(func)
                    funcStr = (funcSrc.partition("lambda ")[1]+funcSrc.partition("lambda ")[2]).partition(", 'end'")[0]
                    df.loc[dfBool, "E" + caloName] = func(*args)
                    bE.update({iRun: True})
                    print("E%s %s df -- obtained via %s" % (caloName, strChange, funcStr))
                else:
                    print("E%s not %s df (run not in list of calo. channels)" % (caloName, strChange))
            else:
                bE.update({iRun: False})
                print("E%s not %s df (calib. function not defined for this run)" % (caloName, strChange))
                if bE0:
                    print("(despite raw E%s not being removed from df)" % caloName)
        else:
            bE.update({iRun: True})
            
    # note: if E... already in df + bOverwrite=True + computation not doable for some reason
    #     --> original raw df variable not removed from df, but bE=False (run by run)
    return df, bE