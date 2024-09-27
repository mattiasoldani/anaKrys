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
nLinesEv = 1

# map of the ASCII/NPZ file variables
# list of strings -- the names must be entered in the list in the same order as the ASCII/NumPy table (left-to-right)
# in case of multiple lines per event (nLinesEv > 1), follow the columns-then-rows order:
#     (0, 0), ..., (0, nCol(0)), (1,0), ..., (1, nCol(1)), ...,  (nLines, 0), ..., (nLines, nCol(nLines))
# mandatory with ASCII/NPZ, useless with ROOT files
asciiMap = list()

for i in range(4): asciiMap.append("xRaw"+str(i))
#for i in range(4): asciiMap.append("nStripHit"+str(i))

#icrilin=0
#for i in range(64):
#    if (i==57):
#        asciiMap.append("digiBaseCaloFwd")
#    elif (i==53):
#        asciiMap.append("digiBaseTiming0")
#    elif (i==54):
#        asciiMap.append("digiBaseTiming1")
#    elif (((i>=0) & (i<32)) | (i>=49) & (i<53)):
#        asciiMap.append("digiBaseCrilin%d"%icrilin)
#        icrilin+=1
#    else:
#        asciiMap.append("digiBase%d"%i)
#
#icrilin=0
#for i in range(64):
#    if (i==57):
#        asciiMap.append("digiTimeCaloFwd")
#    elif (i==53):
#        asciiMap.append("digiTimeTiming0")
#    elif (i==54):
#        asciiMap.append("digiTimeTiming1")
#    elif (((i>=0) & (i<32)) | (i>=49) & (i<53)):
#        asciiMap.append("digiTimeCrilin%d"%icrilin)
#        icrilin+=1
#    else:
#        asciiMap.append("digiTime%d"%i)
#
#icrilin=0
#for i in range(64):
#    if (i==57):
#        asciiMap.append("digiHalfTimeCaloFwd")
#    elif (i==53):
#        asciiMap.append("digiHalfTimeTiming0")
#    elif (i==54):
#        asciiMap.append("digiHalfTimeTiming1")
#    elif (((i>=0) & (i<32)) | (i>=49) & (i<53)):
#        asciiMap.append("digiHalfTimeCrilin%d"%icrilin)
#        icrilin+=1
#    else:
#        asciiMap.append("digiHalfTime%d"%i)
#
#icrilin=0
#for i in range(64):
#    if (i==57):
#        asciiMap.append("digiPHRawCaloFwd")
#    elif (i==53):
#        asciiMap.append("digiPHRawTiming0")
#    elif (i==54):
#        asciiMap.append("digiPHRawTiming1")
#    elif (((i>=0) & (i<32)) | (i>=49) & (i<53)):
#        asciiMap.append("digiPHRawCrilin%d"%icrilin)
#        icrilin+=1
#    else:
#        asciiMap.append("digiPHRaw%d"%i)

igarbage=0

for i in range(64):
    if (i==57):
        asciiMap.append("digiBaseCaloFwd")
    elif (i==56):
        asciiMap.append("digiBaseCiofex")
    elif (i==8):
        asciiMap.append("digiBaseCrilin8")
    elif (i==9):
        asciiMap.append("digiBaseCrilin9")
    elif (i==60):
        asciiMap.append("digiBaseCher0")
    elif (i==61):
        asciiMap.append("digiBaseCher1")
    elif (i==62):
        asciiMap.append("digiBaseFiorello0")
    elif (i==63):
        asciiMap.append("digiBaseFiorello1")
    else:
        asciiMap.append("Garbage%d"%igarbage)
        igarbage+=1

for i in range(64):
    if (i==57):
        asciiMap.append("digiTimeCaloFwd")
    elif (i==56):
        asciiMap.append("digiTimeCiofex")
    elif (i==8):
        asciiMap.append("digiTimeCrilin8")
    elif (i==9):
        asciiMap.append("digiTimeCrilin9")
    elif (i==60):
        asciiMap.append("digiTimeCher0")
    elif (i==61):
        asciiMap.append("digiTimeCher1")
    elif (i==62):
        asciiMap.append("digiTimeFiorello0")
    elif (i==63):
        asciiMap.append("digiTimeFiorello1")
    else:
        asciiMap.append("Garbage%d"%igarbage)
        igarbage+=1

for i in range(64):
    if (i==57):
        asciiMap.append("digiHalfTimeCaloFwd")
    elif (i==56):
        asciiMap.append("digiHalfTimeCiofex")
    elif (i==8):
        asciiMap.append("digiHalfTimeCrilin8")
    elif (i==9):
        asciiMap.append("digiHalfTimeCrilin9")
    elif (i==60):
        asciiMap.append("digiHalfTimeCher0")
    elif (i==61):
        asciiMap.append("digiHalfTimeCher1")
    elif (i==62):
        asciiMap.append("digiHalfTimeFiorello0")
    elif (i==63):
        asciiMap.append("digiHalfTimeFiorello1")
    else:
        asciiMap.append("Garbage%d"%igarbage)
        igarbage+=1

for i in range(64):
    if (i==57):
        asciiMap.append("digiPHRawCaloFwd")
    elif (i==56):
        asciiMap.append("digiPHRawCiofex")
    elif (i==8):
        asciiMap.append("digiPHRawCrilin8")
    elif (i==9):
        asciiMap.append("digiPHRawCrilin9")
    elif (i==60):
        asciiMap.append("digiPHRawCher0")
    elif (i==61):
        asciiMap.append("digiPHRawCher1")
    elif (i==62):
        asciiMap.append("digiPHRawFiorello0")
    elif (i==63):
        asciiMap.append("digiPHRawFiorello1")
    else:
        asciiMap.append("Garbage%d"%igarbage)
        igarbage+=1

asciiMap.append("xGonioRawRot")
asciiMap.append("xGonioRawCrad")
asciiMap.append("xGonioRawHorsa")
asciiMap.append("xGonioRawHorsaBig")
asciiMap.append("xGonioRawVersa")

for i in range(9): asciiMap.append("iDummy%d"%i)

# map of the ROOT tree variables
# dictionary -- shape: {newName: oldName} (all string)
# oldName format: look into the raw ROOT tree for the variable names
# if oldName refers to a multivariable branch, each element must be inserted individually
# mandatory, but can be left empty --> no variable mapping
treeMap = {}

for i in range(4): treeMap.update({"xRaw%d" % i: "xpos%d" % i})
for i in range(4): treeMap.update({"nStripHit%d" % i: "nstrip%d" % i})

icrilin=0
for i in range(64):
    if (i==57):
        treeMap.update({"digiBaseCaloFwd": "digiBase%d"%i})
    elif (i==53):
        treeMap.update({"digiBaseTiming0": "digiBase%d"%i})
    elif (i==54):
        treeMap.update({"digiBaseTiming1": "digiBase%d"%i})
    elif (((i>=0) & (i<32)) | (i>=49) & (i<53)):
        treeMap.update({"digiBaseCrilin%d"%icrilin: "digiBase%d"%i})
        icrilin+=1
    else:
        treeMap.update({"digiBase%d"%i: "digiBase%d"%i})

icrilin=0
for i in range(64):
    if (i==57):
        treeMap.update({"digiTimeCaloFwd": "digiTime%d"%i})
    elif (i==53):
        treeMap.update({"digiTimeTiming0": "digiTime%d"%i})
    elif (i==54):
        treeMap.update({"digiTimeTiming1": "digiTime%d"%i})
    elif (((i>=0) & (i<32)) | (i>=49) & (i<53)):
        treeMap.update({"digiTimeCrilin%d"%icrilin: "digiTime%d"%i})
        icrilin+=1
    else:
        treeMap.update({"digiTime%d"%i: "digiTime%d"%i})

icrilin=0
for i in range(64):
    if (i==57):
        treeMap.update({"digiHalfTimeCaloFwd": "digiHalfTime%d"%i})
    elif (i==53):
        treeMap.update({"digiHalfTimeTiming0": "digiHalfTime%d"%i})
    elif (i==54):
        treeMap.update({"digiHalfTimeTiming1": "digiHalfTime%d"%i})
    elif (((i>=0) & (i<32)) | (i>=49) & (i<53)):
        treeMap.update({"digiHalfTimeCrilin%d"%icrilin: "digiHalfTime%d"%i})
        icrilin+=1
    else:
        treeMap.update({"digiHalfTime%d"%i: "digiHalfTime%d"%i})

icrilin=0
for i in range(64):
    if (i==57):
        treeMap.update({"digiPHRawCaloFwd": "digiPH%d"%i})
    elif (i==53):
        treeMap.update({"digiPHRawTiming0": "digiPH%d"%i})
    elif (i==54):
        treeMap.update({"digiPHRawTiming1": "digiPH%d"%i})
    elif (((i>=0) & (i<32)) | (i>=49) & (i<53)):
        treeMap.update({"digiPHRawCrilin%d"%icrilin: "digiPH%d"%i})
        icrilin+=1
    else:
        treeMap.update({"digiPHRaw%d"%i: "digiPH%d"%i})

treeMap.update({"xGonioRawRot" : "xinfo0"})
treeMap.update({"xGonioRawCrad" : "xinfo1"})
treeMap.update({"xGonioRawHorsa" : "xinfo2"})
treeMap.update({"xGonioRawHorsaBig" : "xinfo3"})
    
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
        "2": 620.5,
        "3": 620.5,
        "gonio": 620.5+90.5+4.0,
        "caloFwd": 620.5+90.5+4.0+4.0+5.0,
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
    thInCentres.update({iRun: [-1.288368e-03, 2.577419e-03]})
    
# raw output angle distribution centres for modules alignment
# has to be set run by run
# dictionary -- shape: {run (string): [thX, thY] (2 float or None)}
# if None, the raw distributions are centered via their distrbution modes
# set 0 not to apply any shift
# mandatory for all the runs
thOutCentres = {}
for iRun in nRun0:
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
    if "Axial" in nRun0[iRun]:
        thInCut.update({iRun: [0.5e-3]})
    elif "AxisToRandom" in nRun0[iRun]:
        thInCut.update({iRun: [1.0e-3]})
    else:
        thInCut.update({iRun: [2.0e-3]})

# crystal fiducial rectangle applied at the crystal longitudinal position z -- boundaries excluded
# has to be set run by run
# dictionary -- shape: {run (string): [xCut0, xCut1, yCut0, yCut1] (4 float)}
# mandatory, but can be skipped for some/all runs --> no cut defined, i.e. boolean always True, in missing runs
xCryCut = {}
for iRun in nRun0:
    if ("Crilin" in nRun0[iRun]):
        if (int(iRun)<=800093):
            xCryCut.update({iRun: [4.65, 5.45, 1.85, 2.65]})
        elif (int(iRun)<=800119):
            xCryCut.update({iRun: [4.65, 5.45, 2.85, 3.65]})
        else:
            xCryCut.update({iRun: [5.15, 5.95, 2.85, 3.65]})
    elif ("Ciofex" in nRun0[iRun]):
        if (int(iRun)<=800191):
            xCryCut.update({iRun: [5.05, 5.85, 2.29, 3.09]})
        else:
            xCryCut.update({iRun: [4.05, 4.85, 2.29, 3.09]})
    else:
        xCryCut.update({iRun: [-10, 10, -10, 10]})

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
gonioMap = {}
gonioMap = { 
    "Rot": ["thIn1", False, -10**6],
    "Crad": ["thIn0", False, -10**6],
    "Horsa": ["xCry1", True, -10],
    "HorsaBig": ["xCry1", True, -2*10],
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
    digiPHCut.update({iRun : {}})
    digiPHCut[iRun].update({iRun: {"CaloFwd" : [0, 5000]}})
    digiPHCut[iRun].update({"CaloFwd" : [0, 5000]})
    digiPHCut[iRun].update({"Cher0" : [13, 5000]})
    for icrilin in range(36):
        digiPHCut[iRun].update({"Crilin%d"%icrilin : [0, 5000]})

# time cut interval -- inner events kept, boundaries excluded
# has to be set run by run
# dictionary - shape: {run (string): {var (string), [inf, sup] (2 floats)}}
# var format: insert the part of the variable name following "digiPHRaw"
# mandatory, but can be skipped for some/all runs or for some/all channels within a single run
#     --> no cuts defined, i.e. booleans always True, in missing runs/channels
digiTimeCut = {}
for iRun in nRun0:
    digiTimeCut.update({iRun : {}})
    if (int(iRun)<=800123):
        digiTimeCut[iRun].update({"CaloFwd" : [525, 550]})
        digiTimeCut[iRun].update({"Cher0" : [575, 600]})
    else:
        digiTimeCut[iRun].update({"CaloFwd" : [525, 550]})
        digiTimeCut[iRun].update({"Cher0" : [575, 600]})
    for icrilin in range(36):
        digiTimeCut[iRun].update({"Crilin%d"%icrilin : [0, 1000]})

# set of channels that are forward calorimeter channels
# has to be set run by run
# dictionary -- shape: {run: [var0, var1, ...]} (all string)
# varX format: insert the part of the variable name following "digiPHRaw"
# mandatory, but can be skipped for some/all runs --> forward calo. total PH and energy are set to NaN for those runs
lsDigiChCaloFwd = {}
for iRun in nRun0: lsDigiChCaloFwd.update({iRun: ["CaloFwd"]})

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
for iRun in nRun0:
    calibMapFwd.update({iRun: [lambda x, a: x, [1], 'end']})