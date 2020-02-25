#!/usr/bin/env python
# -*- coding: utf-8 -*-
# execfile("/home/feng/meta/header__peakBW.py",)

# execfile('/home/feng/meta/header__script2figure.py')
import collections
import synotil.dio as sdio
import synotil.util as sutil
import synotil.jobs as sjob
import matplotlib.pyplot as plt
import pymisca.util as pyutil
import pymisca.ext as pyext

figs = collections.OrderedDict()
peakFile = '/home/feng/envs/Fig_PIF/type=closest_bed=1505-17C-ZT16_S16_peaks_radius=1_feat=genes.gtf.cds_chipTarg.tsv'

###### Cutoff by FC
bwSingle = bwMeta.loc['186CS12']
FC_CUTOFF = 3.25
query = 'FC>%.1f' % FC_CUTOFF

peakFile = bwSingle.npkFile
bed = sdio.extract_peak(peakFile)
bed['per_FC'] = bed.eval('@pyutil.dist2ppf(FC)')
# bed.query('per_FC')
bed.plot.scatter('per_FC','FC')
plt.title(query)
plt.grid(1)
figs['FC_cutoff']=plt.gcf()

ofname = pyutil.queryCopy(infile=bwSingle.npkFile,query=query,inplace=0,reader=sdio.extract_peak)
peakFile = ofname

#### map to genes
featFile ='/home/feng/ref/Arabidopsis_thaliana_TAIR10/annotation/genes.gtf.cds'
GSIZE ='/home/feng/ref/Arabidopsis_thaliana_TAIR10/genome.sizes'
peakSummit = sutil.npk_expandSummit(fname=peakFile,radius=1)
peak2geneFile = sutil.job__nearAUG(peakSummit=peakSummit,
                                   featFile=featFile,
                                   GSIZE=GSIZE,
                                   CUTOFF=3500,
                                   peakWid=1)

# peakFile = pyutil.os.path.realpath(peakFile)
# midx = '''
# 189CS10
# 189CS11
# 189CS16
# 189CS17
# '''.strip().splitlines()
bwCurr = bwMeta.query('runID=="192C" & bname.str.contains("PIF7")')
# print (peakFile)




print('[peakFile]',peakFile)
print (pyutil.lineCount(peakFile))

testDict = dict(
    outerRadius=500,
    # innerRadius = 50,
    center_summit = 0,
    NCORE = 4,
    peakFile = peakFile,
# outIndexFunc = pyutil.basename,
# stepSize= 10,
bwFiles = bwCurr.fname)
figs.update(sjob.figs__peakBW(**testDict)[0])


# dfig = pyutil.saveFigDict(figs,DIR=DIR)
# buf=[pyutil.ppJson(dfig)]
# pyutil.printlines(buf,'figures.json')
# ofname = pyjin.quickRender(templateFile,
#                            context=dfig,
#                            ofname=DIR+'/figure.html',
#                           )
# print ('[OUTPUT]',ofname)
# execfile('/home/feng/meta/footer__script2figure.py')

### for testing
# assert 0 