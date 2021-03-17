#!/bin/bash

# note: conda has to be installed and deactivated
# note: run this with "bash -i createEnvComplete.sh" i.e. in interactive mode
# note: for different configurations, see the anaKrys documentation

ENVNAME=anaKrys

# 1st of all, update conda & add conda-forge repo
conda update -y conda
conda config --add channels conda-forge

# install all the necessary dependencies
echo "environment installation..."
conda env create --name $ENVNAME --file environment.yml

# activate the newly created environment (ENVNAME)
conda activate $ENVNAME

# interactive mode -- Jupyter Notebook & JupyterLab
echo "extensions for interactive mode..."
conda install -y "ipympl=0.5.8"
conda install -y "nodejs>=10.0"
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter labextension install jupyter-matplotlib@0.7.4
jupyter nbextension enable --py widgetsnbextension

# Git extension
echo "extensions for Git..."
conda install -y "git>2.0"
conda install -y jupyterlab-git
jupyter labextension install @jupyterlab/git

# in the end, deactivate environment
conda deactivate
echo "to activate the environment: conda activate $ENVNAME"


