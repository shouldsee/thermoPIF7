#!/usr/bin/env python
# -*- coding: utf-8 -*-

NCORE = 10
import pymisca.ext as pyext
import pymisca.jobs as pyjob
execfile(pyext.base__file('headers/header__import.py'))
figs = pyutil.collections.OrderedDict()

# keyDF = pyutil.readBaseFile('headers/key_brachy.csv')


tks = pyutil.readBaseFile('figures/0108__prepareRNA__PIF7/cache.npy').tolist()

trainData = tks['rnaseq_wt_27C17C']
testData = tks['rnaseq_pif7col_27C']

tdf = pd.concat([trainData,testData],axis=1)


mdl0 = pyjob.job__cluster__mixtureVMF__incr(
#     normalizeSample=1,
    tdf        = tdf,
    meanNorm   = 0,
    init_method= 'random',
    nIter      = 250,
    start      = 0.001,
    end        = 20.0,
    verbose    = 2,
    K          = 40,)

np.save('mdl.npy',mdl0)

axs = pyjob._mod1.qc__vmf(mdl0)

fig = plt.gcf()
ax=  fig.axes[0]
# pyvis.abline(y0=3.7,k=0,ax=ax)

figs['qcVMF'] = fig

pyutil.render__images(figs,)