import sys
import pymisca.header as pyheader
import matplotlib; matplotlib.use('agg') 
import matplotlib.pyplot as plt

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