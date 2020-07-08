# filetype, string -- either "ASCII" or "ROOT"
# mandatory, otherwise no proper working
fileType = "ASCII"

# file path, string
# mandatory, otherwise no proper working
filePath = "./ascii_local/"

# file name format (with no path), string
# shape: replace the run number with XXXXXX and (for multiple files per run) the file number with YYYYYY
# mandatory, otherwise no proper working
# fileNameFormat = "runXXXXXXtot.dat"  # 1-per-run-merged filesets
fileNameFormat = "runXXXXXX_YYYYYY.dat"