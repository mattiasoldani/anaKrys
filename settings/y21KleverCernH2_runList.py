# full run list
# shape: {number: type} (all string)
# select the run numbers or types to be opened with nRunToOpen...
nRun0 = {
    "500813" : "PbF2_AxisSearch0",  # used for input tracker alignment (coarse)
    "500814" : "PbF2_AxisSearch1",
    "500815" : "PbF2_AxisSearch2",
    "500816" : "PbF2_AxisSearch3",
    "500817" : "PbF2_AxisSearch4",  # used for input tracker alignment (finer)
    "500819" : "PbF2_AxisSearch5",
    "500820" : "PbF2_ScanRot0",
    "500821" : "PbF2_ScanRot0",
    "500822" : "PbF2_ScanRot0",
    "500823" : "PbF2_ScanRot0",
    "500824" : "PbF2_ScanCrad0",
    "500825" : "PbF2_ScanCrad0",
    "500826" : "PbF2_AxisSearch6",
    "500827" : "PbF2_ScanRot1",
    "500829" : "PbF2_ScanCrad1",
    "500830" : "PbF2_ScanCrad1",
    "500832" : "PbF2_Axial",
    "500833" : "PbF2_Axial",
    "500834" : "PbF2_Random",
    "500836" : "PbF2_AxisToRandom_1250urad",
    "500837" : "PbF2_Axial",
    "500843" : "PbF2_AxisToRandom_mixed",  # 0th/1st/2nd scan step at 4100urad/5200urad/8300urad --> typeRun changed accordingly, iRun changed to 500843_0/1/2
    "500846" : "PbF2_AxisToRandom_650urad",
    
    "500841" : "Bkg_MagnetOff",
    "500842" : "Bkg_MagnetOn",
    
    "500843_0" : "PbF2_AxisToRandom_4100urad",  # don't touch this, needed for execution flow
    "500843_1" : "PbF2_AxisToRandom_5200urad",  # don't touch this, needed for execution flow
    "500843_2" : "PbF2_AxisToRandom_8300urad",  # don't touch this, needed for execution flow
}