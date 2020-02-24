#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymisca.ext as pyext
NCORE = 10
execfile(pyext.base__file('headers/header__import.py'))
# tks = pyutil.readBaseFile('results/0130__makeTracks-Brachy/tracks.npy').tolist()
figs = pyutil.collections.OrderedDict()


ENT_CUTOFF=2.6
ENT_CUTOFF=2.0
STEP = 100

figsize=[14,5]


mdl0 = pyutil.readBaseFile('results/0206__cluster__PIF7/mdl.npy').tolist()
mdl = mdl0.callback.mdls[STEP][-1]
mdl.predict = pyutil.functools.partial(mdl.predict, 
                                              entropy_cutoff=ENT_CUTOFF)
clu0 = clu= mdl.predictClu(mdl0.data, index=mdl0.data.index )
cacheFile = pyutil.cache__model4data(mdl,
                                     tdf=mdl0.data,
                                     ofname='cache.npy')
dClu = pyutil.readData(cacheFile)
# clu0 = clu= mdl.predictClu(mdl0.data, entropy_cutoff=ENT_CUTOFF,index=mdl0.data.index )
# clu.to_csv()

plt.rcParams['font.size'] = 14.
plt.rcParams['xtick.labelsize'] = 16.
plt.rcParams['axes.titlepad'] = 24.

dClu = pyutil.readData(cacheFile).tolist()
order = dClu['stats']

common = dict(
    figsize=[14, 7],
    show_axa = 1,
    show_axc = 0,
    showGrid = 0,
    width_ratios = [1,14,0.]
#     title= '',
#     height_ratios = [1,3,3,3,1],
    )

axs = pyjob.qc__vmf(mdl0)
fig = plt.gcf()
ax=  fig.axes[0]
pyvis.abline(y0=ENT_CUTOFF,k=0,ax=ax)
pyvis.abline(x0=STEP,ax=ax)
figs['qcVMF'] = fig


clu = clu.sort_values('clu')
vdf = scount.countMatrix( mdl0.data)
vdf = vdf.reindex(clu.index)
vdf.heatmap(figsize=figsize)
plt.title('N=%d'%len(vdf))
figs['allClu'] = plt.gcf() 

vdf = scount.countMatrix( mdl0.data)
vdf = vdf.reindex(clu.query('clu!=-1').index)
vdf.heatmap(figsize=figsize)
plt.title('N=%d'%len(vdf))
figs['sureClu'] = plt.gcf() 




clu0.to_csv('clu.csv')
pyutil.render__images(figs,)