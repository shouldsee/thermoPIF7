#!/usr/bin/env python
# -*- coding: utf-8 -*-

execfile('/home/feng/meta/header__script2figure.py')

##### PIF7 rnaseq-ptb
indVenn = pyutil.readData('/home/feng/static/figures/1126__PIF7__tempResp-AND-pif7Resp/Venn-index.csv')
indPIFresp = indVenn.ind2.dropna()

### PIF7 bound
url = 'http://172.26.114.34:81/static/figures/1119_PIF7_192C_A/job_nearAUG__peak_1505-Zt12-27C-S12-peaks-query=FC-GT-3dot2-radius=1_$
peak2gene =  pyutil.readData(url)
indCHIP = peak2gene.feat_acc.unique()

### deprre
# indCHIP=   pyutil.readData('/home/feng/envs/Fig_PIF/targ_rnaseqXchipseq.csv').ind1.dropna()

xlab = 'pif7Resp'
ylab = 'pif7Bound'
res = pyvis.qc_index(indPIFresp, indCHIP,xlab=xlab,ylab=ylab,silent=0)[0]
bed = peak2gene.set_index('feat_acc').loc[res.indAll.dropna()]
bed = bed[sdio.bedHeader[:-1]]
ofname = sutil.to_tsv(bed,'functionalPeaks.narrowPeak')
sutil.npk_expandSummit(ofname, radius=50,)

res.to_csv('Venn-index.csv')
figs['qc_Venn'] = plt.gcf()

# execfile('/home/feng/home/feng/envs/Fig_PIF/loadRNA_Ath.py')

execfile('/home/feng/meta/footer__script2figure.py')
