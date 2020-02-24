#!/usr/bin/env python
# BACKEND='GTK3Cairo'
# BACKEND='cairo'
BACKEND='agg'
NCORE = 10
import pymisca.ext as pyext
execfile(pyext.base__file('headers/header__import.py'))
figs = pyutil.collections.OrderedDict()

import pymisca.jobs as pyjob

execfile('/home/feng/envs/Fig_PIF/loadRNA_Ath.py')


# rnaCluFile = '/home/feng/envs/Fig_PIF/cluster.csv'
# rnaCluFile = '/home/feng/figureScript/notebooks/clu.csv'
# pyutil.readBaseFile()
clu = pyutil.readBaseFile('results/0206__showCluster__PIF7/clu.csv')
dClu = pyutil.readBaseFile('results/0206__showCluster__PIF7/cache.npy').tolist()
order = dClu['stats']

clu = scount.countMatrix(clu,)
clu.to_csv('clu.csv')
clu = clu.query('clu!=-1')
# rnaCluFile = ''
cluAuxin = 7

tdf = dfc =  rnaseq_wt_27C17C
tdf.qc_Avg()
# dfcc = tdf.reindex(tdf.summary.query('per_MSQ >0.8').index)
dfcc = tdf

# mdl = sutil.fit_BGM(dfcc)
# clu = tdf.setDF(mdl.model.predict(tdf))
# clu.columns=['clu']
# cluNew = clu


if 1:
    chipFile = '/home/feng/envs/Fig_PIF/\
chipTarg/182C/type=closest_bed=1505-27C-ZT0_S17_peaks_radius=1_feat=genes.gtf.cds_type=firstByKey.tsv'
    chipDF = pyutil.readData(chipFile)

    query = 'FC>6.0'
    chipDF[query] = chipDF.eval(query) 
    chipPeak = chipDF[[query]]
    chipPeak = chipPeak.reindex(tdf.index).fillna(False)
    chipPeak1 = scount.countMatrix(chipPeak,name='182C-S17_'+query)
    
    peak2gene = pyutil.readData('/home/feng/static/figures/1120__PIF7__peaks2genes/\
job_nearAUG__peak_diffBind--per-FC-GT-0dot9-182C-PIF7-radius=1__cutoff_4000__feat_genes.gtf.cds.tsv')
    peak2gene['per_FC'] = peak2gene.eval("@pyutil.dist2ppf(FC)")
    
#     peakInd = peak2gene.query('img==0 & per_FC>0.7').feat_acc.unique()
    peakInd = peak2gene.query('img==0 & FC>6.0 & distance < 3000').feat_acc.unique()
#     peakInd = peak2gene.query('img==0').feat_acc.unique()
    chipPeak = dfc.eval("index.isin(@peakInd)").to_frame()
    chipPeak2 = scount.countMatrix(chipPeak,name='DiffBind__peaks')
    
# dfcc = scount.countMatrix(dfcc)


# rnaseq_pif7col = scount.countMatrix(rnaseq_pif7col)
# rnaseq_pif7col.vlim=[-2,2]
rnaseq_pif7col_27C.qc_Avg();

# stats = pd.DataFrame(chipPeak)
stats = pd.concat([clu,
                   rnaseq_pif7col_27C.summary.get('MSQ')
                  ],axis=1)

cluTrack = spanel.fixCluster(clu)
tracks = [
    cluTrack,
    chipPeak1,
    chipPeak2,
    rnaseq_wt_27C17C,
    # rnaseq_pif727C_wt17C,
    rnaseq_pif7col_27C,
    keyDF[['BioName']],
    # rnaseq_pif4col_27C,
]

# np.save('tracks.npy',tracks)


figs = pyutil.collections.OrderedDict()

#### Add global heatmap
pp = spanel.panelPlot(tracks, figsize=[16,11], show_axa=1, showGrid=0)
pp.compile(index=dfcc.index,order = order,how='left')
fig = pp.render();
figs['rnaseq_heatmap'] = fig
pp.bigTable.to_csv('figData.csv')


#### add chip targets heatmap
pp = spanel.panelPlot(tracks, figsize=[14,12], show_axa=1, showGrid=0)
pp.compile(index=chipPeak1.index[chipPeak1.values.ravel()] & dfcc.index,
           order=order,how='left',
          )
fig = pp.render();
figs['rnaseq_chipPeak1'] = fig

#### add chip targets heatmap
pp = spanel.panelPlot(tracks, figsize=[14,12], show_axa=1, showGrid=0)
pp.compile(index=chipPeak2.index[chipPeak2.values.ravel()] & dfcc.index,
           order=order,how='left',
          )
fig = pp.render();
figs['rnaseq_chipPeak2'] = fig

##### add auxin cluster heatmap
pp = spanel.panelPlot(tracks, figsize=[14,12], show_axa=1, showGrid=0)
pp.compile(
    index=clu.query('clu==%d'%cluAuxin).index  & dfcc.index,
    order=stats,how='left',
)
fig = pp.render();
figs['rnaseq_auxinClu'] = fig

# if not DEBUG:
pyutil.render__images(figs,exts=['png','svg'])