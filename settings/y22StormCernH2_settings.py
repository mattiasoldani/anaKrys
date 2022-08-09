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
for i in range(4): asciiMap.append("xRaw"+str(i))
for i in range(4): asciiMap.append("nStripHit"+str(i))
for i in range(4): asciiMap.append("nHit"+str(i))
for i in range(16): asciiMap.append("digiBaseAll"+str(i))
asciiMap.append("digiPHRawEmpty0")
asciiMap.append("digiPHRawUaglio0")
asciiMap.append("digiPHRawUaglio1")
asciiMap.append("digiPHRawPinin1")
asciiMap.append("digiPHRawPinin0")
for i in range(3): asciiMap.append("digiPHRawEmpty"+str(i+1))
asciiMap.append("digiPHRawCaloFwdBL")
asciiMap.append("digiPHRawCaloFwdBR")
asciiMap.append("digiPHRawCaloFwdCL")
asciiMap.append("digiPHRawCaloFwdCC")
asciiMap.append("digiPHRawCaloFwdCR")
asciiMap.append("digiPHRawCaloFwdTL")
asciiMap.append("digiPHRawCaloFwdTR")
asciiMap.append("digiPHRawEmpty4")
asciiMap.append("digiTimeEmpty0")
asciiMap.append("digiTimeUaglio0")
asciiMap.append("digiTimeUaglio1")
asciiMap.append("digiTimePinin1")
asciiMap.append("digiTimePinin0")
for i in range(4): asciiMap.append("digiTimeEmpty"+str(i+1))
asciiMap.append("digiTimeCaloFwdBL")
asciiMap.append("digiTimeCaloFwdBR")
asciiMap.append("digiTimeCaloFwdCL")
asciiMap.append("digiTimeCaloFwdCC")
asciiMap.append("digiTimeCaloFwdCR")
asciiMap.append("digiTimeCaloFwdTL")
asciiMap.append("digiTimeCaloFwdTR")
asciiMap.append("xGonioRawRot")
asciiMap.append("xGonioRawCrad")
asciiMap.append("xGonioRawHorsa")
asciiMap.append("xGonioRawHorsaBig")
asciiMap.append("xGonioRawVersa")
asciiMap.append("iSpill")
asciiMap.append("iStep")
asciiMap.append("iAEv")

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
for i in range(4):
    filterMap.update({"xRaw"+str(i): [[True, [-20, 20]]]})  # senseful data from input tracking layers

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
for iVar in nRun0:
    z.update({iVar: {
        "0": 0,
        "1": 0,
        "2": 1590,
        "3": 1590,
        "gonio": 1590+157,
        "caloFwd": 1590+157+29,
    }})
    
# base tracking modules, i.e. 4 (2) in the input (output) stage
# list of lists of strings -- shape: [[xIn0, yIn0, xIn1, yIn1], [xOut, yOut]]
# for all the fields, insert the part of the variable name following "xRaw"
# mandatory
baseTrackingMap = [["0", "1", "2", "3"], ["2", "3"]]

# raw input angle distribution centres for modules alignment
# has to be set run by run
# dictionary -- shape: {run (string): [thX, thY] (2 float or None)}
# if None, the raw distributions are centered via their distrbution modes
# set 0 not to apply any shift
# mandatory for all the runs
thInCentres = {}
for iRun in nRun0:
    thInCentres.update({iRun: [-2.367236e-04, 1.050870e-04]})
    
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
#for iRun in nRun0:
#    thOutCentres.update({iRun: [0, 0]})

# crystal fiducial rectangle applied at the crystal longitudinal position z -- boundaries excluded
# has to be set run by run
# dictionary -- shape: {run (string): [xCut0, xCut1, yCut0, yCut1] (4 float)}
# mandatory, but can be skipped for some/all runs --> no cut defined, i.e. boolean always True, in missing runs
xCryCut = {}

# upper/lower limit for low/high output multiplicity selection (included)
# has to be set run by run
# dictionary -- shape: {run (string): [lowWindowCut, upWindowCut] (all float)}
# mandatory, but can be skipped for some/all runs --> no cuts defined, i.e. booleans always True, in missing runs
outMultCut = {}
    
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
    "Horsa": ["xCry0", True, -10],
    "HorsaBig": ["xCry0", True, 2*10],
}  # careful, since run 195 Crad & HorsaBig are inverted wrt. this configuration

########################################################################################################################
# DIGITIZERS

# PH (equalised) cut interval -- inner events kept, boundaries excluded
# has to be set run by run
# dictionary - shape: {run (string): {var (string), [inf, sup] (2 floats)}}
# var format: insert the part of the variable name following "digiPHRaw"
# mandatory, but can be skipped for some/all runs or for some/all channels within a single run
#     --> no cuts defined, i.e. booleans always True, in missing runs/channels
digiPHCut = {}

# time cut interval -- inner events kept, boundaries excluded
# has to be set run by run
# dictionary - shape: {run (string): {var (string), [inf, sup] (2 floats)}}
# var format: insert the part of the variable name following "digiPHRaw"
# mandatory, but can be skipped for some/all runs or for some/all channels within a single run
#     --> no cuts defined, i.e. booleans always True, in missing runs/channels
digiTimeCut = {}
for iRun in nRun0:
    digiTimeCut.update({iRun: {}})
    for i in range(2): digiTimeCut[iRun].update({"Uaglio%d" % i : [0, 20000]})
    for i in range(2): digiTimeCut[iRun].update({"Pinin%d" % i : [0, 20000]})
    for i in range(7): digiTimeCut[iRun].update({"FwdCalo%d" % i : [0, 20000]})

# set of channels that are forward calorimeter channels
# has to be set run by run
# dictionary -- shape: {run: [var0, var1, ...]} (all string)
# varX format: insert the part of the variable name following "digiPHRaw"
# mandatory, but can be skipped for some/all runs --> forward calo. total PH and energy are set to NaN for those runs
lsDigiChCaloFwd = {}
for iRun in nRun0:
    lsDigiChCaloFwd.update({iRun: [
        "CaloFwdBL", "CaloFwdBR", "CaloFwdTL", "CaloFwdTR",
        "CaloFwdCL", "CaloFwdCC", "CaloFwdCR",
    ]})

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
    equalMap.update({iRun: {}})
    equalMap[iRun].update({"CaloFwdBL" : [lambda x, m, q: (x-q)/m, [59.8, -18.6], 'end']})
    equalMap[iRun].update({"CaloFwdBR" : [lambda x, m, q: (x-q)/m, [111.8, 153.9], 'end']})
    equalMap[iRun].update({"CaloFwdCL" : [lambda x, m, q: (x-q)/m, [160.0, 124.9], 'end']})
    equalMap[iRun].update({"CaloFwdCC" : [lambda x, m, q: (x-q)/m, [94.212, 90.313], 'end']})
    equalMap[iRun].update({"CaloFwdCR" : [lambda x, m, q: (x-q)/m, [101.1, -73.3], 'end']})
    equalMap[iRun].update({"CaloFwdTL" : [lambda x, m, q: (x-q)/m, [127.4, 207.9], 'end']})
    equalMap[iRun].update({"CaloFwdTR" : [lambda x, m, q: (x-q)/m, [101.5, 21.9], 'end']})

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
    calibMapFwd.update({iRun: [lambda x, a: x, [1], 'end']})
