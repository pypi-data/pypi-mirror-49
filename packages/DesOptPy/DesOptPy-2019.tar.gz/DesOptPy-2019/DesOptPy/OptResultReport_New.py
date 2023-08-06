try:
    import _pickle as pickle
except:
    try:
        import cPickle as pickle
    except:
        import pickle
try:
    from matplotlib2tikz import save as tikz_save
    TikzRendered = True
except:
    TikzRendered = False
TikzRendered = False
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.colors as colors
from matplotlib import cm
from matplotlib.font_manager import FontProperties
import numpy as np

fontP = FontProperties()
fontP.set_size(10)
FileTypeRendered = ["png", "svg"]

def BarPlot(figName, fun0, funOpt, funLabel0, funLabelOpt, xLabel, yLabel,
            ResultsFolder, OptName, figType=FileTypeRendered, Color0='#FAA43A',
            ColorOpt='#5DA5DA', figsizex=6, figsizey=3, width=0.5,
            xspacing=0.25, dpi=200, xtick=True, usetex=False, Tikz=True):
    plt.rc('text', usetex=usetex)
    Plot = plt.figure(figsize=(figsizex, figsizey), dpi=dpi)
    ax = Plot.add_subplot(111)
    nf = np.size(fun0)
    ind = np.arange(nf)
    rects1 = ax.bar(ind+xspacing*2.5, fun0, width, color=Color0)
    rects2 = ax.bar(ind+xspacing*2.5+width/2, funOpt, width, color=ColorOpt)
    lgd = ax.legend((rects1[0], rects2[0]), (funLabel0, funLabelOpt),
                    frameon=False, prop=fontP, bbox_to_anchor=(1.05, 1),
                    loc=2, borderaxespad=0.)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.xlim(xmin=xspacing*2, xmax=nf+width/2+xspacing)
    plt.ylim(ymin=np.min((np.min(fun0), np.min(funOpt), 0.0)),
             ymax=np.max((np.max(fun0), np.max(funOpt))))
    if xtick == False:
        plt.tick_params(axis='x', which='both', bottom='off',
                        labelbottom='off')
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    #plt.tight_layout()
    for ii in range(np.size(figType)):
        plt.savefig(ResultsFolder+OptName+'_'+figName+'.'+figType[ii],
                    bbox_extra_artists=(lgd,), bbox_inches='tight')
    if Tikz==True:
        tikz_save(ResultsFolder+OptName+'_'+figName+'.tikz')
    plt.close()
    fail = 0
    return fail

def LoadData(optname, DesOptDir):
    return()



def OptResultReport(optname, OptAlg, DesOptDir, diagrams=1, tables=0, lyx=0):
    DirRunFiles = DesOptDir + "/Results/"+optname+"/RunFiles/"
    ResultsFolder = DesOptDir + "/Results/"+optname+"/ResultReport/"
    file_OptSolData = open(DirRunFiles+optname+"_OptSol.pkl", "rb")
    OptSolData = pickle.load(file_OptSolData)
    x0 = OptSolData['x0']
    xOpt = OptSolData['xOpt']
    xOptNorm = OptSolData['xOptNorm']
    xIter = OptSolData['xIter'].T
    xIterNorm = OptSolData['xIterNorm'].T
    fOpt = OptSolData['fOpt']
    fIter = OptSolData['fIter']
    fIterNorm = OptSolData['fIterNorm']
    gOpt = OptSolData['gOpt']
    gIter = OptSolData['gIter'].T
    gMaxIter = OptSolData['gMaxIter']
    fGradIter = OptSolData['fNablaIter'].T
    gGradIter = OptSolData['gNablaIter'].T
    fGradOpt = OptSolData['fNablaOpt']
    gGradOpt = OptSolData['gNablaOpt']
    OptName = OptSolData['OptName']
    OptModel = OptSolData['OptModel']
    OptTime = OptSolData['OptTime']
    today = OptSolData['today']
    computerName = OptSolData['computerName']
    operatingSystem = OptSolData['operatingSystem']
    architecture = OptSolData['architecture']
    nProcessors = OptSolData['nProcessors']
    userName = OptSolData['userName']
    Alg = OptSolData['Alg']
    DesVarNorm = OptSolData['DesVarNorm']
    KKTmax = OptSolData['KKTmax']
    lambda_c = OptSolData['lambda_c']
    nEval = OptSolData['nEval']
    nIter = OptSolData['nIter']
    SPg = OptSolData['SPg']
    gc = OptSolData['gc']
    # OptAlg = OptSolData['OptAlg']
    x0norm = OptSolData['x0norm']
    xL = OptSolData['xL']
    xU = OptSolData['xU']
    ng = OptSolData['ng']
    nx = OptSolData['nx']
    nf = OptSolData['nf']
    Opt1Order = OptSolData['Opt1Order']
    hhmmss0 = OptSolData['hhmmss0']
    hhmmss1 = OptSolData['hhmmss1']


    fail = BarPlot("gBarRendered", gIter[0], gOpt, "$g^0$", "$g^{*}$",
                   "Constraint", "$g$", ResultsFolder, OptName,
                   figType=FileTypeRendered, Color0='#FAA43A',
                   ColorOpt='#5DA5DA', figsizex=6, figsizey=3,
                   width=0.5, xspacing=0.25, dpi=200, usetex=True,
                   Tikz=TikzRendered)
    print(x0)





if __name__ == "__main__":
    print("test of DesOptPy result report")
    optname = "test"
    OptAlg = "NLPQLP"  # OptAlg = "NSGA2"
    DesOptDir = "test"
    OptResultReport(optname, OptAlg, DesOptDir, diagrams=1, tables=1, lyx=1)