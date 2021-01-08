# note: conda has to be installed and deactivated

# 1st of all, update conda
conda update conda

# install all the necessary dependencies
conda env create -f environment.yml

# activate the newly created environment (anaKrys)
conda activate anaKrys

# interactive mode in Jupyternotebook only
conda install -y ipympl

# interactive mode in JupyterLab also
conda install -y "nodejs>=10.0"
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter labextension install jupyter-matplotlib
jupyter nbextension enable --py widgetsnbextension

# Git extension
conda install -y jupyterlab-git
jupyter labextension install @jupyterlab/git

# in the end, deactivate environment
conda deactivate

# for different configurations, see the anaKrys documentation


