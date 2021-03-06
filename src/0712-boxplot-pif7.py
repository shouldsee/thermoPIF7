#!/usr/bin/env python
# BACKEND='GTK3Cairo'
# BACKEND='cairo'
BACKEND='agg'
NCORE = 10
import os
import simpleeval
import pymisca.ext as pyext
import synotil.CountMatrix as scount

import collections
from path import Path

from header_import import job_process,plotters
from short_header import job_process,plotters
import deps.loadRNA_Ath as rnadata
# from pymisca.plotters import 
# execfile(os.path.join( os.path.dirname(__file__),'header__import.py'))
figs = collections.OrderedDict()
DIR = Path(__file__).dirname()
import pymisca.jobs as pyjob

meta  = rnadata.meta
keyDF = rnadata.keyDF
rnaseq= rnadata.rnaseq

    
def get__dataset(key):
    return rnaseq[key]

def get__fcValues(s):
    sp = s.split('/')
    assert len(sp)==2,(s,sp)
    dats = map(get__dataset, sp)
    res = dats[0] - dats[1]
    return res

plots = [  
    plotters.boxplot(
        dict(
            comment='''
            This plot shows expression of a rnaseq-based group of synergistically expressed genes
            ''',
            OFNAME = "clu7-boxplot-1.svg",
            idnex=keyDF.index,
            datasets = [
                dict(label="Col-0_27C/17C_ZT8",
                    value=get__fcValues('185RS9/185RS8')),
                dict(label="pif7_27C/17C_ZT8",
                    value=get__fcValues('185RS23/185RS26')),
                dict(label="Col-0_27C/17C_ZT12",
                    value=get__fcValues('185RS12/185RS11')),
                dict(label="pif7_27C/17C_ZT12",
                    value=get__fcValues('185RS25/185RS4')),
            ],
            axis={
                "ylim":[-2,4],
                "ylabel":"logFC", 
                "figsize":[5,5]},

            ),{},),



   plotters.venn_diagram(dict(
    OFNAME = "venn-diagram-1.svg",
    comment = '''
    This plot shows overlap between 
        rna-based pif7-dependent genes
        and 
        rna-based temperature-dependent genes.        
    The selection criteria can be found in "src/0224_venn_pif7.py"
    ''',
    index1=pyext.readData(DIR/'0224_venn_pif7.py.result/Venn-index.csv')['ind1'],
    index2=pyext.readData(DIR/'0224_venn_pif7.py.result/Venn-index.csv')['ind2'],
    axis={
         "xlabel":"tempResponsive",
         "ylabel":"PIF7_Dependent",
    },
    ),{}),


   # plotters.venn_diagram(dict(
   #  OFNAME = "venn-diagram-2.svg",
   #  comment = '''
   #  This plot shows overlap between 
   #      rna-based pif7-responsive genes 
   #      and 
   #      chipseq-based PIF7-bound genes
   #  The selection criteria can be found in "???"
   #  ''',
   #  index1=pyext.readData(DIR/'0224_venn_pif7.py.result/Venn-index.csv')['ind1'],
   #  index2=pyext.readData(DIR/'0224_venn_pif7.py.result/Venn-index.csv')['ind2'],
   #  axis={
   #      "xlabel":"pif7_resp",
   #      "ylabel":"PIF7_bound",    
   #  },
   #  ),{}),




]
assert 0
d = '''
#### edit this to change plot features

[
    {
    "FUNCTION":"!{plotters.boxplot}",
    "OFNAME":"clu7-boxplot-1.svg",
    "index":"!{pyext.readData('/home/feng/static/results/0206__heatmap__PIF7/clu.csv').query('clu==7').index}",
    "datasets":[
        {"label": "Col-0_27C/17C_ZT8",
         "value": "!{get__fcValues('185RS9/185RS8')}",
        },
        {"label":"pif7_27C/17C_ZT8",
         "value": "!{get__fcValues('185RS23/185RS26')}",
        },        
        {"label": "Col-0_27C/17C_ZT12",
         "value": "!{get__fcValues('185RS12/185RS11')}",
        },
        {"label":"pif7_27C/17C_ZT12",
         "value": "!{get__fcValues('185RS25/185RS4')}",
        }
        ],
        "axis":{
            "ylim":[-2,4],
            "ylabel":"logFC", 
            "figsize":[5,5]

        #     ""
        }    
    },
    {
    "FUNCTION":"!{plotters.boxplot}",
    "OFNAME":"clu7-boxplot-2.svg",
    "index":"!{pyext.readData('/home/feng/static/results/0206__heatmap__PIF7/clu.csv').query('clu==7').index}",
    "datasets":[
        {"label": "Col-0_27C/17C_ZT8",
         "value": "!{get__fcValues('185RS9/185RS8')}",
        },
        {"label":"pif7_27C/17C_ZT8",
         "value": "!{get__fcValues('185RS23/185RS26')}",
        },        
        {"label": "Col-0_27C/17C_ZT12",
         "value": "!{get__fcValues('185RS12/185RS11')}",
        },
        {"label":"pif7_27C/17C_ZT12",
         "value": "!{get__fcValues('185RS25/185RS4')}",
        }
        ],
        "axis":{
            "ylim":[-2,4],
            "ylabel":"logFC", 
            "figsize":[5,5]

        #     ""
        }    
    },
    {
    "FUNCTION":"!{plotters.boxplot}",
    "OFNAME":"clu7-boxplot-1.svg",
    "index" : "!{pyext.readData('/home/feng/static/figures/1126__PIF7__tempResp-AND-pif7Resp/Venn-index.csv',)['ind2'].dropna()}",
    "datasets":[
        {"label": "Col-0_27C/17C_ZT8",
         "value": "!{get__fcValues('185RS9/185RS8')}",
        },
        {"label":"pif7_27C/17C_ZT8",
         "value": "!{get__fcValues('185RS23/185RS26')}",
        },        
        {"label": "Col-0_27C/17C_ZT12",
         "value": "!{get__fcValues('185RS12/185RS11')}",
        },
        {"label":"pif7_27C/17C_ZT12",
         "value": "!{get__fcValues('185RS25/185RS4')}",
        }
        ],
        "axis":{
            "ylim":[-2,4],
            "ylabel":"logFC", 
            "figsize":[5,5]

        #     ""
        }    
    },    
   {
    "FUNCTION":"!{plotters.venn_diagram}",
    "OFNAME":"venn-diagram-1.svg",
    "index1":"!{pyext.readData('/home/feng/static/figures/1126__PIF7__tempResp-AND-pif7Resp/Venn-index.csv',)['ind1']}",
    "index2":"!{pyext.readData('/home/feng/static/figures/1126__PIF7__tempResp-AND-pif7Resp/Venn-index.csv',)['ind2']}",
    "axis":{
        "xlabel":"tempResponsive",
         "ylabel":"PIF7_Dependent",
        "title":"Fisher exact test: p={pval}",
    }
    },
   {
    "FUNCTION":"!{plotters.venn_diagram}",
    "OFNAME":"venn-diagram-2.svg",
    "index1":"!{pyext.readData('/home/feng/static/figures/1126__PIF7__Venn__pif7Resp-AND-pif7SimpleBound/Venn-index.csv',)['ind1']}",
    "index2":"!{pyext.readData('/home/feng/static/figures/1126__PIF7__Venn__pif7Resp-AND-pif7SimpleBound/Venn-index.csv',)['ind2']}",
    "axis":{
        "xlabel":"pif7_resp",
         "ylabel":"PIF7_bound",
        "title":"Fisher exact test: p={pval}",
    }
    },    
]
'''
pyext.printlines([d],'all-plots.json')
d_s = simpleeval.EvalWithCompoundTypes().eval(d)
# d_s = d_s[-2:]
htmlLines=['<a href="./">Parent_Directory</a><br>',
          '<a href="all-plots.json">all-plots.json</a>']

if __name__ == '__main__':
	with (Path(__file__)+'.result').makedirs_p() as d:
		# res = map(job_process,d_s);
		htmlLines.extend(res)
		pyext.printlines(htmlLines,'figure.html')
	print('[INFO] results created in %s'%d.realpath())
