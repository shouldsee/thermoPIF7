
import sys
import pymisca.header as pyheader
pyheader.set__numpy__thread(locals().get('NCORE',None))
# if "matplotlib" not in sys.modules.keys():
pyheader.mpl__setBackend(locals().get('BACKEND','agg'))
# import matplotlib as mpl; mpl.use('Agg');
import synotil.dio as sdio;reload(sdio)
import synotil as synotil; reload(synotil)
import synotil.qcplots as pkg; reload(pkg)
import synotil.util as sutil;reload(sutil)
import synotil.PanelPlot as spanel;reload(spanel)
import synotil.CountMatrix as scount;reload(scount)
import synotil.jobs as sjob
import synotil.norm as snorm

import pymisca.ext as pyext
import pymisca.shell as pysh
import pymisca.util as pyutil; reload(pyutil)
import pymisca.vis_util as pyvis; reload(pyvis)
import pymisca.jobs as pyjob
import pymisca.callbacks as pycbk
import pymisca.proba 
import cPickle as pk
import funcy
import slugify


np = pyutil.np; pd = pyutil.pd
plt = pyutil.plt; 
if pyutil.hasIPD:
    get_ipython().magic('matplotlib inline')
    

#### pymisca/tree_worker.py    
import collections
_DICT_CLASS = collections.OrderedDict
import IPython
import simpleeval
import re
# def template__format(template, context=None):
#     functions = {'list':list}
# #     functions.update( simpleeval.DEFAULT_FUNCTIONS) 

#     if context is None:
#         context = pymisca.header.get__frameDict(level=1)
        
#     ob = IPython.utils.text.DollarFormatter()
#     res = ob.vformat(template,args=[],kwargs = context)
#     del context
#     return res

##### pymisca.header
import inspect
import pymisca.header
def get__frameDict(frame=None,level=0):
    '''
    if level==0, get the calling frame
    if level > 0, walk back <level> levels from the calling frame
    '''
    if frame is None:
        frame = inspect.currentframe().f_back

    for i in range(level):
        frame = frame.f_back
    context = frame.f_locals
    del frame
    return context
pymisca.header.get__frameDict = get__frameDict

##### pyext
def fig__save(fig,ofname, transparent = False, bbox_inches = 'tight',facecolor = None,
              **kwargs):
    if facecolor is None:
        facecolor = fig.get_facecolor()
    res = fig.savefig(ofname,
                bbox_inches=bbox_inches,
                transparent= transparent,
                facecolor=facecolor,
                **kwargs
               )
    return res
pyext.fig__save = fig__save

    
def template__format(template, context = None, formatResult= True):
    functions = {'list':list}
#     context['_CONTEXT'] = context
    functions.update( simpleeval.DEFAULT_FUNCTIONS) 
    functions.update(context)

    if context is None:
        context = pymisca.header.get__frameDict(level=1)
        
    ptn =  '([^{]?){([^}]+)}'
    class counter():
        i = -1

    def count(m):
        counter.i += 1
        return m.expand('\\1{%d}'%counter.i)
    
    s = template
    template = re.sub(ptn,string=s, repl= count)
    exprs = [x[1] for x in re.findall(ptn,s)]
    
    vals = map(simpleeval.EvalWithCompoundTypes(
#     vals = map(simpleeval.SimpleEval(
        names=context,
        functions=functions).eval,exprs)
#     if vals
        
    if len(vals)==1 and not formatResult:
        res = vals[0]
    else:
        res = template.format(*vals)
    del context
    return res


f = fformat = template__format
def worker__value__interpret(DB_WORKER, value,formatter=None, formatResult=False):
    if formatter is None:
        formatter = template__format
    if isinstance(value,basestring):
        _type = type(value)
        if value.startswith('!'):
            value = value[1:]
            value = formatter(value,context = dict(DB_WORKER=DB_WORKER,**DB_WORKER),
                             formatResult=formatResult)
            if isinstance(value,basestring):
                value = _type(value)

    return value

def worker__key__interpret(DB_WORKER, key):
    value = DB_WORKER[key]
    DB_WORKER[key] = value = worker__value__interpret(DB_WORKER,value)
    return value

def tree__worker__interpret(node, context):
    _this_func = tree__worker__interpret
    if isinstance(node,basestring):
        res = worker__value__interpret(context,node)
    elif isinstance(node,list):
        res = [_this_func(_node,context) for _node in node ]
    elif isinstance(node,dict):
        context = context.copy()
        context.update(node)
        res = _DICT_CLASS([(_key, _this_func( _node, context)) 
                          for _key, _node in node.iteritems()])
    else:
        res = node
        pass
#         assert 0,(type(node),)
    return res


def job_process(d,context=None):
    if context is None:
        context = pymisca.header.get__frameDict(level=1)
    _ = pyext.printlines([pyext.ppJson(d)],d['OFNAME']+'.json')
    d['FUNCTION'] = tree__worker__interpret(d['FUNCTION'],context)
    res = d['FUNCTION'](d,context) 
    return res
job__process = job_process

class plotters(object):
    @classmethod
    def html__tableLine(cls,OFNAME):
        res = '''<table style="width:auto; height="75%" border="1">
        <tr>
        <th>
        <a href="{OFNAME}">{OFNAME}</a>
        <br>
        <a href="{OFNAME}.json">{OFNAME}.json</a>
        </th>
        </tr>
        <tr>
            <th>
            <img src="{OFNAME}"></img>
            </th>
        </tr>
        </table>
        '''.format(OFNAME=OFNAME)    
        return res
    @classmethod
    def boxplot(cls,d,context):
        
        assert "get__fcValues" in context
        d = tree__worker__interpret(d,context)
        OFNAME = d.get('OFNAME',None) 
        assert OFNAME,(pyext.ppJson(d),)

        d_ax = d.get('axis',{})
        d_ax = cls.dict__castAxis(d_ax)
#         ylim = d_ax.get('ylim',[])
#         ylabel = d_ax.get('ylabel',None)
#         figsize = d_ax.get('figsize',None)

        fig, ax = plt.subplots(1,1,figsize=d_ax['figsize'])


        if d_ax['ylim']:
            ax.set_ylim(d_ax['ylim'])

        if d_ax['ylabel']:
            ax.set_ylabel(d_ax['ylabel'])

        # d['datasets'] = 
        res = [pd.Series(_d['value'],name=_d['label']) for _d in d['datasets']]
        res = pd.DataFrame(res).T
        d['_df'] = res
        import scipy.stats
        # .ttest_rel

        # INDEX_FILE = '/home/feng/static/figures/1126__PIF7__tempResp-AND-pif7Resp/Venn-index.csv'
        # pyext.MDFile('/home/feng/static/figures/1126__PIF7__tempResp-AND-pif7Resp/Venn-index.csv')
#         index : "!{pyext.readData('/home/feng/static/figures/1126__PIF7__tempResp-AND-pif7Resp/Venn-index.csv',)['ind2'].dropna()}"
        # index = pyext.readData('/home/feng/static/results/0206__heatmap__PIF7/clu.csv').query('clu==7').index
        # print len(index)
        df = d['_df']
        index = d.get('index',[])
        if len(index):
            df = df.reindex(index)
        # testResult = scipy.stats.ttest_rel(*df.values.T[:2])
        testResult = scipy.stats.ttest_ind(*df.values.T[:2])

        ax.set_title('''
        independent-t-test-between-two-leftmost-samples
        p={testResult.pvalue:.3E}
        N={df.shape[0]}
        '''.format(**locals()))
        df.boxplot(rot='vertical',ax=ax)
        
        pyext.fig__save(fig,OFNAME)
#         fig.savefig(OFNAME)
        res = cls.html__tableLine(OFNAME)

        return res
    
    @classmethod
    def dict__castAxis(cls, d_ax, context=None):
        res = dict(ylim = d_ax.get('ylim',[]),
            ylabel = d_ax.get('ylabel',None),
            xlabel = d_ax.get('xlabel',None),
            figsize = d_ax.get('figsize',None),
            title = d_ax.get('title',None),
                  )
        return res
    
    @classmethod
    def venn_diagram(cls,d,context):
        d = tree__worker__interpret(d,context)
        import pymisca.proba
        d_ax = cls.dict__castAxis(d.get('axis',{}))
        OFNAME = d.get('OFNAME',None) 
        assert OFNAME,(pyext.ppJson(d),)
        
        
        d['index1']= pd.Index(d['index1']).dropna()
        d['index2']= pd.Index(d['index2']).dropna()
        if d.get('index_bkgd',None) is not None:
            pass
        else:
            d['index_bkgd'] = d['index1'] | d['index2']
        d['index_bkgd'] = pd.Index(d['index_bkgd']).dropna()
        
#         d['title'] = d.get('title', "Fisher exact test: p={pval}")
        fig, ax = plt.subplots(1,1,figsize=d_ax['figsize'])

        testResult = pymisca.proba.index__getFisher(cluIndex=d['index1'], 
                                                    featIndex=d['index2'])
        pval = '%.3E'%testResult['p']
        ax= plt.gca()
        res = pyvis.qc_index(d['index1'],d['index2'],
                             xlab=d_ax['xlabel'],ylab=d_ax['ylabel'],silent=0,ax=ax);
        ax.set_title(d_ax['title'].format(**locals()))    
        
        cls.fig__save(fig,OFNAME)
        res = cls.html__tableLine(OFNAME)
        
        return res
    
    @classmethod
    def fig__save(cls,fig,OFNAME):
        return pyext.fig__save(fig,OFNAME)
plt.rcParams['font.size'] = 14.
plt.rcParams['xtick.labelsize'] = 16.
plt.rcParams['axes.titlepad'] = 24.