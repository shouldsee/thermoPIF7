#!/usr/bin/env python
# -*- coding: utf-8 -*-
BACKEND='agg'
execfile('/home/feng/headers/header__import.py')
r = 1000
X = np.random.random(size=(r,r))

tks = pyutil.readBaseFile('figures/0108__prepareRNA__PIF7/cache.npy').tolist()

trainData = tks['rnaseq_wt_27C17C']
testData = tks['rnaseq_pif7col_27C']
X = trainData.values[:5000].T

figsize=[12,6]
def saveFig():
    fig.savefig('%d.png'% i)
    fig.savefig('%d.svg'% i)

i = -1
i += 1

fig = plt.figure(figsize=figsize)
ax=  plt.gca()
ax.matshow(X)
saveFig()

i+= 1
fig = plt.figure(figsize=figsize)
ax=  plt.gca()
ax.imshow(X,aspect='auto')
saveFig()

i+= 1
fig = plt.figure(figsize=figsize)
ax=  plt.gca()
ax.matshow(X,aspect='auto')
saveFig()

i+= 1
fig = plt.figure(figsize=figsize)
ax=  plt.gca()
ax.pcolormesh(X)
saveFig()
