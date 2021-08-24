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
    "500847" : "PbF2_AxisToRandom_650urad",
    
    "500865" : "PWO1X0_AxisSearch0",
    "500866" : "PWO1X0_AxisSearch1",
    "500867" : "PWO1X0_ScanCrad0",
    "500869" : "PWO1X0_ScanCrad0",
    "500870" : "PWO1X0_ScanCrad0",
    "500871" : "PWO1X0_ScanCrad0",
    "500872" : "PWO1X0_ScanRot0",
    "500873" : "PWO1X0_ScanRot0",
    "500874" : "PWO1X0_ScanRot0",
    "500875" : "PWO1X0_ScanRot0",
    "500876" : "PWO1X0_ScanRot0",
    "500877" : "PWO1X0_ScanRot0",
    "500878" : "PWO1X0_ScanCrad1",
    "500881" : "PWO1X0_ScanCrad1",
    "500882" : "PWO1X0_ScanCrad1",
    "500883" : "PWO1X0_ScanCrad1",
    "500884" : "PWO1X0_ScanCrad1",
    "500885" : "PWO1X0_ScanCrad1",
    "500886" : "PWO1X0_ScanCrad1",
    "500887" : "PWO1X0_ScanCrad2",
    "500888" : "PWO1X0_ScanCrad3",
    
    "500841" : "Bkg_MagnetOff",
    "500842" : "Bkg_MagnetOn",
    
    "500843_0" : "PbF2_AxisToRandom_4100urad",  # don't touch this, needed for execution flow
    "500843_1" : "PbF2_AxisToRandom_5200urad",  # don't touch this, needed for execution flow
    "500843_2" : "PbF2_AxisToRandom_8300urad",  # don't touch this, needed for execution flow
}