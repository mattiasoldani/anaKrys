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
for i in range(8): asciiMap.append("nHit"+str(i))
for i in range(8): asciiMap.append("xRaw"+str(i))
for i in range(4): asciiMap.append("xRaw"+str(4+i)+"_1")  # downstream modules can have double-hit events -- 2nd is "_1"
for i in range(8): asciiMap.append("nStripHit"+str(i))
for i in range(4): asciiMap.append("nStripHit"+str(4+i)+"_1")  # downstream modules can have double-hit events -- 2nd is "_1"
asciiMap.append("xGonioRawRot")
asciiMap.append("xGonioRawCrad")
asciiMap.append("xGonioRawHorsa")
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
for iVar in ["nHit"+s for s in ["0", "1", "2", "3", "4", "5", "6", "7"]]:  # global single-hit condition
    filterMap.update({iVar: [[True, [1, 1]]]})
for iVar in ["xRaw"+s for s in ["0", "1", "2", "3", "4", "5", "6", "7"]]:  # senseful positions in all the layers
    filterMap.update({iVar: [[True, [-20, 20]]]})

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
        "2": 565.5,
        "3": 565.5,
        "4": 565.5+149.1,
        "5": 565.5+149.1,
        "gonio": 565.5+31.2,
        "caloFwd": 0,  # no calorimeter here
        
        "6": 565.5+149.1+86.4,
        "7": 565.5+149.1+86.4,
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
    # thInCentres.update({iRun: [-7.640931e-04, -2.425900e-04]})  # alignment w/ alignment run not perfect
    thInCentres.update({iRun: [None, None]})

# raw output angle distribution centres for modules alignment
# has to be set run by run
# dictionary -- shape: {run (string): [thX, thY] (2 float or None)}
# if None, the raw distributions are centered via their distrbution modes
# set 0 not to apply any shift
# mandatory for all the runs
thOutCentres = {}
for iRun in nRun0:
    # thOutCentres.update({iRun: [4.535002e-02-3.861804e-03-1.754184e-05, 3.690271e-02-1.226760e-03-1.508983e-05]})  # alignment w/ alignment run not perfect
    thOutCentres.update({iRun: [None, None]})

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
    if nRun0[iRun] in [s for s in sorted(nRun0.values()) if "Channeling" in s]:  # strict cut in x for channeling runs (any crystal)
        thInCut.update({iRun: [-0.00005, 0.00005, -0.05, 0.05]})

# crystal fiducial rectangle applied at the crystal longitudinal position z -- boundaries excluded
# has to be set run by run
# dictionary -- shape: {run (string): [xCut0, xCut1, yCut0, yCut1] (4 float)}
# mandatory, but can be skipped for some/all runs --> no cut defined, i.e. boolean always True, in missing runs
xCryCut = {}
for iRun in nRun0:
    if "SiBent16mrad" in nRun0[iRun]:
        xCryCut.update({iRun: [0.97, 1.44, 0.39, 1.90]})

# upper/lower limit for low/high output multiplicity selection (included)
# has to be set run by run
# dictionary -- shape: {run (string): [lowWindowCut, upWindowCut] (all float)}
# mandatory, but can be skipped for some/all runs --> no cuts defined, i.e. booleans always True, in missing runs
outMultCut = {}
for iRun in nRun0:
    outMultCut.update({iRun: [0, 2]})
    
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
    "Rot": ["thIn0", False, -10**6],  # magnitude & sign TBC
    "Crad": ["thIn1", False, 10**6],  # magnitude & sign TBC
    "Horsa": ["xCry0", True, 20],  # magnitude & sign TBC
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

# time cut interval -- inner events kept, boundaries excluded
# has to be set run by run
# dictionary - shape: {run (string): {var (string), [inf, sup] (2 floats)}}
# var format: insert the part of the variable name following "digiPHRaw"
# mandatory, but can be skipped for some/all runs or for some/all channels within a single run
#     --> no cuts defined, i.e. booleans always True, in missing runs/channels
digiTimeCut = {}

# set of channels that are forward calorimeter channels
# has to be set run by run
# dictionary -- shape: {run: [var0, var1, ...]} (all string)
# varX format: insert the part of the variable name following "digiPHRaw"
# mandatory, but can be skipped for some/all runs --> forward calo. total PH and energy are set to NaN for those runs
lsDigiChCaloFwd = {}

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
