# full run list
# shape: {number: type} (all string)
# select the run numbers or types to be opened with nRunToOpen...
nRun0 = {
    
    # W [100] "square"
    "405286": "WSquare_Random",  # used for divergence characterisation before collimator tweaking -- the 2 WSquare_Random runs might differ
    "405365": "WSquare_Random",  # used for WSquare shape identification -- after collimator tweaking -- the 2 WSquare_Random runs might differ
    "405287": "WSquare_Axial",
    "405363": "WSquare_Axial",
    "405368": "WSquare_Axial",
    
    "405409": "WSquare_Random_Presh0.20X0",
    "405408": "WSquare_Axial_Presh0.20X0",
    
    "405434": "WSquare_AxisToRandom_D0",  # run type name hardcoded in xCryCut (in y19EliotDesyT21.py file), careful
    "405433": "WSquare_AxisToRandom_D1",  # run type name hardcoded in xCryCut (in y19EliotDesyT21.py file), careful
    "405432": "WSquare_AxisToRandom_D2",  # run type name hardcoded in xCryCut (in y19EliotDesyT21.py file), careful
    "405431": "WSquare_AxisToRandom_D3",  # run type name hardcoded in xCryCut (in y19EliotDesyT21.py file), careful
    "405430": "WSquare_AxisToRandom_D4",  # run type name hardcoded in xCryCut (in y19EliotDesyT21.py file), careful
    "405429": "WSquare_AxisToRandom_D5",  # run type name hardcoded in xCryCut (in y19EliotDesyT21.py file), careful
    
    "405195": "WSquare_ScanHorsa0_Old",  # "Old" addresses old trigger and/or position (changed due to magnet accident) configuration
    "405198": "WSquare_ScanHorsa1_Old",
    "405199": "WSquare_ScanVersa0_Old",
    "405200": "WSquare_ScanVersa0_Old",
    "405201": "WSquare_ScanVersa1_Old",
    "405202": "WSquare_ScanHorsa2_Old",
    "405203": "WSquare_ScanVersa2_Old",
    "405204": "WSquare_ScanCradle_Old",
    "405205": "WSquare_ScanCradle_Old",
    "405221": "WSquare_ScanAngle_Old",
    "405222": "WSquare_ScanAngle_Old",
    "405263": "WSquare_AxisSearch_Realignment_Old",
    "405279": "WSquare_Random_Realignment_Old",
    "405280": "WSquare_AxisSearch_Realignment_Old",
    "405281": "WSquare_Random_Old",

    # PWO [100] "thick"
    "405323": "PWOThick_Random",
    "405327": "PWOThick_Random",
    "405335": "PWOThick_Random",
    "405326": "PWOThick_Axial",
    "405336": "PWOThick_Random0",
    "405338": "PWOThick_Random0",
    
    "405379": "PWOThick_Random_Presh0.20X0",
    "405376": "PWOThick_Random_Presh0.20X0",
    "405377": "PWOThick_Random_Presh0.20X0",
    "405378": "PWOThick_Axial_Presh0.20X0",
    "405380": "PWOThick_Axial_Presh0.20X0",
    
    "405400": "PWOThick_AxisToRandom_D0",
    "405401": "PWOThick_AxisToRandom_D1",
    "405403": "PWOThick_AxisToRandom_D6",
    "405404": "PWOThick_AxisToRandom_D4",
    "405405": "PWOThick_AxisToRandom_D3",
    "405406": "PWOThick_AxisToRandom_D2",
    "405407": "PWOThick_AxisToRandom_D5",
    
    "405324": "PWOThick_AxisSearch",
    "405325": "PWOThick_AxisSearch",
    
    "405362": "PWOThick_45deg_ScanCradle",  # different axis -- @ 45°
    "405371": "PWOThick_45deg_ScanCradle",  # different axis -- @ 45°
    "405372": "PWOThick_45deg_ScanCradle",  # different axis -- @ 45°
    "405373": "PWOThick_45deg_ScanCradle",  # different axis -- @ 45°

    # PWO [100] "strip"
    "405428": "PWOStrip_Random",  # used for divergence characterisation after collimator tweaking & for PWOStrip shape identification
    "405427": "PWOStrip_Axial",
    "405436": "PWOStrip_Axial",
    
    "405414": "PWOStrip_Random_Presh040X0",
    
    "405437": "PWOStrip_AxisToRandom_D0",
    "405438": "PWOStrip_AxisToRandom_D3",
    "405439": "PWOStrip_AxisToRandom_D2",
    "405440": "PWOStrip_AxisToRandom_D1",

    "405413": "PWOStrip_AxisSearch_Presh0.40X0",
    "405415": "PWOStrip_AxisSearch_Presh0.40X0",
    "405416": "PWOStrip_AxisSearch_Presh0.40X0",
    "405417": "PWOStrip_AxisSearch_Presh0.40X0",
    "405418": "PWOStrip_AxisSearch_Presh0.40X0",
    "405419": "PWOStrip_AxisSearch_Presh0.40X0",
    "405420": "PWOStrip_AxisSearch_Presh0.40X0",
    "405422": "PWOStrip_AxisSearch_Presh0.40X0",
    "405423": "PWOStrip_AxisSearch_Presh0.40X0",
    "405424": "PWOStrip_AxisSearch_Presh0.40X0",
    "405425": "PWOStrip_AxisSearch_Presh0.40X0",
    
    # calorimeter calibration
    "405391": "CaloCalib_2.0GeV",
    "405390": "CaloCalib_4.0GeV",
    "405383": "CaloCalib_4.4GeV",
    "405384": "CaloCalib_5.2GeV",
    "405385": "CaloCalib_5.6GeV",
    
    # other runs
    "405296": "Plastic_MagnetOn",
    "405297": "Direct_MagnetOn",
    
}