# anaKrys

[![python](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/) [![anaconda](https://img.shields.io/badge/anaconda-3-blue.svg)](https://www.anaconda.com/)

This is **anaKrys**, a Python- and Jupyter-based data analysis software for the AXIAL/ELIOT team experimental studies on the electromagnetic interactions between high-energy particles and oriented crystalline lattices. In particular, it has been developed with a focus on the event-by-event analysis of the data collected during the fixed-target experiments performed at several high-energy particle beam facilities with the INSULAb detectors &mdash; further information on both the particle-crystal interaction physics and on the experimental setup features can be found, for example, [here](http://cds.cern.ch/record/1353904) and [here](http://annali.unife.it/iuss/article/view/1630).

Basic dependencies:

[![jupyterlab](https://img.shields.io/badge/jupyterlab-2-blue.svg)](https://jupyterlab.readthedocs.io/en/stable/) [![matplotlib](https://img.shields.io/badge/matplotlib-3.3.1-blue.svg)](https://matplotlib.org/) [![numpy](https://img.shields.io/badge/numpy-grey.svg)](https://numpy.org/) [![pandas](https://img.shields.io/badge/pandas-grey.svg)](https://pandas.pydata.org/) [![pip](https://img.shields.io/badge/pip-grey.svg)](https://pip.pypa.io/en/stable/) [![scipy](https://img.shields.io/badge/scipy-grey.svg)](https://www.scipy.org/)  [![succolib](https://img.shields.io/badge/succolib-grey.svg)](https://github.com/mattiasoldani/succolib) [![tqdm](https://img.shields.io/badge/tqdm-grey.svg)](https://github.com/tqdm/tqdm) [![uproot](https://img.shields.io/badge/uproot-3-blue.svg)](https://github.com/scikit-hep/uproot) 

Note: all the basic dependencies, as well as the required installation channels, are listed in the Anaconda environment.yml file &mdash; see the section on environment setup for further details on this and on the optional JupyterLab extensions.

Found a bug? Or simply have any questions, comments or suggestions you'd like to talk about? Feel free to contact me at <mattiasoldani93@gmail.com>. And brace yourself, for the best is yet to come!

---

### Installation and environment setup

**HOW TO DOWNLOAD ANAKRYS**

**HOW TO SET THE (ANACONDA) ENVIRONMENT UP**

The environment.yml file contains all the necessary information on the Anaconda environment setup, which can be automatically installed (with the only prerequisite that Anaconda itself is installed) via
```
conda update conda
conda env create -f environment.yml
```
This will install the anaKrys environment, which then can be accessed via `conda activate anaKrys` (and closed via `conda deactivate`).

If you want to use anaKrys in JupyterLab (or Jupyter Notebook) without interactive mode, you need to set `%matplotlib inline` in the **notebook settings & imports** section and `bProgressBars = False` in the "settings" section. Once these have been set, the software will work in the plain environment installed with the environment.yml file only. For more complex environment configurations, see the sections below &mdash; express installation scripts are also available, check below.

**HOW TO ENABLE INTERACTIVE PLOTS & WIDGETS**

[![ipympl](https://img.shields.io/badge/ipympl-0.5.8-blue.svg)](https://github.com/matplotlib/ipympl) [![nodejs](https://img.shields.io/badge/nodejs->=10-blue.svg)](https://nodejs.org/)

_(sources: [here](https://stackoverflow.com/questions/50149562/jupyterlab-interactive-plot) and [here](https://towardsdatascience.com/how-to-produce-interactive-matplotlib-plots-in-jupyter-environment-1e4329d71651))_

On the other hand, in order to enable the interactive mode in JupyterLab, you need to run these steps in the anaKrys environment:
```
conda install "ipympl=0.5.8"
conda install "nodejs>=10.0"
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter labextension install jupyter-matplotlib@0.7.4
jupyter nbextension enable --py widgetsnbextension
```
(where the extensions versions have been chosen to match those of the rest of the environment &mdash; see the [ipympl documentation](https://github.com/matplotlib/ipympl)) and then decorate with `%matplotlib widget` (whereas `bProgressBar` can be set either to True or False). Moreover, in order to run the interactive mode in Jupyter Notebook rather than in JupyterLab, it is sufficient to run `conda install "ipympl=0.5.8"` in the fresh anaKrys environment.

**HOW TO ENABLE THE JUPYTERLAB GIT EXTENSION**

[![git](https://img.shields.io/badge/git->2-blue.svg)](https://git-scm.com/) [![jupyterlab-git](https://img.shields.io/badge/jupyterlab/git-grey.svg)](https://github.com/jupyterlab/jupyterlab-git)

_(source: [here](https://github.com/jupyterlab/jupyterlab-git))_

In order to be able to execute Git actions, e.g. switching branches, from a drop-down menu within JupyterLab, the jupyterlab-git extension has to be installed and enabled via
```
conda install "git>2.0"
conda install jupyterlab-git
jupyter labextension install @jupyterlab/git
```

**HOW TO PERFORM A FULL ENVIRONMENT EXPRESS INSTALLATION**

The createEnvComplete.sh and createEnvNoExtensions.sh Bash scripts are provided in order to automatically perform the full environment installation, i.e. with all the aforementioned extensions, and the installation of the anaKrys environment and of the interactive mode for Jupyter Notebook only respectively. Just run e.g. createEnvComplete.sh out of any Anaconda environment:
```
bash -i createEnvComplete.sh
```

Note: running the script via `./createEnvComplete.sh` won't work since the Bash interactive mode is needed.
