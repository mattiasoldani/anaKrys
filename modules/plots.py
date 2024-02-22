import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import succolib as sl
from scipy.optimize import curve_fit
from matplotlib.colors import LogNorm, Normalize

###############################################################################
###############################################################################

# functions for ranges drawing on already existing plots

def plot_selectionX(ax, axEdges, selEdges, lineC, lineW):
    for i in range(len(selEdges)):
        if axEdges[0] < selEdges[i] < axEdges[1]:
            ax.axvline(x = selEdges[i], color=lineC, linewidth=lineW)

def plot_selectionY(ax, axEdges, selEdges, lineC, lineW):
    for i in range(len(selEdges)):
        if axEdges[0] < selEdges[i] < axEdges[1]:
            ax.axhline(y = selEdges[i], color=lineC, linewidth=lineW)
            
def plot_selectionBox(ax, selEdges, lineC, lineW):
    patch = plt.Rectangle((selEdges[0], selEdges[2]), selEdges[1]-selEdges[0], selEdges[3]-selEdges[2], fill=False, lw=lineW, color=lineC)
    ax.add_patch(patch)

###############################################################################
###############################################################################

# iRun (or index in the sorted list of non-numeric iRun values) & xGonio... (all) vs time
def plot_runInfo(
    df,  # MANDATORY
    
    lsBool = [],  # list of boolean names (to be defined a priori as variables in df) to filter the data to plot
    bXGonio=False,  # if True, goniometer DOF trends are plotted -- set it true only if a xGonioRaw (and hence xGonio) variable actually exists in df 
    bEpoch=False,  # set it True only if the epoch variable actually exists in df
    bUseEpoch=False,  # if False, event index in the current execution (always available) is used -- only if epoch in df, otherwise index anyway
    pal2d = plt.rcParams["image.cmap"],
    units={},
    xSize=plt.rcParams["figure.figsize"][0],
    ySize=plt.rcParams["figure.figsize"][1],
    figName="temp",
    bSave=False,
):
    
    plt.close(figName)
    nRows = 1 + (len([s for s in df.columns if "xGonioRaw" in s]) if bXGonio else 0)
    fig, ax = plt.subplots(nrows=nRows, ncols=1, squeeze=False, figsize=[xSize, ySize], num=figName)
    
    # plot boolean & corresponding title
    # also x, which is common to all the plots
    title = ""
    dfBool = True
    if len(lsBool)>0:
        for iBool in [df[s] for s in lsBool]:
            dfBool = dfBool & iBool
        x = df[dfBool]["epoch"] if (bEpoch & bUseEpoch) else df[dfBool].index
        for i in range(len(lsBool)-1):
            title += lsBool[i] + " & "
        title += lsBool[len(lsBool)-1]
    else:
        x = df["epoch"] if (bEpoch & bUseEpoch) else df.index
    xUnit = units[x.name] if x.name in units else ""
    xFullName = x.name+xUnit if (bEpoch & bUseEpoch) else "index"

    ######
    # iRun
    try:  # if iRun comprises numbers only, the call to pd.to_numeric() is successful
        y = pd.to_numeric(df["iRun"] if len(lsBool)==0 else df[dfBool]["iRun"])
    except:  # if iRun is truly non numeric, the call to pd.to_numeric() fails --> the ordinate here is the index number in the sorted list of iRun unique values
        for i, iRun in enumerate(sorted(df["iRun"].unique())):
            df.loc[df["iRun"] == iRun, "iRunTemp"] = i
        y = df["iRunTemp"] if len(lsBool)==0 else df[dfBool]["iRunTemp"]
        del df["iRunTemp"]
    bins = [min(1000, x.max() - x.min()), min(100, max(10, 2*int(y.max() - y.min())))]
    ax[0, 0].hist2d(x, y, bins, cmap=pal2d)
    ax[0, 0].set_title("%s:%s" % (y.name, xFullName), fontsize="small")

    ######
    # all the goniometer DOF (if any available)
    if bXGonio:  # only done if any xGonioRaw (and hence xGonio) variable available
        for i, iDof in enumerate([s.replace("Raw", "") for s in df.columns if "xGonioRaw" in s]):
            y = df[iDof] if len(lsBool)==0 else df[dfBool][iDof]
            yFullName = y.name + (units[y.name] if y.name in units else "")
            bins = [min(1000, x.max() - x.min()), 100]
            ax[i+1, 0] = plt.subplot(nRows, 1, i+2)
            ax[i+1, 0].hist2d(x, y, bins, cmap=pal2d)
            ax[i+1, 0].set_title("%s:%s" % (yFullName, xFullName), fontsize="small")
        
    fig.suptitle(title, y=1, va="top", fontsize="small")
    fig.tight_layout()
    
    # save output figure
    if bSave:
        plt.savefig(fname="./out_plots/"+figName+".png", dpi=1000)
            
###############################################################################
###############################################################################

# x-y angle distribution histograms, with fits (optional) & range delimiters (optional)
# returns a dictionary -- see below...
def plot_th(
    df,  # MANDATORY
    var,  # MANDATORY -- full df name of the set of (x & y) angle distributions without the vista index 0/1 (e.g. "thIn")
    
    binSize = None,  # if None, 100 bins
    lsBool = [],  # list of boolean names (to be defined a priori as variables in df) to filter the data to plot
    xRange = [None, None],  # length 2 -- left-then-right, same for both x & y -- if value is None, corresponding boundary position is defined automatically
    bFit = False,  # fit & corresponding parameter output (on both vistas) is performed only if True
    fitSigma = None,  # starting point for gaussian sigma fit (set to ~ half the distribution FWHM) -- if None, automatically computed
    outData = {},  # dictionary that will be updated with the spectrum & fit parameters -- details below...
    bSel = False,  # cut edges are drawn only if True
    thSel = {},  # cut shape -- details below...
    bLog = False,  # if True (False), log (lin) scale on y
    fitC = plt.rcParams['axes.prop_cycle'].by_key()['color'][0],
    fitW = plt.rcParams['lines.linewidth'],
    lineC = plt.rcParams['axes.prop_cycle'].by_key()['color'][0],
    lineW = plt.rcParams['lines.linewidth'],
    units = {},
    xSize=plt.rcParams["figure.figsize"][0],
    ySize=plt.rcParams["figure.figsize"][1],
    figName="temp",
    bSave=False,
):
    
    plt.close(figName)
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=[xSize, ySize], num=figName)
    
    # plot boolean & corresponding title & variables to be plotted
    title = ""
    dfBool = True
    if len(lsBool)>0:
        for iBool in [df[s] for s in lsBool]:
            dfBool = dfBool & iBool
        xLs = [df[dfBool][var+"0"], df[dfBool][var+"1"]]
        for i in range(len(lsBool)-1):
            title += lsBool[i] + " & "
        title += lsBool[len(lsBool)-1]
    else:
        xLs = [df[var+"0"], df[var+"1"]]

    for i, x in enumerate(xLs):  # loop on vistas
        
        # histogram
        xRangeTot = []
        cat = pd.cut(x, bins=np.arange(x.min(), x.max(), 0.0001), labels=np.arange(x.min(), x.max()-0.0001, 0.0001))
        centre = cat.describe()[2]
        for j in range(2):
            # lower, then upper histogram range, always defined wrt. the distribution centre
            # xRange always overwritten with the values shifted wrt. the centre
            if xRange[j] is None:
                xRangeTot.append(centre + max([10*x0.std() for x0 in xLs])*(-1)**(j+1))
            else:
                xRangeTot.append(xRange[j] + centre)
        bins = int((xRangeTot[1] - xRangeTot[0]) / binSize) if binSize!=None else 100
        
        histo = ax[i].hist(x, bins, range=xRangeTot, histtype="step", log=bLog)
        xFullName = x.name + (units[x.name] if x.name in units else "")
        ax[i].set_xlabel(xFullName, fontsize="small")
        if min(histo[1]) < 0 < max(histo[1]):
            ax[i].axvline(x=0, color="k")
            
        xBars = np.array([x0 + (histo[1][1] - histo[1][0])/2 for x0 in histo[1][:-1]])
        yBars = histo[0]
        yErrs = np.array([max(1, np.sqrt(y0)) for y0 in yBars])
        outName = x.name + "_histo"
        outData[outName] = [xBars, yBars, yErrs]
        print("spectrum returned in a dictionary with key %s -- x, y, ey" % outName)
            
        # fit (only if requested)
        if bFit:
            if (len(x.unique()) > 1):
                print("performing gaussian fit on %s..." % x.name)
                xFit, yFit, eFit = xBars, yBars, yErrs
                eFit = np.array([eFit[ii] for ii in range(len(yFit)) if (yFit[ii]!=0)])  # only nonempty bins are fitted
                xFit = np.array([xFit[ii] for ii in range(len(yFit)) if (yFit[ii]!=0)])  # only nonempty bins are fitted
                yFit = np.array([yFit[ii] for ii in range(len(yFit)) if (yFit[ii]!=0)])  # only nonempty bins are fitted
                p0 = [float(yFit.max()), xFit[list(yFit).index(yFit.max())], min(x.std(), fitSigma) if fitSigma!=None else x.std()]
                try:  # gaussian fits occasionally fail for some reason...
                    p, cov = curve_fit(sl.fGaus, xFit, yFit, p0=p0, sigma=eFit)  # fit here
                    xFitPlot = np.linspace(min(xFit), max(xFit), 500)
                    ax[i].plot(xFitPlot, sl.fGaus(xFitPlot, *p), fitC, linewidth = fitW, label="mean = %.3e\nsigma = %.3e" % (p[1], p[2]))
                    ax[i].legend(fontsize="small")
                    print("fit parameters:")
                    print("\tampl.\t%e +- %e" % (p[0], [cov[i][i] for i in range(len(p))][0]))
                    print("\tmean\t%e +- %e" % (p[1], [cov[i][i] for i in range(len(p))][1]))
                    print("\tsigma\t%e +- %e" % (p[2], [cov[i][i] for i in range(len(p))][2]))
                    outData[x.name + "_fit"] = [p, cov]  # filling output dictionary
                    print("fit parameters are returned in a dictionary with key %s -- parameters, cov. matrix" % x.name + "_fit")
                    print("--")
                except:
                    print("fit failed\n--")
                    pass

            else:
                print("%s gaussian fit not performed (distribution has %d value(s))\n--" % (x.name, len(x.unique())))
        else:
            print("%s gaussian fit not performed (not requested)\n--" % x.name)

        # selection (only if requested -- run by run)
        # recall that thSel must be a dictionary with run names (range limits) as keys (values) --> if no runs are concerned, just use a single placeholder key (no need for a true run nr.)
        if bSel:
            for iRun in thSel:
                if len(thSel[iRun]) == 1:  # circular cut
                    plot_selectionX(ax[i], xRangeTot, [-thSel[iRun][0], thSel[iRun][0]], lineC, lineW)
                elif len(thSel[iRun]) == 2:  # elliptical cut
                    plot_selectionX(ax[i], xRangeTot, [-thSel[iRun][i], thSel[iRun][i]], lineC, lineW)
                elif len(thSel[iRun]) == 4:  # rectangular cut
                    plot_selectionX(ax[i], xRangeTot, [thSel[iRun][2*i], thSel[iRun][2*i+1]], lineC, lineW)

        # fix for visualisation issues in case of bLog = True & bFit = True
        if bLog:
            ax[i].set_ylim([min(yBars), 2*max(yBars)])

    fig.suptitle(title, y=1, va="top", fontsize="small")
    fig.tight_layout()
    
    # save output figure
    if bSave:
        plt.savefig(fname="./out_plots/"+figName+".png", dpi=1000)
    
    # careful with outData:
    #     if a dictionary is given as argument and bFit=True, both the spectra info lists with x, y & ey and the fit parameters (& cov. matrix) are added to the dictionary with the variable names as keys (plus "_histo" and "_fit" respectively) & the updated dictionary is returned
    #     if a dictionary is given as argument and bFit=False, only the spectra info lists are added to the dictionary with the keys described above & the updated dictionary is returned
    #     if no dictionary is given as argument and bFit=True, a new dictionary with both the spectra info list and the fit parameters (& cov. matrix) with the keys described above is returned
    #     if no dictionary is given as argument and bFit=False, a new dictionary with only the spectra info lists with the keys described above is returned
    return outData
    
###############################################################################
###############################################################################

# tracking layer multiplicity, 1d (in selectable range) & 2d (vs time) with range delimiters (optional)
def plot_nHit(
    df,  # MANDATORY
    var,  # MANDATORY -- full df name of the multiplicity value under study (e.g. "nHitIn")

    lsBool = [],  # list of boolean names (to be defined a priori as variables in df) to filter the data to plot
    bEpoch=False,  # set it True only if the epoch variable actually exists in df
    bUseEpoch=False,  # if False, event index in the current execution (always available) is used -- only if epoch in df, otherwise index anyway
    maxNHit=None,  # multiplicity upper limit in plots -- if None, range (& binning) automatically defined
    tRange=None,  # range on the 2d plots x to be used to costrain the data included in the 1d plots -- length-2 array or None (in this case no costraint is applied)
    bSel=False,  # cut edges are drawn only if True
    hitSel={},  # cut shape -- details below...
    outData={},  # dictionary that will be updated with the spectrum (1d & 2d) parameters -- details below...
    bLog=False,  # if True (False), log (lin) scale on y in 1d plots & z in 2d plots
    lineC = plt.rcParams['axes.prop_cycle'].by_key()['color'][0],
    lineW = plt.rcParams['lines.linewidth'],
    pal2d = plt.rcParams["image.cmap"],
    units={},
    xSize=plt.rcParams["figure.figsize"][0],
    ySize=plt.rcParams["figure.figsize"][1],
    figName="temp",
    bSave=False,
):
    
    plt.close(figName)
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=[xSize, ySize], num=figName)

    # plot boolean & corresponding title
    # also x for the 2d plots, which is common to all the latter
    title = ""
    dfBool = True
    if len(lsBool)>0:
        for iBool in [df[s] for s in lsBool]:
            dfBool = dfBool & iBool
        x = df[dfBool]["epoch"] if (bEpoch & bUseEpoch) else df[dfBool].index
        for i in range(len(lsBool)-1):
            title += lsBool[i] + " & "
        title += lsBool[len(lsBool)-1]
    else:
        x = df["epoch"] if (bEpoch & bUseEpoch) else df.index
    xName = x.name if (bEpoch & bUseEpoch) else "index"
    xUnit = units[x.name] if x.name in units else ""
    xFullName = xName+xUnit if (bEpoch & bUseEpoch) else xName
    
    if tRange is None:
        tRange = [df["epoch"].min(), df["epoch"].max()] if (bEpoch & bUseEpoch) else [df.index.min(), df.index.max()]
    if bEpoch & bUseEpoch:
        tRangeBool = (df["epoch"] > tRange[0]) & (df["epoch"] < tRange[1])
    else:
        tRangeBool = (df.index > tRange[0]) & (df.index < tRange[1])

    ######
    # iRun
    try:  # if iRun comprises numbers only, the call to pd.to_numeric() is successful
        y = pd.to_numeric(df["iRun"] if len(lsBool)==0 else df[dfBool]["iRun"])
    except:  # if iRun is truly non numeric, the call to pd.to_numeric() fails --> the ordinate here is the index number in the sorted list of iRun unique values
        for i, iRun in enumerate(sorted(df["iRun"].unique())):
            df.loc[df["iRun"] == iRun, "iRunTemp"] = i
        y = df["iRunTemp"] if len(lsBool)==0 else df[dfBool]["iRunTemp"]
        del df["iRunTemp"]
    bins = [min(1000, x.max() - x.min()), min(100, max(10, 2*int(y.max() - y.min())))]
    
    # 2d
    ax[0, 0].hist2d(x, y, bins, cmap=pal2d)
    ax[0, 0].set_xlabel(xFullName, fontsize="small")
    ax[0, 0].set_ylabel(y.name, fontsize="small")
    
    # 1d, run by run
    for iRun in (df[tRangeBool]["iRun"].unique() if len(lsBool)==0 else df[dfBool & tRangeBool]["iRun"].unique()):
        yTemp = y[(df["iRun"] == iRun) & tRangeBool] if len(lsBool)==0 else y[(df["iRun"] == iRun) & dfBool & tRangeBool]
        ax[0, 1].hist(yTemp, 1000, density=True, histtype="step", label="run %s" % iRun)
    ax[0, 1].set_xlabel(yTemp.name, fontsize="small")
    ax[0, 1].set_title("%s in (%d, %d)" % (xName, tRange[0], tRange[1]), fontsize="small")
    ax[0, 1].legend(fontsize="small")

    ######
    # multiplicity
    y = df[var] if len(lsBool)==0 else df[dfBool][var]
    yFullName = y.name + (units[y.name] if y.name in units else "")
    bins = [min(1000, x.max() - x.min()), min(100, max(3, 2*int(y.max() - y.min()))) if maxNHit==None else maxNHit]
    hRange = [None, [-0.5, bins[1]-0.5]]
        
    # 2d
    histo2d = ax[1, 0].hist2d(x, y, bins, range=hRange, cmap=pal2d, norm=LogNorm() if bLog else Normalize())
    ax[1, 0].set_xlabel(xFullName, fontsize="small")
    ax[1, 0].set_ylabel(yFullName, fontsize="small")
    
    # 2d extracting values and filling output dictionary
    xBars = np.array([x0 + (histo2d[1][1] - histo2d[1][0])/2 for x0 in histo2d[1][:-1]])
    yBars = np.array([y0 + (histo2d[1][1] - histo2d[1][0])/2 for y0 in histo2d[1][:-1]])
    zBars = histo2d[0]
    outName = y.name + "_" + xName + "_histo"
    outData[outName] = [xBars, yBars, zBars]
    print("2d spectrum returned in a dictionary with key %s -- x, y, z" % outName)
    print("--")
    
    # 2d selection (only if requested -- run by run)
    # recall that hitSel must be a dictionary with run names (range limits) as keys (values) --> if no runs are concerned, just use a single placeholder key (no need for a true run nr.)
    if bSel:
        for iRun in hitSel:
            plot_selectionY(ax[1, 0], hRange[1], hitSel[iRun], lineC, lineW)

    # 1d, run by run
    for iRun in (df[tRangeBool]["iRun"].unique() if len(lsBool)==0 else df[dfBool & tRangeBool]["iRun"].unique()):
        yTemp = y[(df["iRun"] == iRun) & tRangeBool] if len(lsBool)==0 else y[(df["iRun"] == iRun) & dfBool & tRangeBool]
        histo = ax[1, 1].hist(yTemp, bins[1], range=hRange[1], density=True, histtype="step", log=bLog)
        
        # extracting values and filling output dictionary
        print("studying %s when iRun = %s" % (var, iRun))
        xBars = np.array([x0 + (histo[1][1] - histo[1][0])/2 for x0 in histo[1][:-1]])
        yBars = histo[0]
        yErrs = np.sqrt(yBars / (bins[1] * yTemp.shape[0]))
        outName = y.name+"_"+iRun+"_histo"
        outData[outName] = [xBars, yBars, yErrs]
        print("1d spectrum returned in a dictionary with key %s -- x, y, ey" % outName)
        print("--")
        
    ax[1, 1].set_xlabel(yFullName, fontsize="small")
    ax[1, 1].set_title("%s in (%d, %d)" % (xName, tRange[0], tRange[1]), fontsize="small")
    
    # 1d selection (only if requested -- run by run)
    # recall that hitSel must be a dictionary with run names (range limits) as keys (values) --> if no runs are concerned, just use a single placeholder key (no need for a true run nr.)
    if bSel:
        for iRun in hitSel:
            plot_selectionX(ax[1, 1], hRange[1], hitSel[iRun], lineC, lineW)

    fig.suptitle(title, y=1, va="top", fontsize="small")
    fig.tight_layout()
    
    # save output figure
    if bSave:
        plt.savefig(fname="./out_plots/"+figName+".png", dpi=1000)
    
    # careful with outData:
    #     if a dictionary is given as argument:
    #         (0) 2d multiplicity-vs-time spectrum is added to the dictionary with key varY_xName_histo -- format: [x, y, z]
    #         (1) 1d multiplicity spectra are added to the dictionary with key varY_iRun_histo for each iRun involved -- format: [x, y, ey]
    #         (2) updated dictionary is returned
    #     if no dictionary is given as argument:
    #         (0) & (1) like the case above, but starting from an empty dictionary
    #         (2) the newly created dictionary is returned
    return outData

###############################################################################
###############################################################################

# x-y beam projection to a transverse plane with range delimiters (optional)
def plot_proj(
    df,  # MANDATORY
    var,  # MANDATORY -- full df name of the set of (x & y) beam projections without the vista index 0/1 (e.g. "xCry") or tuple with the full names of the 2 variables to be plotted (y-then-x)
    
    binSize = None,  # if None, 100*100 bins
    lsBool = [],  # list of boolean names (to be defined a priori as variables in df) to filter the data to plot
    hRange = [None, None],  # plot range -- shape [rangeX, rangeY] with range = [left, right] or None (i.e. automatic computation)
    bSel=False,  # cut edges are drawn only if True
    fidSel={},  # cut shape -- details below...
    bLog = False,  # if True (False), log (lin) scale on z
    lineC = plt.rcParams['axes.prop_cycle'].by_key()['color'][0],
    lineW = plt.rcParams['lines.linewidth'],
    pal2d = plt.rcParams["image.cmap"],
    units={},
    xSize=plt.rcParams["figure.figsize"][0],
    ySize=plt.rcParams["figure.figsize"][1],
    figName="temp",
    bSave=False,
):

    plt.close(figName)
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[xSize, ySize], num=figName)
    
    # plot boolean & corresponding title & x & y
    title = ""
    dfBool = True
    if len(lsBool)>0:
        for iBool in [df[s] for s in lsBool]:
            dfBool = dfBool & iBool
        x = df[dfBool][var+"0" if type(var)==str else var[0]]
        y = df[dfBool][var+"1" if type(var)==str else var[1]]
        for i in range(len(lsBool)-1):
            title += lsBool[i] + " & "
        title += lsBool[len(lsBool)-1]
    else:
        x = df[var+"0" if type(var)==str else var[0]]
        y = df[var+"1" if type(var)==str else var[1]]
    xFullName = x.name + (units[x.name] if x.name in units else "")
    yFullName = y.name + (units[y.name] if y.name in units else "")
    
    if hRange[0] is None:
        hRange[0] = [x.min(), x.max()]
    if hRange[1] is None:
        hRange[1] = [y.min(), y.max()]
    bins = [int(abs(hRange[0][1] - hRange[0][0]) / binSize), int(abs(hRange[1][1] - hRange[1][0]) / binSize)] if binSize!=None else [100, 100]

    # histogram
    ax.hist2d(x, y, bins=bins, range=hRange, cmap=pal2d, norm=LogNorm() if bLog else Normalize())
    ax.set_xlabel(xFullName, fontsize="small")
    ax.set_ylabel(yFullName, fontsize="small")
    
    # selection (only if requested -- run by run)
    # recall that fidSel must be a dictionary with run names (box vertexes) as keys (values) --> if no runs are concerned, just use a single placeholder key (no need for a true run nr.)
    if bSel:
        for iRun in fidSel:
            plot_selectionBox(ax, fidSel[iRun], lineC, lineW)
    
    fig.suptitle(title, y=1, va="top", fontsize="small")
    fig.tight_layout()
    
    # save output figure
    if bSave:
        plt.savefig(fname="./out_plots/"+figName+".png", dpi=1000)
    
###############################################################################
###############################################################################

# correlation between 2 goniometer DOF
def plot_gonioCorr(
    df,  # MANDATORY
    lsVar,  # MANDATORY -- x-then-y, format: part of the variable name following "xGonioRaw"
    
    lsBool = [],  # list of boolean names (to be defined a priori as variables in df) to filter the data to plot
    bLog = False,  # if True (False), log (lin) scale on z
    pal2d = plt.rcParams["image.cmap"],
    units={},
    xSize=plt.rcParams["figure.figsize"][0],
    ySize=plt.rcParams["figure.figsize"][1],
    figName="temp",
    bSave=False,
):
    
    plt.close(figName)
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[xSize, ySize], num=figName)
    
    bins = 200
    
    # plot boolean & corresponding title & x & y
    title = ""
    dfBool = True
    if len(lsBool)>0:
        for iBool in [df[s] for s in lsBool]:
            dfBool = dfBool & iBool
        x = df[dfBool]["xGonio"+lsVar[0]]
        y = df[dfBool]["xGonio"+lsVar[1]]
        for i in range(len(lsBool)-1):
            title += lsBool[i] + " & "
        title += lsBool[len(lsBool)-1]
    else:
        x = df["xGonio"+lsVar[0]]
        y = df["xGonio"+lsVar[1]]
    xFullName = x.name + (units[x.name] if x.name in units else "")
    yFullName = y.name + (units[y.name] if y.name in units else "")

    ax.hist2d(x, y, bins=bins, cmap=pal2d, norm=LogNorm() if bLog else Normalize())
    ax.set_xlabel(xFullName, fontsize="small")
    ax.set_ylabel(yFullName, fontsize="small")
    
    fig.suptitle(title, y=1, va="top", fontsize="small")
    fig.tight_layout()
    
    # save output figure
    if bSave:
        plt.savefig(fname="./out_plots/"+figName+".png", dpi=1000)
    
###############################################################################
############################################################################### 
    
# digitizer channels data: PH vs time (if time available, otherwise PH 1d distribution) & range delimiters (optional)
def plot_digi(
    df,  # MANDATORY
    lsVar,  # MANDATORY -- all the digitizer channels, format: part of the variable name following "digiPHRaw"
    
    binSize = [None, None],  # length=2 -- if one of the 2 values is None, 100 bins on the corresponding axis
    lsBool = [],  # list of boolean names (to be defined a priori as variables in df) to filter the data to plot
    bDigiTime = {},  # dictionary with the channel names (parts following digiPHRaw) as keys and True/False as values, depending on digiTime existence in df (check carefully!)
    bSel = False,  # cut edges are drawn only if True
    PHSel = {},  # x cut shape (overall cut x & y) -- details below...
    timeSel = {},  # y cut shape (overall cut x & y) -- details below...
    bLog = False,  # if True (False), log (lin) scale on z
    lineC = plt.rcParams['axes.prop_cycle'].by_key()['color'][0],
    lineW = plt.rcParams['lines.linewidth'],
    pal2d = plt.rcParams["image.cmap"],
    units={},
    xSize=plt.rcParams["figure.figsize"][0],
    ySize=plt.rcParams["figure.figsize"][1],
    figName="temp",
    bSave=False,
):

    plt.close(figName)
    nRows = int(np.ceil(len(lsVar)/2))
    fig, ax = plt.subplots(nrows=nRows, ncols=2, squeeze=False, figsize=[xSize, ySize], num=figName)
    
    # plot boolean & corresponding title & dictionaries with x & y for each channel
    title = ""
    x = {}
    y = {}
    dfBool = True
    if len(lsBool)>0:
        for iBool in [df[s] for s in lsBool]:
            dfBool = dfBool & iBool
        x = dict(zip(lsVar, [(df[dfBool]["digiTime"+s] if s in bDigiTime else None) for s in lsVar]))
        y = dict(zip(lsVar, [df[dfBool]["digiPH"+s] for s in lsVar]))
        for i in range(len(lsBool)-1):
            title += lsBool[i] + " & "
        title += lsBool[len(lsBool)-1]
    else:
        x = dict(zip(lsVar, [(df["digiTime"+s] if s in bDigiTime else None) for s in lsVar]))
        y = dict(zip(lsVar, [(df["digiPH"+s] if s in bDigiTime else None) for s in lsVar]))
        
    # also create a unique dictionary for the selections -- boxSel, from timeSel & PHSel
    # recall that PHSel & timeSel must be 2 dictionaries with run & then variable names (box vertexes) as keys (values) --> if no runs are concerned, just use a single placeholder key for run name in PHSet & timeSet (no need for a true run nr., but in order to have a box it has to be the same for both the dictionaries)
    boxSel = {}
    for iRun in np.unique(list(PHSel.keys()) + list(timeSel.keys())):
        boxSel[iRun] = {}
        for iVar in np.unique(lsVar):
            boxXRepl = [x[iVar].min() - 10*abs(x[iVar].max()-x[iVar].min()), x[iVar].max() + 10*abs(x[iVar].max()-x[iVar].min())]
            boxYRepl = [y[iVar].min() - 10*abs(y[iVar].max()-y[iVar].min()), y[iVar].max() + 10*abs(y[iVar].max()-y[iVar].min())]
            boxX = (timeSel[iRun][iVar] if iVar in timeSel[iRun] else boxXRepl) if iRun in timeSel else boxXRepl
            boxY = (PHSel[iRun][iVar] if iVar in PHSel[iRun] else boxYRepl) if iRun in PHSel else boxYRepl
            boxSel[iRun][iVar] =  boxX + boxY

    for i, iVar in enumerate(lsVar):
        xAx, yAx = int(np.floor(0.5*i)), i%2
        xFullName = x[iVar].name + (units[x[iVar].name] if x[iVar].name in units else "")
        yFullName = y[iVar].name + (units[y[iVar].name] if x[iVar].name in units else "")
        
        # histogram
        if bDigiTime[iVar]:  # time data available --> 2d histogram (PH vs time)
            hRange = [[x[iVar].min(), x[iVar].max()], [y[iVar].min(), y[iVar].max()]]
            bins = [int(abs((hRange[0][1] - hRange[0][0]) / binSize[0])) if binSize[0]!=None else 100, int(abs((hRange[1][1] - hRange[1][0]) / binSize[1])) if binSize[1]!=None else 100]
            ax[xAx, yAx].hist2d(x[iVar], y[iVar], bins=bins, range=hRange, cmap=pal2d, norm=LogNorm() if bLog else Normalize())
            ax[xAx, yAx].set_xlabel(xFullName, fontsize="small")
            ax[xAx, yAx].set_ylabel(yFullName, fontsize="small")
            
        else:  # time data unavailable --> 1d histogram w/ PH only
            hRange = [y[iVar].min(), y[iVar].max()]
            bins = int(abs((hRange[1][1] - hRange[1][0]) / binSize[1])) if binSize[1]!=None else 100
            ax[xAx, yAx].hist(y[iVar], bins=bins, range=hRange, histtype="step")
            ax[xAx, yAx].set_xlabel(yFullName, fontsize="small")
            
        # selection (only if requested -- run by run & variable by variable)
        # check boxSel construction above...
        if bSel:
            for iRun in boxSel:
                # iVar is available in boxSel[iRun].keys() by construction
                if bDigiTime[iVar]:  # time data available --> selection box
                    plot_selectionBox(ax[xAx, yAx], boxSel[iRun][iVar], lineC, lineW)
                else:  # time data unavailable -- > selection slice, only on PH
                    plot_selectionX(ax[xAx, yAx], hRange, PHSel[iRun][iVar], lineC, lineW)
            
    fig.suptitle(title, y=1, va="top", fontsize="small")
    fig.tight_layout()
    
    # save output figure
    if bSave:
        plt.savefig(fname="./out_plots/"+figName+".png", dpi=1000)
    
###############################################################################
############################################################################### 

# 1d single energy spectrum -- can also be coupled to an already existing figure
# returns a dictionary -- see below...
def plot_energySingle(
    df,  # MANDATORY
    var,  # MANDATORY -- energy value, format: part of the variable name following "E"
    binSize,  # MANDATORY -- can't be set to None
    
    xRange0 = None,  # [min, max] or None -- if None, automatically defined
    fig = None,  # 1st output of a figure created externally with plt.subplots() -- if None, 1*1 brand new figure is created here
    ax = None,  # 2nd output of a figure created externally with plt.subplots() -- if None, 1*1 brand new figure is created here
    lsBool = [],  # list of boolean names (to be defined a priori as variables in df) to filter the data to plot
    bLog = False,  # if True (False), log (lin) scale on y
    label = None,  # plot label in the final legend -- if None, plot is not added to legend or, if no legend already existing, legend is not created
    title0 = None,  # figure title -- if None, title is created automatically according to lsBool (i.e. listing all the applied booleans)
    outData = {},  # dictionary that will be updated with the spectrum values -- details below...
    units={},
    histC = plt.rcParams['axes.prop_cycle'].by_key()['color'][0],
    newXSize=plt.rcParams["figure.figsize"][0],
    newYSize=plt.rcParams["figure.figsize"][1],
    newFigName="temp",
    bSave=False,
):
    
    # new figure is created only if fig or ax argument is not passed or is None, i.e. if figure isn't already existing
    if ((fig is None) | (ax is None)):
        plt.close(figName)
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[newXSize, newYSize], num=newFigName)
            
    # spectrum is created only if ax has the right typing (plt.subplots() output np.array in case of multidimensional figures)
    if str(type(ax))=="<class 'matplotlib.axes._axes.Axes'>":  # small tweak applied on 22/2/2024!
    # if str(type(ax))=="<class 'matplotlib.axes._subplots.AxesSubplot'>":
        
        # plot boolean & title (corresponding to boolean if title0 is None, else title0) & variable
        title = "" if title0==None else title0
        dfBool = True
        if len(lsBool)>0:
            for iBool in [df[s] for s in lsBool]:
                dfBool = dfBool & iBool
            x = df[dfBool]["E"+var]
            if title0==None:
                for i in range(len(lsBool)-1):
                    title += lsBool[i] + " & "
                title += lsBool[len(lsBool)-1]
        else:
            x = df["E"+var]
        xName = x.name
        xFullName = xName + (units[xName] if xName in units else "")

        xRange = [x.min(), x.max()] if xRange0==None else xRange0
        bins = int(abs(xRange[1] - xRange[0]) / binSize)

        ax.set_xlabel(xFullName, fontsize="small")

        # histogram
        histo = ax.hist(x, bins, range=xRange, density=True, log=bLog, histtype="step", label=label, color=histC)

        # errorbars
        xBars = np.array([x0 + (histo[1][1] - histo[1][0])/2 for x0 in histo[1][:-1]])
        yBars = histo[0]
        yErrs = np.sqrt(yBars / (binSize * x.shape[0]))
        ax.errorbar(xBars, yBars, yerr=yErrs, fmt="none", c=histC)

        # (leftmost) spectrum max
        xMax = xBars[np.argmax(yBars)]
        print("spectrum created, with (leftmost) maximum @ E%s = %.3f" % (var, xMax))

        # filling output dictionary with the spectrum
        outName = (xName+"_"+label+"_histo") if label!=None else xName+"_histo"
        outData[outName] = [xBars, yBars, yErrs]
        print("spectrum returned in a dictionary with key %s -- x, y, ey" % outName)

        if label != None:  # legend is updated (or created, if not already existing) only if label isn't None
            ax.legend(fontsize="small")
        fig.suptitle(title, y=1, va="top", fontsize="small")
        fig.tight_layout()
            
    else:
        print("subplot typing mismatch --> no E%s plot performed\n--" % var)
        
    # save output figure
    if bSave:
        plt.savefig(fname="./out_plots/"+figName+".png", dpi=1000)

    # careful with outData:
    #     if a dictionary is given as argument and the spectrum is created, a list with x, y & ey is added to the dictionary with key xName_label (or xName if label=None) & the updated dictionary is returned
    #     if no dictionary is given as argument and the spectrum is created, a new dictionary with the same elements of the case above is returned
    #     if a dictionary is given as argument and the spectrum is not created, the input dictionary is returned unchanged
    #     if no dictionary is given as argument and the spectrum is not created, an empty dictionary is returned
    return outData

###############################################################################
###############################################################################

# 1d energy typeRun-by-typeRun spectra & 2d trend vs time
# returns a dictionary -- see below...
def plot_energyRuns(
    df,  # MANDATORY
    var,  # MANDATORY -- energy value, format: part of the variable name following "E"
    binSize,  # MANDATORY -- can't be set to None
    bE,  # MANDATORY -- dictionary with the run numbers as keys & True/False as values, depending on the variable existence in df (check carefully!)

    xRange0 = None,  # [min, max] or None -- if None, automatically defined
    bEpoch=False,  # set it True only if the epoch variable actually exists in df
    bUseEpoch=False,  # if False, event index in the current execution (always available) is used -- only if epoch in df, otherwise index anyway
    lsBool = [],  # list of boolean names (to be defined a priori as variables in df) to filter the data to plot
    bLog = False,  # if True (False), log (lin) scale on y in 1d plots & z in 2d plots
    outData = {},  # dictionary that will be updated with all the spectra values bin by bin -- details in plot_energySingle()
    pal2d = plt.rcParams["image.cmap"],
    units={}, 
    xSize=plt.rcParams["figure.figsize"][0],
    ySize=plt.rcParams["figure.figsize"][1],
    figName="temp",
    bSave=False,
):

    plt.close(figName)
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=[xSize, ySize], num=figName)
    
    # plot boolean & corresponding title
    # also x & y for the 2d plot -- 1d is dealt with in plot_energySingle()
    title = ""
    dfBool = True
    if len(lsBool)>0:
        for iBool in [df[s] for s in lsBool]:
            dfBool = dfBool & iBool
        x2d = df[dfBool]["epoch"] if (bEpoch & bUseEpoch) else df[dfBool].index
        y2d = df[dfBool]["E"+var]
        for i in range(len(lsBool)-1):
            title += lsBool[i] + " & "
        title += lsBool[len(lsBool)-1]
    else:
        x2d = df["epoch"] if (bEpoch & bUseEpoch) else df.index
        y2d = df["E"+var]
    xUnit = units[x2d.name] if x2d.name in units else ""
    yUnit = units[y2d.name] if y2d.name in units else ""
    x2dFullName = x2d.name+xUnit if (bEpoch & bUseEpoch) else "index"
    y2dFullName = y2d.name+yUnit

    # 1d spectra (run-by-run)
    for i, iTypeRun in enumerate(np.unique([df[dfBool & (df["iRun"]==s)]["typeRun"].unique()[0] for s in bE if bE[s]])):
        print("studying E%s when typeRun = %s" % (var, iTypeRun))
        histC = plt.rcParams['axes.prop_cycle'].by_key()['color'][i]
        outData = plot_energySingle(df[dfBool & (df["typeRun"] == iTypeRun)], var, binSize, xRange0, fig, ax[0], lsBool, bLog, iTypeRun, "", outData, units, histC, bSave=False)
        print("--")
        
    # 2d -- value over time
    bins = [min(1000, x2d.max() - x2d.min()), 100]
    ax[1].hist2d(x2d, y2d, bins, range=[None, xRange0], norm=LogNorm() if bLog else Normalize(), cmap=pal2d)
    ax[1].set_xlabel(x2dFullName, fontsize="small")
    ax[1].set_ylabel(y2dFullName, fontsize="small")
    
    fig.suptitle(title, y=1, va="top", fontsize="small")
    fig.tight_layout()
    
    # save output figure
    if bSave:
        plt.savefig(fname="./out_plots/"+figName+".png", dpi=1000)
        
    # careful with outData: see details in plot_energySingle()
    return outData
            
###############################################################################
###############################################################################

# custom variable trend vs one or more goniometer DOF + profile plot (always) + degree-0, -1 or -2 polynomial fit (optional) -- also check dictGonioX format for analysis parameters
# returns a dictionary -- see below...
def plot_gonioTrends(
    df,  # MANDATORY
    varY,  # MANDATORY -- full variable name in df
    dictGonioX,  # MANDATORY -- list of goniometer DOF to be studied with varY & of analysis parameter -- check below... 
    
    lsBool = [],  # list of boolean names (to be defined a priori as variables in df) to filter the data to plot
    outData = {},  # dictionary that will be updated with the profile plots & fit parameters -- details below...
    bLog = False,  # if True (False), log (lin) scale on z
    fitC = plt.rcParams['axes.prop_cycle'].by_key()['color'][0],
    fitW = plt.rcParams['lines.linewidth'],
    lineC = plt.rcParams['axes.prop_cycle'].by_key()['color'][0],
    lineW = plt.rcParams['lines.linewidth'],
    pal2d = plt.rcParams["image.cmap"],
    units={},
    xSize=plt.rcParams["figure.figsize"][0],
    ySize=plt.rcParams["figure.figsize"][1],
    figName="temp",
    bSave=False,
):
    
    # # # # # # # # # # # # # # # # # # # # 
    # dictGonioX
    # dictionary of the variables to be analysed -- shape:
    # {varY (string): {
    #         varX0 (string): [[xL0, xR0, dx0], [yL0, yR0, dy0], [bFit0 (bool), deg0 (integer/"Gaussian"), xFitL0, xFitR0]], (float if not otherwise specified)
    #         varX1: [[xL1, xR1, dx1], [yL1, yR1, dy1], [bFit1, deg1, xFitL1, xFitR1]],
    #         ...
    # }}
    # 1 figure per varY, each with 1 plot per varX -- varX format: part of the variable name following "xGonioRaw"
    # plot in ranges (xL, xR) & (yL, yR) with bin size dx & dy
    # polynomial fit with degree deg -- supported deg = 0, 1, 2; Gaussian fit if deg = "Gaussian"
    # all entries (apart from bFit) can also be None -- automatic definition in this case (e.g. deg = 0)
    # # # # # # 
    
    figNameFull = "%s_%s" % (figName, varY)
    plt.close(figNameFull)
    nRows = len(dictGonioX)
    fig, ax = plt.subplots(nrows=nRows, ncols=1, squeeze=False, figsize=[xSize, ySize], num=figNameFull)
    
    title = ""
    if len(lsBool)>0:
        dfBoolGlob = True
        for iBool in [df[s] for s in lsBool]:
            dfBoolGlob = dfBoolGlob & iBool
        for i in range(len(lsBool)-1):
            title += lsBool[i] + " & "
        title += lsBool[len(lsBool)-1]
        # figure title will include all the names of the global booleans
    
    for i, iX in enumerate(dictGonioX):  # loop on all the goniometer DOF to be studied vs varY
        
        xName = "xGonio"+iX 
        print("studying %s vs %s" % (varY, xName))

        x0 = df[dfBoolGlob][xName] if len(lsBool)>0 else df[xName]
        y0 = df[dfBoolGlob][varY] if len(lsBool)>0 else df[varY]
        
        # if lower/upper range boundary is None, itis set to the min/max value of the distribution (with global selection)
        xL = dictGonioX[iX][0][0] if dictGonioX[iX][0][0] != None else x0.min()
        xR = dictGonioX[iX][0][1] if dictGonioX[iX][0][1] != None else x0.max()
        yL = dictGonioX[iX][1][0] if dictGonioX[iX][1][0] != None else y0.min()
        yR = dictGonioX[iX][1][1] if dictGonioX[iX][1][1] != None else y0.max()
        dx = dictGonioX[iX][0][2] if dictGonioX[iX][0][2] != None else (xR-xL) / 100
        dy = dictGonioX[iX][1][2] if dictGonioX[iX][1][2] != None else (yR-yL) / 100
        hRange = [[xL, xR], [yL, yR]]
        bins = [max(1, int((xR-xL) / dx)), max(1, int((yR-yL) / dy))]
        
        dfBoolLocX = (df[xName] >= xL) & (df[xName] <= xR)
        dfBoolLocY = (df[varY] >= yL) & (df[varY] <= yR)
        dfBoolLoc = dfBoolLocX & dfBoolLocY
        x = df[dfBoolGlob & dfBoolLoc][xName] if len(lsBool)>0 else df[dfBoolLoc][xName]
        y = df[dfBoolGlob & dfBoolLoc][varY] if len(lsBool)>0 else df[dfBoolLoc][varY]
        
        xFullName = xName + (units[xName] if xName in units else "")
        yFullName = y.name + (units[y.name] if y.name in units else "")
        subtitle = "(%f <= %s <= %f) & (%f <= %s <= %f)" % (xL, xName, xR, yL, y.name, yR)
        
        # histogram
        histo = ax[i, 0].hist2d(x, y, bins=bins, range=hRange, cmap=pal2d, norm=LogNorm() if bLog else Normalize())
        ax[i, 0].set_xlabel(xFullName, fontsize="small")
        ax[i, 0].set_ylabel(yFullName, fontsize="small")
        ax[i, 0].set_title(subtitle, fontsize="small")
        
        # profile plot
        profile = sl.hist2dToProfile(histo, "mean")
        # keeping only points with nonzero error (i.e. x slices with at least 2 nonempty y bins)
        xProf = np.array([k for j, k in enumerate(profile[0]) if profile[2][j] != 0])
        yProf = np.array([k for j, k in enumerate(profile[1]) if profile[2][j] != 0])
        eyProf = np.array([j for j in profile[2] if j != 0])
        if len(xProf) > 1:  # using only profile plots with at least 2 points (with nonzero error)
            outData["%s_%s_prof" % (varY, xName)] = [xProf, yProf, eyProf]
            print("profile plot returned in a dictionary with key %s -- x, y, ey" % ("%s_%s_prof" % (varY, xName)))
            if dictGonioX[iX][2][0]:  # profile plot drawn only if requested (while outData is filled anyway with "..._prof" entry)
                ax[i, 0].plot(xProf, yProf, color=lineC, linewidth=lineW)
                ax[i, 0].plot(xProf, [yProf[j] - eyProf[j] for j in range(len(xProf))], color=lineC, linestyle=":", linewidth=lineW)
                ax[i, 0].plot(xProf, [yProf[j] + eyProf[j] for j in range(len(xProf))], color=lineC, linestyle=":", linewidth=lineW)
            else:
                print("as requested, profile plot not drawn")
            
        else:
            print("no profile plot drawn (0 or 1 points only)")
            
        # polynomial fit
        if len(xProf) > 1:  # also fit only profile plots with at least 2 points (with nonzero error)
            if dictGonioX[iX][2][1]:  # fit only if requested (also applied to outData "..._fit" entry)
                xFitL = dictGonioX[iX][2][3] if dictGonioX[iX][2][3] != None else min(xProf)
                xFitR = dictGonioX[iX][2][4] if dictGonioX[iX][2][4] != None else max(xProf)
                xFit = [k for k in xProf if ((k>=xFitL) & (k<=xFitR))]
                yFit = [k for j, k in enumerate(yProf) if ((xProf[j]>=xFitL) & (xProf[j]<=xFitR))]
                eFit = [k for j, k in enumerate(eyProf) if ((xProf[j]>=xFitL) & (xProf[j]<=xFitR))]
                
                # polynomial degree -- if None, degree 0 polynomial (i.e. offset) if selected -- if "Gaussian", Gaussian function is selected
                polyDeg = dictGonioX[iX][2][2] if dictGonioX[iX][2][2]!=None else 0
                if polyDeg=="Gaussian":
                    polyName = "Gaussian"
                elif polyDeg==0:
                    polyName = "offset"
                elif polyDeg==1:
                    polyName = "linear"
                elif polyDeg==2:
                    polyName = "parabolic"
                else:
                    print("unsupported polynomial degree --> offset fit will be performed")
                    polyDeg=0
                    polyName = "offset"
                
                label = "%s fit in (%.4f, %.4f)" % (polyName, xFitL, xFitR)
                print("performing %s fit on %s vs %s in (%f, %f)..." % (polyName, varY, xName, xFitL, xFitR))
                
                if polyDeg=="Gaussian":
                    fPoly = sl.fGaus
                    # parameter starting points given in case of Gaussian fit
                    parGaus = [max(yFit)-np.mean(yFit), xFitL+0.5*(xFitR-xFitL), max(0.1*(xFitR-xFitL), (xFit[1]-xFit[0]))]
                elif polyDeg==0:
                    fPoly = lambda x, x0: 0*x + x0
                elif polyDeg==1:
                    fPoly = lambda x, m, q: m*x + q
                elif polyDeg==2:
                    fPoly = lambda x, a, b, c: a*x*x + b*x + c

                # fit here
                p, cov = curve_fit(fPoly, xFit, yFit, sigma=eFit, p0=parGaus if polyDeg=="Gaussian" else None)
                ep = [np.sqrt(cov[k, k]) for k in range(len(p))]
                print("fit parameters (highest-power first):" if polyDeg!="Gaussian" else "fit parameters (ampl., mean, sigma)")
                for j in range(len(p)):
                    print("\t%e +- %e" % (p[j], ep[j]))
                if polyDeg=="Gaussian":
                    label += "\n(mean, sigma) = (%.3f, %.3f)" % (p[1], p[2])
                if polyDeg==0:
                    label += "\nvalue = %.3f" % p[0]
                if polyDeg==1:
                    label += "\nslope = %.9f" % p[0]
                if polyDeg==2:
                    xVertex = - p[1] / (2*p[0])
                    yVertex = fPoly(xVertex, *p)
                    label += "\nvertex @ (x, y) = (%.3f, %.3f)" % (xVertex, yVertex)
                    print("\t--> parabola vertex @ (x, y) = (%e, %e)" % (xVertex, yVertex))
                    
                xFitPlot = np.linspace(min(xFit), max(xFit), 500)
                ax[i, 0].plot(xFitPlot, fPoly(xFitPlot, *p), fitC, linewidth=fitW, label=label)
                ax[i, 0].legend(fontsize="small")

                # filling output dictionary (shape differs depending on the polynomial degree)
                outData["%s_%s_fit" % (varY, xName)] = [polyDeg, p, cov]
                if polyDeg==2:
                    outData["%s_%s_fit" % (varY, xName)] += [(xVertex, yVertex)]
                    print("fit info are returned in a dictionary with key %s -- deg., par., cov. matr., vertex" % ("%s_%s_fit" % (varY, xName)))
                else:
                    print("fit info are returned in a dictionary with key %s -- deg., par., cov. matr." % ("%s_%s_fit" % (varY, xName)))
                
            else:
                print("fit not performed (not requested)")
                
        print("--")

    fig.suptitle(title, y=1, va="top", fontsize="small")
    fig.tight_layout()
    
    # save output figure
    if bSave:
        plt.savefig(fname="./out_plots/"+figName+".png", dpi=1000)
    
    # careful with outData:
    #     if a dictionary is given as argument:
    #         (0) profile plots (only those with more than 1 point) are added to the dictionary with key varY_xName_prof for each xName -- format: [x, y, ey]
    #         (1) fit parameters are added to the dictionary with key varY_xName_fit for each xName whose fit is performed -- format: [parameters, cov. matrix]
    #         (2) updated dictionary is returned
    #     if no dictionary is given as argument:
    #         (0) & (1) like the case above, but starting from an empty dictionary
    #         (2) the newly created dictionary is returned
    return outData

###############################################################################
###############################################################################

# beam profiles (2 together) to a transverse plane with range delimiters (optional)
# returns a dictionary -- see below...
def plot_prof(
    df,  # MANDATORY
    var,  # MANDATORY -- tuple with the names of the 2 spatial variables to be plotted
    
    binSize = None,  # if None, 100*100 bins
    lsBool = [],  # list of boolean names (to be defined a priori as variables in df) to filter the data to plot
    hRange = [None, None],  # plot range -- shape [rangeX, rangeY] with range = [left, right] or None (i.e. automatic computation)
    outData = {},  # dictionary that will be updated with the spectrum & statistical parameters -- details below...
    bLog = False,  # if True (False), log (lin) scale on z
    units={},
    xSize=plt.rcParams["figure.figsize"][0],
    ySize=plt.rcParams["figure.figsize"][1],
    figName="temp",
    bSave=False,
):

    plt.close(figName)
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=[xSize, ySize], num=figName)
    
    # plot boolean & corresponding title & x & y
    title = ""
    dfBool = True
    if len(lsBool)>0:
        for iBool in [df[s] for s in lsBool]:
            dfBool = dfBool & iBool
        x = df[dfBool][var[0]]
        y = df[dfBool][var[1]]
        for i in range(len(lsBool)-1):
            title += lsBool[i] + " & "
        title += lsBool[len(lsBool)-1]
    else:
        x = df[var[0]]
        y = df[var[1]]
    xFullName = x.name + (units[x.name] if x.name in units else "")
    yFullName = y.name + (units[y.name] if y.name in units else "")
    
    if hRange[0] is None:
        hRange[0] = [x.min(), x.max()]
    if hRange[1] is None:
        hRange[1] = [y.min(), y.max()]
    bins = [int(abs(hRange[0][1] - hRange[0][0]) / binSize), int(abs(hRange[1][1] - hRange[1][0]) / binSize)] if binSize!=None else [100, 100]

    # histograms & some stats
    histo = ax[0].hist(x, bins[0], range=hRange[0], histtype="step", log=bLog)
    ax[0].set_xlabel(xFullName, fontsize="small")
    xBarsX = np.array([x0 + (histo[1][1] - histo[1][0])/2 for x0 in histo[1][:-1]])
    yBarsX = histo[0]
    yErrsX = np.array([max(1, np.sqrt(y0)) for y0 in yBarsX])
    outName = x.name + "_histo"
    outData[outName] = [xBarsX, yBarsX, yErrsX]
    print("%s spectrum returned in a dictionary with key %s -- x, y, ey" % (x.name, outName))
    
    meanX = sum([x0*y0 for x0, y0 in zip(xBarsX, yBarsX)]) / sum(yBarsX)
    fwhmPopX = [xBarsX[i] for i in list(np.where(np.array(yBarsX)>0.5*max(yBarsX))[0])]
    fwhmX = max(fwhmPopX) - min(fwhmPopX)
    fwhmCentreX = min(fwhmPopX) + fwhmX/2
    outName = x.name + "_stat"
    outData[outName] = [meanX, fwhmCentreX, fwhmX]
    print("stats:")
    print("\tmean\t\t\t%f" % meanX)
    print("\tFWHM range centre\t%f" % fwhmCentreX)
    print("\tFWHM\t\t\t%f" % fwhmX)
    print("==> returned in a dictionary with key %s -- mean, FWHM range centre, FWHM" % outName)
    print("--")
    
    histo = ax[1].hist(y, bins[1], range=hRange[1], histtype="step", log=bLog)
    ax[1].set_xlabel(yFullName, fontsize="small")
    xBarsY = np.array([x0 + (histo[1][1] - histo[1][0])/2 for x0 in histo[1][:-1]])
    yBarsY = histo[0]
    yErrsY = np.array([max(1, np.sqrt(y0)) for y0 in yBarsY])
    outName = y.name + "_histo"
    outData[outName] = [xBarsY, yBarsY, yErrsY]
    print("%s spectrum returned in a dictionary with key %s -- x, y, ey" % (y.name, outName))
    
    meanY = sum([x0*y0 for x0, y0 in zip(xBarsY, yBarsY)]) / sum(yBarsY)
    fwhmPopY = [xBarsY[i] for i in list(np.where(np.array(yBarsY)>0.5*max(yBarsY))[0])]
    fwhmY = max(fwhmPopY) - min(fwhmPopY)
    fwhmCentreY = min(fwhmPopY) + fwhmY/2
    outName = y.name + "_stat"
    outData[outName] = [meanY, fwhmCentreY, fwhmY]
    print("stats:")
    print("\tmean\t\t\t%f" % meanY)
    print("\tFWHM range centre\t%f" % fwhmCentreY)
    print("\tFWHM\t\t\t%f" % fwhmY)
    print("==> returned in a dictionary with key %s -- mean, FWHM range centre, FWHM" % outName)
    print("--")
    
    fig.suptitle(title, y=1, va="top", fontsize="small")
    fig.tight_layout()
    
    # save output figure
    if bSave:
        plt.savefig(fname="./out_plots/"+figName+".png", dpi=1000)
        
    # careful with outData:
    #     if a dictionary is given as argument, both the spectra (x, y, ey) and the stats (mean, FWHM/2, center of the FWHM range) are added to it with the variable names as keys (plus "_histo" and "_stat" respectively) & the updated dictionary is returned
    #     if no dictionary is given as argument, a new dictionary with the aforementioned content is returned
    return outData