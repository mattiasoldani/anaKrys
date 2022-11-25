import os
import importlib

# importing run list from the corresponding settings file (in the same directory as this)
#     --> argument 2 in import_module() (package) must be "settings" ("settings.test") when working with custom (test) data
nRun0 = (importlib.import_module("."+os.path.basename(__file__).replace("settings", "runList").replace(".py", ""), package="settings")).nRun0

########################################################################################################################
# DATA STRUCTURE

# ROOT tree or NumPy array name, string
# mandatory with ROOT/NPZ, useless with ASCII files
treeName = ""

# descaling fraction, i.e. fraction of events to be processed (uniformly distributed along the run)
# the lower is this value, the smaller the loaded dataset
# minimum/maximum: 1 event per file/all the events in the file
# dictionary -- shape: {runNumber (string): value (float)}
# value range: any -- automatically set to 1e-12 (1) if <=0 (>1) (see succolib functions)
# mandatory, but can be left empty --> value set to 1
descFrac = {}

# number of lines per event in the ASCII/NPZ files -- integer >0
# see asciiMap for the variable list format
# mandatory with ASCII/NPZ, useless with ROOT files
nLinesEv = 1

# map of the ASCII/NPZ file variables
# list of strings -- the names must be entered in the list in the same order as the ASCII/NumPy table (left-to-right)
# in case of multiple lines per event (nLinesEv > 1), follow the columns-then-rows order:
#     (0, 0), ..., (0, nCol(0)), (1,0), ..., (1, nCol(1)), ...,  (nLines, 0), ..., (nLines, nCol(nLines))
# mandatory with ASCII/NPZ, useless with ROOT files
asciiMap = list()
for i in range(6): asciiMap.append("xRaw%d" % i)
asciiMap.append("xRaw7")  # last SiBC: x & y swapped
asciiMap.append("xRaw6")  # last SiBC: x & y swapped
for i in range(6): asciiMap.append("nStripHit%d" % i)
asciiMap.append("nStripHit7")  # last SiBC: x & y swapped
asciiMap.append("nStripHit6")  # last SiBC: x & y swapped
for i in range(6): asciiMap.append("nHit%d" % i)
asciiMap.append("nHit7")  # last SiBC: x & y swapped
asciiMap.append("nHit6")  # last SiBC: x & y swapped
for i in range(2): asciiMap.append("digiBaseAPC%d" % i)
for i in range(9): asciiMap.append("digiBaseCaloFwd%d" % i)
asciiMap.append("digiBaseAPC2")
for i in range(4): asciiMap.append("digiBaseEmpty%d" % i)
for i in range(2): asciiMap.append("digiPHRawAPC%d" % i)
for i in range(9): asciiMap.append("digiPHRawCaloFwd%d" % i)
asciiMap.append("digiPHRawAPC2")
for i in range(4): asciiMap.append("digiPHRawEmpty%d" % i)
for i in range(2): asciiMap.append("digiTimeAPC%d" % i)
for i in range(9): asciiMap.append("digiTimeCaloFwd%d" % i)
asciiMap.append("digiTimeAPC2")
for i in range(4): asciiMap.append("digiTimeEmpty%d" % i)
asciiMap.append("xGonioRawRot")
asciiMap.append("xGonioRawCrad")
asciiMap.append("xGonioRawHorsa")
asciiMap.append("xGonioRawHorsaBig")
asciiMap.append("xGonioRawVersa")
asciiMap.append("iSpill")
asciiMap.append("iStep")
asciiMap.append("iEvent")
for i in range(4): asciiMap.append("xCharge%d" % i)
# for j in range(8):
#     for i in range(263): asciiMap.append("wf_"+str(j)+"_"+str(i))

# map of the ROOT tree variables
# dictionary -- shape: {newName: oldName} (all string)
# oldName format: look into the raw ROOT tree for the variable names
# if oldName refers to a multivariable branch, each element must be inserted individually
# mandatory, but can be left empty --> no variable mapping
treeMap = {}
    
# variables to mirror, i.e. var --> -var
# has to be set run by run
# dictionary -- shape: {run: [var]} (all string)
# var format: the full dataframe variable name
# mandatory, but can be skipped/filled with [] for some/all runs --> no variable mirroring for missing runs
mirrorMap = {}
for iRun in nRun0: mirrorMap.update({iRun: ["xRaw7"]})
    
# 1st level data filters
# dictionary -- shape: 
# {var (string): 
#     [
#          [bIncl0 (bool), [low0, up0] (all float)], 
#          [bIncl1, [low1, up1]], 
#          ...
#     ]
# }
# var format: the full dataframe variable name
# selection applied independently on each var: 
#     and/or of all the out-of-range/in-range values for all the (lowX, upX) ranges for which bInclX=False/True
# mandatory, but can be left empty --> no filtering
filterMap = {}
for i in range(4): filterMap.update({"xRaw"+str(i): [[True, [-20, 20]]]})  # senseful data from input tracking layers

########################################################################################################################
# SETUP GEOMETRY & TRACKING

# positions of the setup elements along the beam axis z
# has to be set run by run
# dictionary -- shape: {run (string): {element (string): z (float)}}
# element format:
#     "gonio" for the crystal (base)
#     "caloFwd" for the forward calorimeter (either front or centre) (base)
#     for tracking modules, use the part of the variable name following "xRaw" (base: 4/2 input/output layers)
# mandatory, but can be skipped/filled partially for some/all runs --> all missing base positions set to 0
z = {}
for iRun in nRun0:
    z.update({iRun: {
        "0": 0,
        "1": 0,
        "2": 78.9,
        "3": 78.9,
        "4": 78.9 + 100.15,
        "5": 78.9 + 100.15,
        "gonio": 78.9 + 26.25,
        "caloFwd": 78.9 + 100.15 + 587.6 + 8.5 + 69.7,
        
        "6": 78.9 + 100.15 + 587.6,
        "7": 78.9 + 100.15 + 587.6,
        "APC" : 78.9 + 100.15 + 587.6 + 8.5,
    }})
    
# base tracking modules, i.e. 4 (2) in the input (output) stage
# list of lists of strings -- shape: [[xIn0, yIn0, xIn1, yIn1], [xOut, yOut]]
# for all the fields, insert the part of the variable name following "xRaw"
# mandatory
baseTrackingMap = [["0", "1", "2", "3"], ["4", "5"]]

# raw input angle distribution centres for modules alignment
# has to be set run by run
# dictionary -- shape: {run (string): [thX, thY] (2 float or None)}
# if None, the raw distributions are centered via their distrbution modes
# set 0 not to apply any shift
# mandatory for all the runs
thInCentres = {}
for iRun in nRun0:
    thInCentres.update({iRun: [-1.791140e-03, 5.749927e-03]})
    if (int(iRun) >= 500963):
        thInCentres.update({iRun: [-1.791140e-03+4.818409e-04, 5.749927e-03+1.702944e-04]})  # beam moved a lot in horsa, then recentered
    
# raw output angle distribution centres for modules alignment
# has to be set run by run
# dictionary -- shape: {run (string): [thX, thY] (2 float or None)}
# if None, the raw distributions are centered via their distrbution modes
# set 0 not to apply any shift
# mandatory for all the runs
thOutCentres = {}
for iRun in nRun0:
    thOutCentres.update({iRun: [5.079274e-02, 5.571645e-02]})        

# aligned input angle range cut, centered around 0, boundaries excluded
# has to be set run by run
# dictionary -- shape: {run (string): cut}
# cut format: 
#     if length=1, the only value rCut is the radius of a circular cut
#     if length=2, the 2 values [xCut, yCut] are the half-width values axes of the axes of an elliptical cut
#     if length=4, the 4 values [xCutL, xCutR, yCutL, yCutR] are the boundaries of a rectangular cut
# mandatory, but can be skipped for some/all runs --> no cut defined, i.e. boolean always True, in missing runs
thInCut = {}
for iRun in nRun0:
    thInCut.update({iRun: [0.05]})  # large cut for random (any crystal) and no-crystal runs
    if nRun0[iRun] in [s for s in sorted(nRun0.values()) if "AxisSearch" in s]:  # strict cut for axis search (any crystal)
        thInCut.update({iRun: [0.002]})
    if nRun0[iRun] in [s for s in sorted(nRun0.values()) if "AxisToRandom" in s]:  # intermediate cut for axis-to-random runs (any crystal)
        thInCut.update({iRun: [0.0015]})
        if ("Diamond" in nRun0[iRun]):  # even stricter cuts for Diamond
            thInCut.update({iRun: [0.0005]})
    if nRun0[iRun] in [s for s in sorted(nRun0.values()) if "Axial" in s]:  # strict cut for axial runs (any crystal)
        thInCut.update({iRun: [0.001]})
        if ("Diamond" in nRun0[iRun]):  # even stricter cuts for Diamond
            thInCut.update({iRun: [0.0002]})

# crystal fiducial rectangle applied at the crystal longitudinal position z -- boundaries excluded
# has to be set run by run
# dictionary -- shape: {run (string): [xCut0, xCut1, yCut0, yCut1] (4 float)}
# mandatory, but can be skipped for some/all runs --> no cut defined, i.e. boolean always True, in missing runs
xCryCut = {}
for iRun in nRun0:
    if ("PbF2" in nRun0[iRun]):
        if ("500897" in iRun):  # PbF2 was a bit shifted in 1st random run, moved after that
            xCryCut.update({iRun: [0.55, 10, -10, 10]})
        else:
            xCryCut.update({iRun: [0.22, 10, -10, 10]})
            if (int(iRun) >= 500963):
                xCryCut.update({iRun: [1.0, 1.6, 0.4, 10]})
        
    if ("Diamond" in nRun0[iRun]):
        if ("500948" in iRun):  # diamond was a bit shifted in 1st random run & position check run, moved after that
            xCryCut.update({iRun: [0.75, 1.3, -10, 0.95]})
        elif ("500960" in iRun):  # still tweaking crystal position here
            xCryCut.update({iRun: [1.35, 1.67, 0.59, 1.43]})
        else:
            xCryCut.update({iRun: [1.15, 1.67, 0.49, 1.43]})

# upper/lower limit for low/high output multiplicity selection (included)
# has to be set run by run
# dictionary -- shape: {run (string): [lowWindowCut, upWindowCut] (all float)}
# mandatory, but can be skipped for some/all runs --> no cuts defined, i.e. booleans always True, in missing runs
outMultCut = {}
for iRun in nRun0:
    outMultCut.update({iRun: [1, 4]})
    
########################################################################################################################
# GONIOMETER

# goniometer DOF to be paired to other variables
# dictionary -- shape: {gonioVar (string): param}
# gonioVar format: insert the part of the variable name following "xGonioRaw"
# param format: [pairedVar (string), bShift (bool), scale (float)]
# pairedVar (shifted via its mean if bShift=True) is multiplied to scale and added to gonioVar
# scale can be negative to adjust relative verso
# mandatory, but can be left empty --> no goniometer DOF pairing
gonioMap = {}
gonioMap = { 
    "Rot": ["thIn0", False, -10**6],
    "Crad": ["thIn1", False, -10**6],
}

########################################################################################################################
# DIGITIZERS

# PH (equalised) cut interval -- inner events kept, boundaries excluded
# has to be set run by run
# dictionary - shape: {run (string): {var (string), [inf, sup] (2 floats)}}
# var format: insert the part of the variable name following "digiPHRaw"
# mandatory, but can be skipped for some/all runs or for some/all channels within a single run
#     --> no cuts defined, i.e. booleans always True, in missing runs/channels
digiPHCut = {}
for iRun in nRun0:
    digiPHCut.update({iRun: {}})

# time cut interval -- inner events kept, boundaries excluded
# has to be set run by run
# dictionary - shape: {run (string): {var (string), [inf, sup] (2 floats)}}
# var format: insert the part of the variable name following "digiPHRaw"
# mandatory, but can be skipped for some/all runs or for some/all channels within a single run
#     --> no cuts defined, i.e. booleans always True, in missing runs/channels
digiTimeCut = {}
for iRun in nRun0:
    digiTimeCut.update({iRun: {
        "APC0" : [100, 135],
        "APC1" : [70, 105],
        "CaloFwd0" : [70, 105],
        "CaloFwd1" : [70, 105],
        "CaloFwd2" : [70, 105],
        "CaloFwd3" : [70, 105],
        "CaloFwd4" : [70, 105],
        "CaloFwd5" : [70, 105],
        "CaloFwd6" : [170, 190],
        "CaloFwd7" : [170, 190],
    }})

# set of channels that are forward calorimeter channels
# has to be set run by run
# dictionary -- shape: {run: [var0, var1, ...]} (all string)
# varX format: insert the part of the variable name following "digiPHRaw"
# mandatory, but can be skipped for some/all runs --> forward calo. total PH and energy are set to NaN for those runs
lsDigiChCaloFwd = {}
for iRun in nRun0: lsDigiChCaloFwd.update({iRun: ["CaloFwd"+str(i) for i in range(8)]})  # GENNI ECal -- channels 0-7 (8 broken!)
# for iRun in nRun0: lsDigiChCaloFwd.update({iRun: ["CaloFwd4"]})  # GENNI ECal -- central channel only

# equalisation functions and parameters for channels to be equalised
# has to be set run by run
# dictionary -- shape: {run (string): {var (string): [func, param, 'end']}}
# var format: insert the part of the variable name following "digiPHRaw"
# func format: any function with
#     - the 1st argument, with custom name, as the raw PH to be equalised -- will be inserted automatically
#     - a succession of other N variables with custom names -- these will be the function parameters
# param format: the list of the N parameters values for channel var, in the same order as in func arguments 1-to-N
# the 'end' string (within apostrophes & the precise form ", 'end'") is just a flag needed for some printing
# mandatory, but can be skipped/filled partially for some/all runs --> raw values are kept for missing channels
equalMap = {}
for iRun in nRun0:
    equalMap.update({iRun: {}})  # nonlinear equalisation -- reference channel is 4
    equalMap[iRun].update({"CaloFwd0": [lambda x, a: x*a, [0.461320], 'end']})
    equalMap[iRun].update({"CaloFwd1": [lambda x, a: x*a, [0.618319], 'end']})
    equalMap[iRun].update({"CaloFwd2": [lambda x, a: x*a, [0.580172], 'end']})
    equalMap[iRun].update({"CaloFwd3": [lambda x, a: x*a, [0.559943], 'end']})
    equalMap[iRun].update({"CaloFwd4": [lambda x, a: x*a, [1], 'end']})
    equalMap[iRun].update({"CaloFwd5": [lambda x, a: x*a, [0.882152], 'end']})
    equalMap[iRun].update({"CaloFwd6": [lambda x, a: x*a, [0.553153], 'end']})
    equalMap[iRun].update({"CaloFwd7": [lambda x, a: x*a, [1.063839], 'end']})
            
# (total) forward calorimeter calibration function and parameters
# has to be set run by run
# dictionary -- shape: {run (string): [func, param, 'end']}
# func format: any function with
#     - the 1st argument, with custom name, as the PH to be calibrated -- will be inserted automatically
#     - a succession of other N variables with custom names -- these will be the function parameters
# param format: the list of the N parameters values, in the same order as in func arguments 1-to-N
# the 'end' string (within apostrophes & the precise form ", 'end'") is just a flag needed for some printing
# mandatory, but can be skipped for some/all runs --> forward calo. energy is set to NaN for those runs
calibMapFwd = {}
for iRun in nRun0:
    calibMapFwd.update({iRun: [lambda x, a, b, c: a*x*x+b*x+c, [3.49e-08, 0.0005343, 0.1489], 'end']})  # linear calibration -- ADC version (to get plain total PH -- equalised)