# full run list
# shape: {number: type} (all string)
# select the run numbers or types to be opened with nRunToOpen...
nRun0 = {
    
    # setup
    "800088" : "set_tracking",
    "800101" : "set_Fiorello",
    "800102" : "set_Fiorello",
    "800103" : "set_Fiorello",
    "800135" : "set_CrilinSaturation",

    # CRILIN axis search
    "800093" : "OLD_Crilin_Random",
    "800094" : "OLD_Crilin_Random",
    "800095" : "OLD_Crilin_find_axis_misc",
    "800096" : "OLD_Crilin_Random2",
    "800097" : "OLD_Crilin_Random",

    # CRILIN axis search 2
    "800119" : "Crilin_find_axis_0",  # random
    "800120" : "Crilin_find_axis_0",  # random
    "800121" : "Crilin_find_axis_0",  # best guess
    "800122" : "Crilin_find_axis_0",  # cradle scan
    "800124" : "Crilin_find_axis_0",  # continuing cradle scan (single DAQ)
    "800125" : "Crilin_find_axis_0",  # continuing cradle scan (single DAQ)
    "800126" : "Crilin_find_axis_1",  # junction between cradle and rot scan (single DAQ)
    "800127" : "Crilin_find_axis_1",  # rot scan (single DAQ)
    "800128" : "Crilin_find_axis_1",  # rot scan (single DAQ)
    "800129" : "Crilin_find_axis_1",  # rot scan (single DAQ)
    "800130" : "Crilin_find_axis_2",  # rot scan (single DAQ)
    "800131" : "Crilin_find_axis_2",  # junction between rot scan and final cradle scan (single DAQ)
    "800132" : "Crilin_find_axis_2",  # cradle scan (single DAQ)
    
    # CRILIN high statistics
    "800134" : "OLD0_Crilin_Axial",  # Fiorello badly set, poor timing
    "800143" : "OLD1_Crilin_Axial",  # CRILIN HV not perfectly set
    "800152" : "Crilin_Axial",
    "800153" : "Crilin_Axial",
    "800154" : "Crilin_Axial",
    "800168" : "Crilin_Random",

    # Ciofecometro2 axis search
    "800178" : "OLD_Ciofex_find_axis_0",
    "800179" : "OLD_Ciofex_find_axis_0",
    "800180" : "OLD_Ciofex_find_axis_0",  # tentative random, but not too far from best guess
    "800181" : "Ciofex_find_axis_2",  # best guess, also use in rot scan
    "800182" : "Ciofex_find_axis_0",  # cradle scan
    "800183" : "Ciofex_find_axis_1",  # random
    "800184" : "Ciofex_find_axis_2",  # rot scan (single DAQ)
    "800185" : "Ciofex_find_axis_2",  # rot scan (single DAQ)
    "800186" : "Ciofex_find_axis_2",  # rot scan (single DAQ)
    "800187" : "Ciofex_find_axis_0",  # cradle scan
    "800188" : "Ciofex_find_axis_0",  # cradle scan
    "800189" : "Ciofex_find_axis_0",  # cradle scan

    # Ciofecometro2 high statistics
    "800192" : "OLD_Ciofex_Axial",  # could tweak alignment a little better
    "800193" : "Ciofex_Axial",
}