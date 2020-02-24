#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
'''

from path import Path
if __name__ =='__main__':


    DEBUG = 0

    import matplotlib as mpl
    mpl.use('agg')
    execfile('./header_import.py')
    import deps.loadRNA_Ath as rnaseq
    keyDF= rnaseq.keyDF
    figs = pyutil.collections.OrderedDict()


    with Path(__file__+'.result').makedirs_p().realpath() as d:

        stats = pd.DataFrame()

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

        # tempMarker = [
        #     'PIF7', 'YUC8'
        #              ]
        keyDFC = keyDF.query('BioName in @tempMarker')
        tdfc = tdf.reindex(keyDFC.index)
        # tdfc = sutil.meanNorm(tdfc)
        tdf.qc_Avg()
        prof = tdfc.T.mean(axis=1)

        #### calculate ranking score for each gene
        score = tdf.dot(prof.values)
        per_score= pyutil.dist2ppf(score)

        fig,axs = plt.subplots(1,3,figsize=[16,4])
        i = -1

        i+=1; ax=axs[i]; plt.sca(ax)
        tdfc.heatmap(vlim = [-2,2],ax=ax)

        i+=1; ax=axs[i]; plt.sca(ax)
        prof.plot(xticks = range(len(tdf.columns)),rot='vertical')

        i+=1; ax=axs[i]; plt.sca(ax)

        per_score = pd.Series(per_score, tdf.index)
        clu = per_score > 0.95

        xs,ys = tdf.summary.MSQ, score
        pyvis.qc_2var(xs,ys, axs=[None,ax, None,None], clu=clu, nMax=len(clu))
        pyvis.add_text(xs,ys,keyDF.BioName,ax=ax)
        figs['qc_TempReponse'] = fig

        stats['tempResponsive'] = clu


        tdf = rnaseq.rnaseq_pif7col_27C
        # tempMarker = ['ATHB2','YUC8']#
        keyDFC = keyDF.loc[ keyDF.BioName.isin(tempMarker) ]
        tdfc = tdf.reindex(keyDFC.index)
        # tdfc = sutil.meanNorm(tdfc)
        tdf.qc_Avg()
        prof = tdfc.T.mean(axis=1)

        score = tdf.dot(prof.values)
        per_score= pyutil.dist2ppf(score)

        fig,axs = plt.subplots(1,3,figsize=[16,4])
        i = -1

        i+=1; ax=axs[i]; plt.sca(ax)
        tdfc.heatmap(vlim = [-2,2],ax=ax)

        i+=1; ax=axs[i]; plt.sca(ax)
        prof.plot(xticks = range(len(tdf.columns)),rot='vertical')

        i+=1; ax=axs[i]; plt.sca(ax)

        # clu = tdf.eval('@per_score>0.975 & @tdf.summary.SD>0.75')
        # pyvis.qc_2var(tdf.summary.SD, score, axs=[None,ax, None,None], clu=clu)
        # clu = tdf.eval('@per_score>0.975 & @tdf.summary.per_MSQ>0.85')
        # clu = tdf.eval( 'index.isin(@tdf.sort_values("per_score").tail(500).index)')
        clu = tdf.eval("@per_score > 0.95")


        # clu = clu.to_frame('PIF7Dependent')
        xs,ys = tdf.summary.MSQ, score
        pyvis.qc_2var(xs,ys, axs=[None,ax, None,None], clu=clu, nMax=len(clu))
        pyvis.add_text(xs,ys,keyDF.BioName,ax=ax)

        stats['PIF7Dependent'] =clu
        # stats 

        # stats['PIF7

        figs['qc_PIF7Dependent'] = fig

        # stats = pd.concat([stats,clu],axis=1)
        # score.plot.scatter('per',0,ax=ax)
        # score.plot.
        # score['per']= pyutil.dist2ppf(score[0])

        xlab = 'tempResponsive'
        ylab = 'PIF7Dependent'
        res = pyvis.qc_index(stats.query(xlab).index, stats.query(ylab).index,silent=0,
                            xlab=xlab,ylab=ylab);

        figs['qc_Venn'] = plt.gcf()
        res[0].to_csv('Venn-index.csv')

        # from pandas.plotting import table

        # keyDF['isTarg'] =keyDF.eval('index.isin(@res[0].indAll)')
        keyDFC = keyDF.merge(stats,left_index=True,right_index=True)

        # fig,ax= plt.subplots(1,1,subplot_kw=dict(frame_on=False))
        ofname = 'markers.html'
        keyDFC.to_html(ofname)

        stats.to_csv('stats.csv')


        import pymisca.jinja2_util as pyjin
        import pymisca.util as pyutil
        def job__saveFig(
            figs,
            DIR,
            templateFile,
            exts = ['png',],
            dpi = 160,
            ):
            dfig = pyutil.saveFigDict(figs,
                                      DIR='.',
                                      exts=exts,
                                      dpi = dpi)
            dfig['fignames'] = [x for x in dfig['fignames'] if x.endswith('.png')]
            buf=[pyutil.ppJson(dfig)]
            ofname = 'figures.json'
            pyutil.printlines(buf,ofname)
            return dfig

        templateFile = '/home/feng/Templates/listImages.html'
        dfig = job__saveFig(figs, d, templateFile)
        ofname = pyjin.quickRender(templateFile,
                                   context=dfig,
                                   ofname= d / 'figure.html',
                                  )
        print ('[OUTPUT]',ofname)
