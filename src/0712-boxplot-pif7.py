#!/usr/bin/env python
# BACKEND='GTK3Cairo'
# BACKEND='cairo'
BACKEND='agg'
NCORE = 10
import os
import simpleeval
import pymisca.ext as pyext
import pymisca.util as pyutil
import synotil.countMatrix as scount
from header_import import job_process,plotters
from path import Path
# from pymisca.plotters import 
# execfile(os.path.join( os.path.dirname(__file__),'header__import.py'))
figs = pyutil.collections.OrderedDict()



import pymisca.jobs as pyjob

# execfile('/home/feng/envs/Fig_PIF/loadRNA_Ath.py')
# execfile('/home/feng/meta/header_0903.py')
meta = pyutil.readData('/home/feng/meta/meta_rna.tsv')
keyDF = pyutil.readData('/home/feng/meta/key_ath.csv')
# if 'rnaseq' not in locals().keys():
rnaseq = pyutil.readData('/home/feng/envs/Fig_PIF/1031__rnaseq__log2p1.pk')
rnaseq = scount.countMatrix(rnaseq)
    
def get__dataset(key):
    return rnaseq[key]

def get__fcValues(s):
    sp = s.split('/')
    assert len(sp)==2,(s,sp)
    dats = map(get__dataset, sp)
    res = dats[0] - dats[1]
    return res

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
		res = map(job_process,d_s);
		htmlLines.extend(res)
		pyext.printlines(htmlLines,'figure.html')
	print('[INFO] results created in %s'%d.realpath())