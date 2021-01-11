#!/bin/bash

# note: conda has to be installed and deactivated
# note: run this with "bash -i createEnvNoExtensions.sh" i.e. in interactive mode
# note: for different configurations, see the anaKrys documentation

ENVNAME=anaKrys_noExtensions

# 1st of all, update conda
conda update -y conda

# install all the necessary dependencies
echo "environment installation..."
conda env create --name $ENVNAME --file environment.yml

# activate the newly created environment (ENVNAME)
conda activate $ENVNAME

# interactive mode -- Jupyter Notebook only
echo "extensions for interactive mode..."
conda install -y "ipympl=0.5.8"

# in the end, deactivate environment
conda deactivate
echo "to activate the environment: conda activate $ENVNAME"


