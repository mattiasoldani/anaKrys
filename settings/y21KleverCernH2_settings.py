import os
import importlib

# importing run list from the corresponding settings file (in the same directory as this)
#     --> argument 2 in import_module() (package) must be "settings" ("settings.test") when working with custom (test) data
nRun0 = (importlib.import_module("."+os.path.basename(__file__).replace("settings", "runList").replace(".py", ""), package="settings")).nRun0

########################################################################################################################
# DATA STRUCTURE

# ROOT tree or NumPy array name, string
# mandatory with ROOT/NPZ, useless with ASCII files
treeName = "t"

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
nLinesEv = 1  # 1 for ASCII w/o waveforms, 9 for ASCII w/ waveforms

# map of the ASCII/NPZ file variables
# list of strings -- the names must be entered in the list in the same order as the ASCII/NumPy table (left-to-right)
# in case of multiple lines per event (nLinesEv > 1), follow the columns-then-rows order:
#     (0, 0), ..., (0, nCol(0)), (1,0), ..., (1, nCol(1)), ...,  (nLines, 0), ..., (nLines, nCol(nLines))
# mandatory with ASCII/NPZ, useless with ROOT files
asciiMap = list()
for i in range(8): asciiMap.append("xRaw"+str(i))
for i in range(8): asciiMap.append("nStripHit"+str(i))
for i in range(8): asciiMap.append("nHit"+str(i))
asciiMap.append("digiBaseEmpty0")
asciiMap.append("digiBaseVeto")
for i in range(2): asciiMap.append("digiBaseCaloLat%d" % (2+i))
asciiMap.append("digiBaseVetoSmall")
asciiMap.append("digiBaseCounterOutSmall")
asciiMap.append("digiBaseCounterBeforeMagnet")  # MCP0 in some old runs (e.g. 500619)
asciiMap.append("digiBaseEmpty1")  # MCP1 in some old runs (e.g. 500619)
for i in range(9): asciiMap.append("digiBaseCaloFwd"+str(i))
for i in range(2): asciiMap.append("digiBaseCaloLat"+str(i))
for i in range(5): asciiMap.append("digiBaseCaloLat%d" % (4+i))
for i in range(4): asciiMap.append("digiBaseSiPM"+str(i))
asciiMap.append("digiBaseEmpty2")
asciiMap.append("digiBaseCounterOut")
for i in range(2): asciiMap.append("digiBaseMCP"+str(i))  
asciiMap.append("digiPHRawEmpty0")
asciiMap.append("digiPHRawVeto")
for i in range(2): asciiMap.append("digiPHRawCaloLat%d" % (2+i))
asciiMap.append("digiPHRawVetoSmall")
asciiMap.append("digiPHRawCounterOutSmall")
asciiMap.append("digiPHRawCounterBeforeMagnet")  # MCP0 in some old runs (e.g. 500619)
asciiMap.append("digiPHRawEmpty1")  # MCP1 in some old runs (e.g. 500619)
for i in range(9): asciiMap.append("digiPHRawCaloFwd"+str(i))
for i in range(2): asciiMap.append("digiPHRawCaloLat"+str(i))
for i in range(5): asciiMap.append("digiPHRawCaloLat%d" % (4+i))
for i in range(4): asciiMap.append("digiPHRawSiPM"+str(i))
asciiMap.append("digiPHRawEmpty2")
asciiMap.append("digiPHRawCounterOut")
for i in range(2): asciiMap.append("digiPHRawMCP"+str(i))
asciiMap.append("digiTimeEmpty0")
asciiMap.append("digiTimeVeto")
for i in range(2): asciiMap.append("digiTimeCaloLat%d" % (2+i))
asciiMap.append("digiTimeVetoSmall")
asciiMap.append("digiTimeCounterOutSmall")
asciiMap.append("digiTimeCounterBeforeMagnet")  # MCP0 in some old runs (e.g. 500619)
asciiMap.append("digiTimeEmpty1")  # MCP1 in some old runs (e.g. 500619)
for i in range(9): asciiMap.append("digiTimeCaloFwd"+str(i))
for i in range(2): asciiMap.append("digiTimeCaloLat"+str(i))
for i in range(5): asciiMap.append("digiTimeCaloLat%d" % (4+i))
for i in range(4): asciiMap.append("digiTimeSiPM"+str(i))
asciiMap.append("digiTimeEmpty2")
asciiMap.append("digiTimeCounterOut")
for i in range(2): asciiMap.append("digiTimeMCP"+str(i))  
asciiMap.append("xGonioRawRot")
asciiMap.append("xGonioRawCrad")
asciiMap.append("xGonioRawHorsa")
asciiMap.append("xGonioRawHorsaBig")
asciiMap.append("xGonioRawVersa")
asciiMap.append("iSpill")
asciiMap.append("iStep")  # here iStep is important for position splitting in scan runs
asciiMap.append("iAbsEv")
# for i in range(1031): asciiMap.append("wfSiPM0_"+str(i))
# for i in range(1031): asciiMap.append("wfSiPM1_"+str(i))
# for i in range(1031): asciiMap.append("wfSiPM2_"+str(i))
# for i in range(1031): asciiMap.append("wfSiPM3_"+str(i))
# for i in range(1031): asciiMap.append("wfEmpty_"+str(i))
# for i in range(1031): asciiMap.append("wfCounterOut_"+str(i))
# for i in range(1031): asciiMap.append("wfMCP0_"+str(i))
# for i in range(1031): asciiMap.append("wfMCP1_"+str(i))

# map of the ROOT tree variables
# dictionary -- shape: {newName: oldName} (all string)
# oldName format: look into the raw ROOT tree for the variable names
# if oldName refers to a multivariable branch, each element must be inserted individually
# mandatory, but can be left empty --> no variable mapping
treeMap = {}
treeMap.update({"digiBaseEmpty0" : "digiBase0"})
treeMap.update({"digiBaseVeto" : "digiBase1"})
for i in range(2): treeMap.update({"digiBaseCaloLat%d" % (2+i) : "digiBase%d" % (2+i)})
treeMap.update({"digiBaseVetoSmall" : "digiBase4"})
treeMap.update({"digiBaseCounterOutSmall" : "digiBase5"})
treeMap.update({"digiBaseCounterBeforeMagnet" : "digiBase6"})  # MCP0 in some old runs (e.g. 500619)
treeMap.update({"digiBaseEmpty1" : "digiBase7"})  # MCP1 in some old runs (e.g. 500619)
for i in range(9): treeMap.update({"digiBaseCaloFwd%d" % i : "digiBase%d" % (8+i)})
for i in range(2): treeMap.update({"digiBaseCaloLat%d" % i : "digiBase%d" % (17+i)})
for i in range(5): treeMap.update({"digiBaseCaloLat%d" % (4+i) : "digiBase%d" % (19+i)})
for i in range(4): treeMap.update({"digiBaseSiPM%d" % i : "digiBase%d" % (24+i)})
treeMap.update({"digiBaseEmpty2" : "digiBase28"})
treeMap.update({"digiBaseCounterOut" : "digiBase29"})
for i in range(2): treeMap.update({"digiBaseMCP%d" % i : "digiBase%d" % (30+i)})                        
treeMap.update({"digiPHRawEmpty0" : "digiPh0"})
treeMap.update({"digiPHRawVeto" : "digiPh1"})
for i in range(2): treeMap.update({"digiPHRawCaloLat%d" % (2+i) : "digiPh%d" % (2+i)})
treeMap.update({"digiPHRawVetoSmall" : "digiPh4"})
treeMap.update({"digiPHRawCounterOutSmall" : "digiPh5"})
treeMap.update({"digiPHRawCounterBeforeMagnet" : "digiPh6"})  # MCP0 in some old runs (e.g. 500619)
treeMap.update({"digiPHRawEmpty1" : "digiPh7"})  # MCP1 in some old runs (e.g. 500619)
for i in range(9): treeMap.update({"digiPHRawCaloFwd%d" % i : "digiPh%d" % (8+i)})
for i in range(2): treeMap.update({"digiPHRawCaloLat%d" % i : "digiPh%d" % (17+i)})
for i in range(5): treeMap.update({"digiPHRawCaloLat%d" % (4+i) : "digiPh%d" % (19+i)})
for i in range(4): treeMap.update({"digiPHRawSiPM%d" % i : "digiPh%d" % (24+i)})
treeMap.update({"digiPHRawEmpty2" : "digiPh28"})
treeMap.update({"digiPHRawCounterOut" : "digiPh29"})
for i in range(2): treeMap.update({"digiPHRawMCP%d" % i : "digiPh%d" % (30+i)})                        
treeMap.update({"digiTimeEmpty0" : "digiTime0"})
treeMap.update({"digiTimeVeto" : "digiTime1"})
for i in range(2): treeMap.update({"digiTimeCaloLat%d" % (2+i) : "digiTime%d" % (2+i)})
treeMap.update({"digiTimeVetoSmall" : "digiTime4"})
treeMap.update({"digiTimeCounterOutSmall" : "digiTime5"})
treeMap.update({"digiTimeCounterBeforeMagnet" : "digiTime6"})  # MCP0 in some old runs (e.g. 500619)
treeMap.update({"digiTimeEmpty1" : "digiTime7"})  # MCP1 in some old runs (e.g. 500619)
for i in range(9): treeMap.update({"digiTimeCaloFwd%d" % i : "digiTime%d" % (8+i)})
for i in range(2): treeMap.update({"digiTimeCaloLat%d" % i : "digiTime%d" % (17+i)})
for i in range(5): treeMap.update({"digiTimeCaloLat%d" % (4+i) : "digiTime%d" % (19+i)})
for i in range(4): treeMap.update({"digiTimeSiPM%d" % i : "digiTime%d" % (24+i)})
treeMap.update({"digiTimeEmpty2" : "digiTime28"})
treeMap.update({"digiTimeCounterOut" : "digiTime29"})
for i in range(2): treeMap.update({"digiTimeMCP%d" % i : "digiTime%d" % (30+i)})
treeMap.update({"xGonioRawRot" : "gonio0"})
treeMap.update({"xGonioRawCrad" : "gonio1"})
treeMap.update({"xGonioRawHorsa" : "gonio2"})
treeMap.update({"xGonioRawHorsaBig" : "gonio3"})
treeMap.update({"xGonioRawVersa" : "gonio4"})
treeMap.update({"iSpill" : "spill"})
treeMap.update({"iStep" : "step"})
for i in range(1031): treeMap.update({"wfSiPM0_%d" % i : "wave0%d" % i})
for i in range(1031): treeMap.update({"wfSiPM1_%d" % i : "wave1%d" % i})
for i in range(1031): treeMap.update({"wfSiPM2_%d" % i : "wave2%d" % i})
for i in range(1031): treeMap.update({"wfSiPM3_%d" % i : "wave3%d" % i})
for i in range(1031): treeMap.update({"wfEmpty_%d" % i : "wave4%d" % i})
for i in range(1031): treeMap.update({"wfCounterOut0_%d" % i : "wave5%d" % i})
for i in range(1031): treeMap.update({"wfMCP0_%d" % i : "wave6%d" % i})
for i in range(1031): treeMap.update({"wfMCP1_%d" % i : "wave7%d" % i})
    
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
        "2": 1365,
        "3": 1365,
        "4": 1365+525+4.5,
        "5": 1365+525+4.5,
        "6": 1365+525+4.5+976.7+394.1+5+7,
        "7": 1365+525+4.5+976.7+394.1+5+7,
        "gonio": 1365+525+4.5+976.7,
        "caloFwd": 0,  # TBC
    }})
    
# base tracking modules, i.e. 4 (2) in the input (output) stage
# list of lists of strings -- shape: [[xIn0, yIn0, xIn1, yIn1], [xOut, yOut]]
# for all the fields, insert the part of the variable name following "xRaw"
# mandatory
baseTrackingMap = [["0", "1", "2", "3"], ["6", "7"]]

# raw input angle distribution centres for modules alignment
# has to be set run by run
# dictionary -- shape: {run (string): [thX, thY] (2 float or None)}
# if None, the raw distributions are centered via their distrbution modes
# set 0 not to apply any shift
# mandatory for all the runs
thInCentres = {}
for iRun in nRun0:
    thInCentres.update({iRun: [0, 0]})
    if ("PbF2" in nRun0[iRun]):
        thInCentres.update({iRun: [-3.284821e-05-1.222887e-05, 1.410627e-04+5.150415e-06]})
    elif ("PWO1X0" in nRun0[iRun]):
        thInCentres.update({iRun: [-4.515854e-05, 1.461665e-04]})
    
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
    thInCut.update({iRun: [0.01, 0.01]})  # large cut for random (any crystal) and no-crystal runs
    if ("Axial" in nRun0[iRun]):
        thInCut.update({iRun: [1e-3, 1e-3]})

# crystal fiducial rectangle applied at the crystal longitudinal position z -- boundaries excluded
# has to be set run by run
# dictionary -- shape: {run (string): [xCut0, xCut1, yCut0, yCut1] (4 float)}
# mandatory, but can be skipped for some/all runs --> no cut defined, i.e. boolean always True, in missing runs
xCryCut = {}
for iRun in nRun0:
    if ("PbF2" in nRun0[iRun]):
        xCryCut.update({iRun: [0.95, 1.72, -10, 10]})

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
gonioMap = { 
    "Rot": ["thIn0", False, -10**6],
    "Crad": ["thIn1", False, 10**6],
    "Horsa": ["xCry0", True, 10],
    "HorsaBig": ["xCry0", True, 2*10],
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

# time cut interval -- inner events kept, boundaries excluded
# has to be set run by run
# dictionary - shape: {run (string): {var (string), [inf, sup] (2 floats)}}
# var format: insert the part of the variable name following "digiPHRaw"
# mandatory, but can be skipped for some/all runs or for some/all channels within a single run
#     --> no cuts defined, i.e. booleans always True, in missing runs/channels
digiTimeCut = {}
for iRun in nRun0:
    digiTimeCut.update({iRun: {}})
    digiTimeCut[iRun].update({"CounterOut" : [650, 750]})
    for i in range(4): digiTimeCut[iRun].update({"SiPM%d" % i : [530, 610]})
    for i in range(8): digiTimeCut[iRun].update({"CaloFwd%d" % i : [75, 100]})
    digiTimeCut[iRun].update({"CaloFwd8" : [85, 120]})

# set of channels that are forward calorimeter channels
# has to be set run by run
# dictionary -- shape: {run: [var0, var1, ...]} (all string)
# varX format: insert the part of the variable name following "digiPHRaw"
# mandatory, but can be skipped for some/all runs --> forward calo. total PH and energy are set to NaN for those runs
lsDigiChCaloFwd = {}
for iRun in nRun0:
    lsDigiChCaloFwd.update({iRun: ["CaloFwd%d" % i for i in range(9)]})

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
    equalMap[iRun].update({"CaloFwd0" : [lambda x, a: a*x, [0.94143814], 'end']})
    equalMap[iRun].update({"CaloFwd1" : [lambda x, a: a*x, [1.9040481], 'end']})
    equalMap[iRun].update({"CaloFwd2" : [lambda x, a: a*x, [1.4871194], 'end']})
    equalMap[iRun].update({"CaloFwd3" : [lambda x, a: a*x, [1.3655914], 'end']})
    equalMap[iRun].update({"CaloFwd4" : [lambda x, a: a*x, [3.5277777], 'end']})
    equalMap[iRun].update({"CaloFwd5" : [lambda x, a: a*x, [2.8863637], 'end']})
    equalMap[iRun].update({"CaloFwd6" : [lambda x, a: a*x, [1.1179577], 'end']})
    equalMap[iRun].update({"CaloFwd7" : [lambda x, a: a*x, [1], 'end']})
    equalMap[iRun].update({"CaloFwd8" : [lambda x, a: a*x, [0.62254900], 'end']})
    equalMap[iRun].update({"CaloLat0" : [lambda x, a: x/a, [1], 'end']})
    equalMap[iRun].update({"CaloLat1" : [lambda x, a: x/a, [0.582], 'end']})  

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
    calibMapFwd.update({iRun: [lambda x, a, b: (x+a)/b, [-102.007, 107.61], 'end']})