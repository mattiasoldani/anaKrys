#!/bin/bash

# note: conda has to be installed and deactivated
# note: run this with "bash -i createEnvNotebook.sh" i.e. in interactive mode
# note: for different configurations, see the anaKrys documentation

ENVNAME=anaKrys

# 1st of all, update conda
conda update -y conda

# install all the necessary dependencies
echo "environment installation..."
conda env create -f environment.yml  # check ENVNAME in here as well

# activate the newly created environment (ENVNAME)
conda activate $ENVNAME

# interactive mode in Jupyter Notebook only
echo "extensions for interactive mode..."
conda install -y ipympl

# in the end, deactivate environment
conda deactivate
echo "to activate the environment: conda activate $ENVNAME"


