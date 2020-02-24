if 'debug' in locals().keys():
    DEBUG= int(debug)
else:
    DEBUG=0
    
if not DEBUG:
    import pymisca.jinja2_util as pyjin
    import pymisca.util as pyutil
    
    lc = locals()
    defaults = {
        'templateFile':'/home/feng/Templates/listImages.html',
        'DIR':'.',
        'exts':['png',],
    }
    for k,v in defaults.items():
        if k in ['DIR']:
            lc[k] = v
        else:
            lc.setdefault(k,v)
    if 'dpi' not in locals().keys():
        dpi = 160 
        
    def job__saveFig(figs):
        dfig = pyutil.saveFigDict(figs,
                                  DIR='.',
                                  exts=exts,
                                 dpi = dpi)
        dfig['fignames'] = [x for x in dfig['fignames'] if x.endswith('.png')]
        buf=[pyutil.ppJson(dfig)]
        ofname = 'figures.json'
        pyutil.printlines(buf,ofname)
        return dfig
    dfig = job__saveFig(figs)
#     dfig = pyutil.saveFigDict(figs,DIR=DIR,exts=['png','svg'])
#     dfig = pyutil.saveFigDict(figs,
#                               DIR=DIR,
#                               exts=exts)
#     dfig['fignames'] = [x for x in dfig['fignames'] if x.endswith('.png')]
#     buf=[pyutil.ppJson(dfig)]
#     pyutil.printlines(buf,'figures.json')
    ofname = pyjin.quickRender(templateFile,
                               context=dfig,
                               ofname=DIR+'/figure.html',
                              )
    print ('[OUTPUT]',ofname)