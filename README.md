# anaKrys

[![python](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/) [![anaconda](https://img.shields.io/badge/anaconda-3-blue.svg)](https://www.anaconda.com/)

This is **anaKrys**, a Python- and Jupyter-based data analysis software for the AXIAL/ELIOT team experimental studies on the electromagnetic interactions between high-energy particles and oriented crystalline lattices. In particular, it has been developed with a focus on the event-by-event analysis of the data collected during the fixed-target experiments performed at several high-energy particle beam facilities with the INSULAb detectors &mdash; further information on both the particle-crystal interaction physics and on the experimental setup features can be found, for example, [here](http://cds.cern.ch/record/1353904) and [here](http://annali.unife.it/iuss/article/view/1630).

Basic dependencies:

[![jupyterlab](https://img.shields.io/badge/jupyterlab-2-blue.svg)](https://jupyterlab.readthedocs.io/en/stable/) [![matplotlib](https://img.shields.io/badge/matplotlib-3.3.1-blue.svg)](https://matplotlib.org/) [![numpy](https://img.shields.io/badge/numpy-grey.svg)](https://numpy.org/) [![pandas](https://img.shields.io/badge/pandas-grey.svg)](https://pandas.pydata.org/) [![pip](https://img.shields.io/badge/pip-grey.svg)](https://pip.pypa.io/en/stable/) [![scipy](https://img.shields.io/badge/scipy-grey.svg)](https://www.scipy.org/)  [![succolib](https://img.shields.io/badge/succolib-grey.svg)](https://github.com/mattiasoldani/succolib) [![tqdm](https://img.shields.io/badge/tqdm-grey.svg)](https://github.com/tqdm/tqdm) [![uproot](https://img.shields.io/badge/uproot->=4-blue.svg)](https://github.com/scikit-hep/uproot) 

Note: all the basic dependencies, as well as the required installation channels, are listed in the Anaconda environment.yml file &mdash; see the section on environment setup for further details on this and on the optional JupyterLab extensions.

Found a bug? Or simply have any questions, comments or suggestions you'd like to talk about? Feel free to contact me at <mattiasoldani93@gmail.com>. And brace yourself, for the best is yet to come!

---

### Installation, environment setup and execution

#### **HOW TO DOWNLOAD ANAKRYS**

The anaKrys source code can be downloaded either as a ZIP archive, from the Code drop-down menu [here](https://github.com/mattiasoldani/anaKrys), or directly from the terminal (open in your project working directory) via
```shell
git clone git://github.com/mattiasoldani/anaKrys.git
```
Note: the latter requires  [Git](https://git-scm.com/) installed on your machine.

#### **HOW TO SET THE ([ANACONDA](https://www.anaconda.com/)) ENVIRONMENT UP**

The environment.yml file contains all the necessary information on the Anaconda environment setup, which can be automatically installed (with the only prerequisite that Anaconda itself is installed &mdash; check [here](https://docs.anaconda.com/anaconda/install/) for details) via
```shell
conda update conda
conda env create -f environment.yml
```
This will install the anaKrys environment, which then can be accessed via `conda activate anaKrys` (and closed via `conda deactivate`).

If you want to use anaKrys in JupyterLab (or Jupyter Notebook) without interactive mode, you need to set `%matplotlib inline` in the **notebook settings & imports** section and `bProgressBars = False` in the **input settings** section. Once these have been set, the software will work in the plain environment installed with the environment.yml file only. For more complex environment configurations, see the sections below &mdash; express installation scripts are also available, check below.

#### **HOW TO PERFORM A FULL ENVIRONMENT EXPRESS INSTALLATION**

The createEnvComplete.sh and createEnvNoExtensions.sh Bash scripts are provided in order to automatically perform the full environment installation, i.e. with all the useful extensions described below, and the installation of the anaKrys environment and of the interactive mode for Jupyter Notebook only respectively. Just run e.g. createEnvComplete.sh out of any Anaconda environment:
```shell
bash -i createEnvComplete.sh
```

Note: running the script via `./createEnvComplete.sh` won't work since the Bash interactive mode is needed.

#### **HOW TO MANUALLY ENABLE INTERACTIVE PLOTS & WIDGETS**

[![ipympl](https://img.shields.io/badge/ipympl-0.5.8-blue.svg)](https://github.com/matplotlib/ipympl) [![nodejs](https://img.shields.io/badge/nodejs->=10-blue.svg)](https://nodejs.org/)

In order to manually enable the interactive mode in JupyterLab, you need to run these steps in the anaKrys environment:
```shell
conda install "ipympl=0.5.8"
conda install "nodejs>=10.0"
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter labextension install jupyter-matplotlib@0.7.4
jupyter nbextension enable --py widgetsnbextension
```
(where the extensions versions have been chosen to match those of the rest of the environment &mdash; see the [ipympl documentation](https://github.com/matplotlib/ipympl)) and then decorate with `%matplotlib widget` (whereas `bProgressBar` can be set either to True or False). Moreover, in order to run the interactive mode in Jupyter Notebook rather than in JupyterLab, it is sufficient to run `conda install "ipympl=0.5.8"` in the fresh anaKrys environment.

#### **HOW TO MANUALLY ENABLE THE JUPYTERLAB GIT EXTENSION**

[![git](https://img.shields.io/badge/git->2-blue.svg)](https://git-scm.com/) [![jupyterlab-git](https://img.shields.io/badge/jupyterlab/git-grey.svg)](https://github.com/jupyterlab/jupyterlab-git)

In order to be able to execute Git actions, e.g. switching branches, from a drop-down menu within JupyterLab, the jupyterlab-git extension can be manually installed and enabled via
```shell
conda install "git>2.0"
conda install jupyterlab-git
jupyter labextension install @jupyterlab/git
```

#### **HOW TO RUN ANAKRYS IN JUPYTERLAB (OR JUPYTER NOTEBOOK)**

Once the environment is set up properly, it can be activated via  `conda activate anaKrys`. Running  `jupyter-lab` (or `jupyter-notebook`) there will open the JupyterLab (or Jupyter Notebook) server which can then be accessed via web browser.

#### **HOW TO RUN ANAKRYS AS A PYTHON SCRIPT**

First of all, an executable PY script has to be created starting from the IPYNB notebook. This can be done, after commenting all the magic lines (e.g. `%matplotlib ...`) out, either in the JupyterLab drop-down File menu or in the terminal, via
```shell
jupyter nbconvert --to script anaKrys.ipynb
```
Both these operations will result in the creation of the anaKrys.py file. Obviously, it is convenient to set everything properly inside the notebook before the conversion.

The anaKrys.py script has to be run in the same path as anaKrys.ipynb because it exploits the same modules and folders for I/O. It can be run within the python interpreter (e.g. `python` in the anaKrys environment) via
```python
exec(open("anaKrys.py").read())
```

Plots are not drawn in any graphic window but output is saved the same way as when executing from JupyterLab/Jupyter Notebook &mdash; see dedicated section.

---

### Settings, I/O and analysis flow

#### **INPUT DATA AND SETTINGS**

anaKrys data input stage (**opening the data files** section) exploits the [succolib](https://github.com/mattiasoldani/succolib) input tools; it supports sets of formatted text files (e.g. DAT files) and of [ROOT](https://root.cern.ch/) [tree](https://root.cern.ch/doc/master/classTTree.html) files. Multiple filesets can be opened at a time, a fileset being a set of files coming from the same data taking run. In turn, each fileset can consist of multiple files. All the filenames must share the same format, differing only in one (optionally two) part(s): the part which unambiguously identifies the fileset, i.e. the run ID and, in case of multiple files per fileset, the part that differentiates the names of the single files, usually a file ID. For example, the file list
```shell
run000000_spill00001.dat
run000000_spill00009.dat
run000000_spill00099.dat
run0001_spillFirst.dat
run0001_spillSecond.dat
runABC_spillIJK.dat
```
consists of 3 different filesets, whose IDs are "000000", "0001" and "ABC", which in turn comprise 3, 2 and 1 files respectively; all these name formats are valid. Obviously, the file structure should also be common to all the files. The file name structure, path and type, as well as other input settings, are set within the anaKrys.ipynb notebook, in the **input settings** section.

Tipically, data from different data taking sessions have to be dealt with separately. For each experiment two settings files must be created in ./settings with name formats
- [EXPERIMENT_NAME]_runList.py, and
- [EXPERIMENT_NAME]_settings.py

respectively. The variable `settingsFileMods` in the **input settings** section must be assigned the string `[EXPERIMENT_NAME]` for the settings to load properly. Tipycally, [EXPERIMENT_NAME] directly refers to the year, team and place of a specific data taking session, e.g. "y19EliotDesyT21". Template files are available with the name "y21EmptyTemplate", as well as examples from the test mode, in ./settings/test.

[EXPERIMENT_NAME]_runList.py contains the `nRun0` dictionary which has the run IDs as keys and human-readable run names as values. Multiple run IDs can be associated with the same run name &mdash; this allows to merge multiple runs acquired in the same experimental conditions. Only the filesets referenced there can be opened; the latter is done by referencing either the run IDs or the run names of interest in the `nRunToOpen` in the **input settings** section.

[EXPERIMENT_NAME]_settings.py contains all the information needed for the data conditioning and analysis &mdash; data structure, experiment geometry, tuning of the detectors raw data, standard data selections. In particular, it is worth mentioning the `descFrac` setting, which allows to load only a fraction of the overall data, and the `filterMap` setting, which allows for a preliminary noise rejection. Further details on how to set everything up are given in the comments inside the template file.

#### **THE DATAFRAME**

All the input data are stored into the `df` [pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/frame.html). In order to fully exploit the anaKrys features, the variable names should be compliant to some rules &mdash; check the `asciiMap` and `treeMap` settings.

|   **name in `df`** |  **type**  | **description**                                                                                                                     |
|-------------------:|:----------:|-------------------------------------------------------------------------------------------------------------------------------------|
|             `iRun` |   string   | Run ID &mdash; if absent among the raw data, it is created starting from the filename                                               |
|          `typeRun` |   string   | Run name (from `nRun0`)                                                                                                             |
|            `iStep` |   number   | Goniometer scan step number                                                                                                         |
|            `epoch` |   number   | Event timestamp                                                                                                                     |
|     `xGonioRaw...` |  number(s) | Goniometer DOF &mdash; raw                                                                                                          |
|        `xGonio...` |  number(s) | Goniometer DOF &mdash; paired with tracking variables and aligned, check `gonioMap` setting                                         |
|          `nHit...` |  number(s) | Tracking multiplicities, i.e. nr. of particles per tracking layer                                                                   |
|           `nHitIn` |   number   | Average input multiplicity &mdash; obtained from the 4 input tracking layers, check `baseTrackingMap` setting                       |
|          `nHitOut` |   number   | Average output multiplicity &mdash; obtained from the 2 output tracking layers, check `baseTrackingMap` setting                     |
|          `xRaw...` |  number(s) | Tracking 1st hits &mdash; raw, but already mirrored, check `mirrorMap` setting                                                      |
|       `thInRaw0/1` |   numbers  | Input angles (0 & 1) &mdash; raw, obtained from the 4 input tracking layers, check `baseTrackingMap` setting                        |
|          `thIn0/1` |   numbers  | Input angles (0 & 1) &mdash; centered to zero                                                                                       |
|             `x...` |  number(s) | Tracking 1st hits &mdash; aligned via `thInRaw0/1`                                                                                  |
|          `xCry0/1` |   numbers  | Input (aligned) positions projected to the goniometer _z_ (0 & 1)                                                                   |
|      `thOutRaw0/1` |   numbers  | Output angles (0 & 1) &mdash; raw, obtained from `xCry0/1` and the 2 output tracking layers, check `baseTrackingMap` setting        |
|         `thOut0/1` |   numbers  | Output angles (0 & 1) &mdash; centered to zero                                                                                      |
|       `thDelta0/1` |   numbers  | Deflection (i.e. output-minus-input aligned) angles (0 & 1)                                                                         |
|      `xCaloFwd0/1` |   numbers  | Input (aligned) positions projected to the forward calorimeter _z_ (0 & 1)                                                          |
|     `digiPHRaw...` |  number(s) | Digitizer pulse heights &mdash; raw                                                                                                 |
|        `digiPH...` |  number(s) | Digitizer pulse heights &mdash; equalised, check `equalMap` setting                                                                 |
|      `digiTime...` |  number(s) | Digitizer peaking times                                                                                                             |
|      `digiBase...` |  number(s) | Digitizer baselines                                                                                                                 |
|        `PHCaloFwd` |   number   | Forward calorimeter total pulse height &mdash; check `lsDigiChCaloFwd` setting                                                      |
|             `EFwd` |   number   | Forward calorimeter total calibrated energy &mdash; check  `calibMapFwd` setting                                                    |
|  `boolSingleHitIn` |   boolean  | True if the 4 input multiplicities are equal to 1; check `baseTrackingMap` setting                                                  |
| `boolSingleHitOut` |   boolean  | True if the 2 output multiplicities are equal to 1; check `baseTrackingMap` setting                                                 |
|    `boolInAligned` |   boolean  | True if the input particle is aligned with the _z_ axis &mdash; check  `thInCut` setting                                            |
|   `boolLowOutMult` |   boolean  | True if the overall output multiplicity is low &mdash; check `outMultCut` setting                                                   |
|  `boolHighOutMult` |   boolean  | True if the overall output multiplicity is high &mdash; check `outMultCut` setting                                                  |
|     `boolInCry0/1` |  booleans  | True if the input trajectory falls within the fiducial box at the goniometer _z_ &mdash; check  `xCryCut` setting, 0 & 1 separately |
|        `boolInCry` |   boolean  | True if the input trajectory falls within the fiducial box at the goniometer _z_ &mdash; check  `xCryCut` setting, 0 & 1 together   |
|    `boolDigiPH...` | boolean(s) | True if the digitizer pulse heights are within the selected range &mdash; check `digiPHCut` setting                                 |
|  `boolDigiTime...` | boolean(s) | True if the digitizer peaking times are within the selected range &mdash; check `digiTimeCut` setting                               |

All these variables either come directly from the raw data or are computed in the **physics analysis** section. Their availability and therefore the parts of the analysis that are actually executed depend on the input data structure. The single `df` variables are [pandas Series](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html) objects and can be accessed via e.g. `df.iRun` or `df["iRun"]`. New variables can be added to `df` anytime, e.g. in the **whiteboard** &mdash; see dedicated section.

#### **PLOTS**

All the plots, together with the related statistical analysis, are obtained in the **plots & output** section. General settings on these operations can be found in the **plot & output settings** subsection right at the beginning of the latter, whereas each plot or set of common plots can be tuned via some specific settings on the top of its own cell.

Of course, there is room to implement custom calculations and plots that might be required in case of more complex analyses: the **whiteboard** section, empty by default, provides a clean workspace for custom pieces of code.

#### **OUTPUT**

Whatever the execution mode, if `bPlotSave = True`, all the default plots are saved as PNG images in ./out_plots. Recall that custom plots, e.g. from the **whiteboard**, have to be saved manually via `plt.savefig(...)` &mdash; `plt` referring to `matplotlib.pyplot`.

Moreover, the `outData` dictionary is created in the **plots & output** section and filled with many useful information from the physics analysis &mdash; e.g. bin-by-bin points for important histograms, fit results and statistical parameters. The content of the dictionary may vary depending on the input data available and on the plots actually drawn. Further useful data can be added in the **whiteboard**.

The outData.pickle [pickle](https://docs.python.org/3/library/pickle.html#module-pickle) file with the `outData` dictionary is always saved in ./out_data at the end of the execution of the default part of the program (i.e. above the **whiteboard** section) and then again at the end of the whole program execution. You can open it via
```python
import pickle

inFile = open("[PATH_TO_IPYNB]/out_data/outData.pickle",'rb')
outData = pickle.load(inFile)
inFile.close()
```
