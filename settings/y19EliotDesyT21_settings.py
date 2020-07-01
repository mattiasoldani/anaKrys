import os
import importlib

# importing run list from the corresponding settings file (in the same directory as this)
#     --> argument 2 in import_module() (package) must be "settings" ("settings.test") when working with custom (test) data
nRun0 = (importlib.import_module("."+os.path.basename(__file__).replace("settings", "runList").replace(".py", ""), package="settings")).nRun0

########################################################################################################################
# DATA STRUCTURE

# ROOT tree name, string
# mandatory with ROOT, useless with ASCII files
treeName = ""

# descaling fraction, i.e. fraction of events to be processed (uniformly distributed along the run)
# the lower is this value, the smaller the loaded dataset
# minimum/maximum: 1 event per file/all the events in the file
# dictionary -- shape: {runNumber (string): value (float)}
# value range: any -- automatically set to 1e-12 (1) if <=0 (>1) (see succolib functions)
# mandatory, but can be left empty --> value set to 1
descFrac = {}

# number of lines per event in the ASCII files -- integer >0
# see asciiMap for the variable list format
# mandatory with ASCII, useless with ROOT files
nLinesEv = 1

# map of the ASCII file variables
# list of strings -- the names must be entered in the list in the same order as the ASCII table (left-to-right)
# in case of multiple lines per event (nLinesEv > 1), follow the columns-then-rows order:
#     (0, 0), ..., (0, nCol(0)), (1,0), ..., (1, nCol(1)), ...,  (nLines, 0), ..., (nLines, nCol(nLines))
# mandatory with ASCII, useless with ROOT files
asciiMap = list()
asciiMap.append("epoch")
asciiMap.append("iEvent")
for i in range(8): asciiMap.append("xRaw%d" % i)
for i in range(8): asciiMap.append("nHit%d" % i)
asciiMap.append("xGonioRawRot")
asciiMap.append("xGonioRawCrad")
asciiMap.append("xGonioRawHorsa")
asciiMap.append("xGonioRawHorsaBig")
asciiMap.append("xGonioRawVersa")
asciiMap.append("iSpill")
asciiMap.append("iStep")
for i in range(16): asciiMap.append("digiBase%d" % i)
for i in range(16): asciiMap.append("digiPHRaw%d" % i)
for i in range(16): asciiMap.append("digiTime%d" % i)

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
for iRun in nRun0: mirrorMap.update({iRun: ["xRaw4", "xRaw7"]})  # planes 4 & 7 swapped
    
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
# mandatory, but can be skipped/filled partially for some/all runs --> all missing base positions set to 0
z = {}
for iRun in nRun0:
    z.update({iRun: {
        "0": 0,
        "1": 0,
        "2": 41.0,
        "3": 41.0,
        "4": 41.0 + 22.75 + 45.3 - 2.4,
        "5": 41.0 + 22.75 + 45.3 - 2.4,
        "gonio": 41.0 + 22.75,
        "caloFwd": 41.0 + 22.75 + 64.4 + 8 + 685.0 + 8.0 + 2.4 + 22.4 + 8.0,
        
        "6": 41.0 + 22.75 + 45.3 - 2.4 + 690.6 + 29.5 + 4.8,
        "7": 41.0 + 22.75 + 45.3 - 2.4 + 690.6 + 29.5 + 4.8,
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
    thInCentres.update({iRun: [-5.490719e-03, -4.515025e-03]})
    
# raw output angle distribution centres for modules alignment
# has to be set run by run
# dictionary -- shape: {run (string): [thX, thY] (2 float or None)}
# if None, the raw distributions are centered via their distrbution modes
# set 0 not to apply any shift
# mandatory for all the runs
thOutCentres = {}
for iRun in nRun0:
    thOutCentres.update({iRun: [0, 0]})

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
    thInCut.update({iRun: [0.05, 0.05]})  # large cut for random (any crystal) and no-crystal runs
    if nRun0[iRun] in [s for s in sorted(nRun0.values()) if "AxisToRandom" in s]:  # intermediate cut for axis-to-random runs (any crystal)
        thInCut.update({iRun: [0.0015, 0.0015]})
    if nRun0[iRun] in [s for s in sorted(nRun0.values()) if "Axial" in s]:  # strict cut for axial runs (any crystal)
        thInCut.update({iRun: [0.0009, 0.0009]})

# crystal fiducial rectangle applied at the crystal longitudinal position z -- boundaries excluded
# has to be set run by run
# dictionary -- shape: {run (string): [xCut0, xCut1, yCut0, yCut1] (4 float)}
# mandatory, but can be skipped for some/all runs --> no cut defined, i.e. boolean always True, in missing runs
xCryCut = {}
for iRun in nRun0:
    xCryCut.update({iRun: [-10, 10, -10, 10]})  # no cut in general
    
    # W [100] "square"
    if "WSquare" in nRun0[iRun]:
        if "Axial" in nRun0[iRun]:
            xCryCut.update({iRun: [0.5, 1.1, 1.1, 1.7]})  # axial runs
        elif "Random0" in nRun0[iRun]:
            xCryCut.update({iRun: [0.55, 0.95, 1.21, 1.61]})  # random (1st set) runs
        elif "Random1" in nRun0[iRun]:
            xCryCut.update({iRun: [0.52, 0.92, 1.25, 1.65]})  # random (2nd set) runs
        else:
            xCryCut.update({iRun: [0.6, 1.0, 1.2, 1.6]})  # all other runs runs (i.e. scans)
        if "Old" in nRun0[iRun]:
            xCryCut.update({iRun: [1.1, 1.5, 1.0, 1.4]})  # any run type with old tracking system positioning (before magnet accident)
            
    # PWO [100] "thick"
    elif "PWOThick" in nRun0[iRun]:
        xCryCut.update({iRun: [0.3, 1.95, 0.25, 1.9]})
        
    # PWO [100] "strip"
    elif "PWOStrip" in nRun0[iRun]:
        xCryCut.update({iRun: [0.95, 1.25, 0.45, 1.85]})

# upper/lower limit for low/high output multiplicity selection (included)
# has to be set run by run
# dictionary -- shape: {run (string): [lowWindowCut, upWindowCut] (all float)}
# mandatory, but can be skipped for some/all runs --> no cuts defined, i.e. booleans always True, in missing runs
outMultCut = {}
for iRun in nRun0:
    outMultCut.update({iRun: [1, 2.5]})
    
########################################################################################################################
# GONIOMETER

# goniometer DOF to be paired to other variables
# dictionary -- shape: {gonioVar (string): param}
# gonioVar format: insert the part of the variable name following "xGonioRaw"
# param format: [pairedVar (string), bShift (bool), scale (float)]
# pairedVar (shifted via its mean if bShift=True) is multiplied to scale and added to gonioVar
# scale can be negative to adjust relative verso
# mandatory, but can be left empty --> no goniometer DOF pairing
gonioMap = { 
    "Rot": ["thIn0", False, -10**6],
    "Crad": ["thIn1", False, 10**6],
    "Horsa": ["xCry0", True, 10],
    "HorsaBig": ["xCry0", True, 20],
    "Versa": ["xCry1", True, -10],
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
    digiPHCut[iRun].update({"10": [-999999, 150]})  # veto scinti -- channel 10
    for s in [str(i) for i in range(9)]:  # GENNI ECal -- channels 0-8
        digiPHCut[iRun].update({s: [20, 999999]})

# time cut interval -- inner events kept, boundaries excluded
# has to be set run by run
# dictionary - shape: {run (string): {var (string), [inf, sup] (2 floats)}}
# var format: insert the part of the variable name following "digiPHRaw"
# mandatory, but can be skipped for some/all runs or for some/all channels within a single run
#     --> no cuts defined, i.e. booleans always True, in missing runs/channels
digiTimeCut = {}
for iRun in nRun0:
    digiTimeCut.update({iRun: {}})
    digiTimeCut[iRun].update({"9": [215, 227]})  # trigger scinti (between crystal & output tracking module) -- channel 9
    digiTimeCut[iRun].update({"10": [163, 178]})  # veto scinti -- channel 10
    digiTimeCut[iRun].update({"11": [160, 175]})  # preshower output scinti -- channel 11
    digiTimeCut[iRun].update({"12": [165, 180]})  # preshower output scinti -- channel 12
    for s in [str(i) for i in range(9)]:  # GENNI ECal -- channels 0-8
        digiTimeCut[iRun].update({s: [230, 260]})
        if s == "8": digiTimeCut[iRun].update({s: [165, 195]})  # channel 8 in 2nd digitizer

# set of channels that are forward calorimeter channels
# has to be set run by run
# dictionary -- shape: {run: [var0, var1, ...]} (all string)
# varX format: insert the part of the variable name following "digiPHRaw"
# mandatory, but can be skipped for some/all runs --> forward calo. total PH and energy are set to NaN for those runs
lsDigiChCaloFwd = {}
for iRun in nRun0: lsDigiChCaloFwd.update({iRun: [str(i) for i in range(9)]})  # GENNI ECal -- channels 0-8

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
    equalMap[iRun].update({"0": [lambda x, a, b, aRef, bRef: x*aRef / (x*bRef + a - x*b), [3625.58, 0.10505, 1818.46, 0.07281], 'end']})
    equalMap[iRun].update({"1": [lambda x, a, b, aRef, bRef: x*aRef / (x*bRef + a - x*b), [2039.81, 0.06787, 1818.46, 0.07281], 'end']})
    equalMap[iRun].update({"2": [lambda x, a, b, aRef, bRef: x*aRef / (x*bRef + a - x*b), [2338.31, 0.04680, 1818.46, 0.07281], 'end']})
    equalMap[iRun].update({"3": [lambda x, a, b, aRef, bRef: x*aRef / (x*bRef + a - x*b), [3129.84, 0.08349, 1818.46, 0.07281], 'end']})
    equalMap[iRun].update({"4": [lambda x, a, b, aRef, bRef: x*aRef / (x*bRef + a - x*b), [1818.46, 0.07281, 1818.46, 0.07281], 'end']})
    equalMap[iRun].update({"5": [lambda x, a, b, aRef, bRef: x*aRef / (x*bRef + a - x*b), [1528.03, 0.04487, 1818.46, 0.07281], 'end']})
    equalMap[iRun].update({"6": [lambda x, a, b, aRef, bRef: x*aRef / (x*bRef + a - x*b), [2676.66, 0.05874, 1818.46, 0.07281], 'end']})
    equalMap[iRun].update({"7": [lambda x, a, b, aRef, bRef: x*aRef / (x*bRef + a - x*b), [2098.63, 0.37278, 1818.46, 0.07281], 'end']})
    equalMap[iRun].update({"8": [lambda x, a, b, aRef, bRef: x*aRef / (x*bRef + a - x*b), [1532.67, 0.04095, 1818.46, 0.07281], 'end']})
            
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
    calibMapFwd.update({iRun: [lambda x, a, b: a*x+b, [1/1892.03, -527.21/1892.03], 'end']})  # linear calibration
