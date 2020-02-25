#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Use RNASEQ data to derive genes that show PIF7-dependent expression
and temperature-dependent expression.
'''
DEBUG = 0
from file_tracer import FileTracer,InputFile,OutputFile  
from path import Path

import matplotlib as mpl; mpl.use('agg')
from pymisca.util import saveFigDict
import matplotlib.pyplot as plt
import pymisca.vis_util as pyvis

import pymisca.ext as pyext
import collections
import pandas as pd

#### data depdendency
from short_header import job_process
import deps.loadRNA_Ath as rnaseq
templateFile = InputFile('deps/Templates.listImages.html').realpath()
import jinja2


if __name__ =='__main__':

    keyDF= rnaseq.keyDF
    figs = collections.OrderedDict()
    scores = pd.DataFrame()
    stats = pd.DataFrame()


    with Path(__file__+'.result').makedirs_p().realpath() as d:


        ##############################################
        ###-------------------------------------------
        _ = '''
        For each gene derive its temperature responsiveness by
        calculating at its dot-product similarity with a set of
        marker genes using time-stratified logFC(27C/17C) profile
        '''
        tdf = rnaseq.rnaseq_wt_27C17C
        tempMarker = [
            'ATHB2',
            'ATHB4',
            'YUC8']

        keyDFC = keyDF.loc[keyDF.BioName.isin(tempMarker)]
        tdfc = tdf.reindex(keyDFC.index)
        tdf.qc_Avg()
        prof = tdfc.T.mean(axis=1)

        #### calculate ranking score for each gene
        score = tdf.dot(prof.values)
        per_score= pyext.dist2ppf(score)

        fig,axs = plt.subplots(1,3,figsize=[16,4])
        i = -1

        i+=1; ax=axs[i]; plt.sca(ax)
        tdfc.heatmap(vlim = [-2,2],ax=ax)

        i+=1; ax=axs[i]; plt.sca(ax)
        prof.plot(xticks = range(len(tdf.columns)),rot='vertical')

        i+=1; ax=axs[i]; plt.sca(ax)

        per_score = pd.Series(per_score, tdf.index)
        clu = per_score > 0.95



        ##### adding diagnostic plots
        xs,ys = tdf.summary.MSQ, score
        pyvis.qc_2var(xs,ys, axs=[None,ax, None,None], 
                clu=clu, nMax=len(clu))
        pyvis.add_text(xs,ys,keyDF.BioName,ax=ax)

        figs['qc_TempReponse'] = fig
        stats['tempResponsive'] = clu
        scores['tempResponsive'] = per_score
        ###-------------------------------------------
        ##############################################


        ##############################################
        ###-------------------------------------------
        _ = '''
        For each gene derive its PIF7-knockout responsiveness by
        calculating at its dot-product similarity with a set of
        marker genes using time-stratified logFC(pif7/wt) profile
        '''

        tdf = rnaseq.rnaseq_pif7col_27C
        keyDFC = keyDF.loc[ keyDF.BioName.isin(tempMarker) ]
        tdfc = tdf.reindex(keyDFC.index)
        # tdfc = sutil.meanNorm(tdfc)
        tdf.qc_Avg()
        prof = tdfc.T.mean(axis=1)

        score = tdf.dot(prof.values)
        per_score= pyext.dist2ppf(score)

        fig,axs = plt.subplots(1,3,figsize=[16,4])
        i = -1

        i+=1; ax=axs[i]; plt.sca(ax)
        tdfc.heatmap(vlim = [-2,2],ax=ax)

        i+=1; ax=axs[i]; plt.sca(ax)
        prof.plot(xticks = range(len(tdf.columns)),rot='vertical')

        i+=1; ax=axs[i]; plt.sca(ax)
        per_score = pd.Series(per_score, tdf.index)
        clu = pd.Series(per_score, tdf.index) > 0.95


        # clu = clu.to_frame('PIF7Dependent')
        xs,ys = tdf.summary.MSQ, score
        pyvis.qc_2var(xs,ys, axs=[None,ax, None,None], clu=clu, nMax=len(clu))
        pyvis.add_text(xs,ys,keyDF.BioName,ax=ax)

        figs['qc_PIF7Dependent'] = fig
        stats['PIF7Dependent']   = clu
        scores['PIF7Dependent'] = per_score
        ###-------------------------------------------
        ##############################################


        ##############################################
        ###-------------------------------------------
        _ = '''
        Venn diagram showing overlap between temperature-responsive gene
        and pif7ko-responsive genes
        '''
        xlab = 'tempResponsive'
        ylab = 'PIF7Dependent'
        res = pyvis.qc_index(stats.query(xlab).index, stats.query(ylab).index,silent=0,
                            xlab=xlab,ylab=ylab);

        figs['qc_Venn'] = plt.gcf()
        OF = OutputFile('Venn-index.csv')
        res[0].to_csv(OF)

        keyDFC = keyDF.merge(stats,left_index=True,right_index=True)
        ofname = OutputFile('markers.html')
        keyDFC.to_html(ofname)

        OF = OutputFile('stats.csv')
        stats.to_csv(OF)
        ###-------------------------------------------
        ##############################################


        ################ output figures  #############
        ###-------------------------------------------
        def job_saveFig(
            figs,
            DIR,
            templateFile,
            exts = ['png',],
            dpi = 160,
            ):
            templateFile = str(templateFile)
            dfig = saveFigDict(     figs,
                                      DIR='.',
                                      exts=exts,
                                      dpi = dpi)
            dfig['fignames'] = [x for x in dfig['fignames'] if x.endswith('.png')]
            buf=[pyext.ppJson(dfig)]
            ofname = 'figures.json'
            pyext.printlines(buf,ofname)
            return dfig
        dfig = job_saveFig(figs, d, templateFile)

        with open(OutputFile(d/'figure.html'),'w') as fo:
            buf = jinja2.Template(open(templateFile,'r').read()).render(**dfig)
            fo.write(buf)
        print ('[OUTPUT]',ofname)
        ###-------------------------------------------
        ##############################################
