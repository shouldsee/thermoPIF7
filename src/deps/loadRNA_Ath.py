'''
Loading datasets for PIF7
'''

from path import Path
with Path(__file__).realpath().dirname().dirname() as d:  
    # execfile('./header_import.py')
    import synotil.CountMatrix as scount
    import pymisca.util as pyutil

    meta  = pyutil.readData( 'deps/meta_rna.csv' )
    meta = meta.loc[~meta.index.isna()]
    keyDF = pyutil.readData( 'deps/key_ath.csv'  )
    rnaseq = pyutil.readData('deps/rnaseq_log2p1.pk')


    assert 'Age' in meta
    # execfile('/home/feng/meta/header_0903.py')

    # # meta  = pyutil.readData( 'deps/meta_rna.csv' )
    meta = pyutil.readData('/home/feng/meta/meta_rna.tsv')
    meta = meta.loc[~meta.index.isna()]

    # keyDF = pyutil.readData( 'deps/key_ath.csv'  )
    # rnaseq = pyutil.readData('deps/rnaseq_log2p1.pk')




    # meta = pyutil.readData('/home/feng/meta/meta_rna.tsv' )
    # rnaseq=  pyutil.readData('/home/feng/envs/Fig_PIF/1031__rnaseq__log2p1.pk')

    rnaseq = scount.countMatrix(rnaseq)
    rnaseq.qc_Avg()
    rnaseq = rnaseq.reindex(rnaseq.summary.query( 'per_M > 0.4' ).index)


    meta = meta.sort_values(['Age',
                             'gtype',
                             'ZTime_int',])

    mcurr = meta.query('SpecAcc=="Ath" & gtype == "Col" & runID=="185R"')
    m1 = mcurr.query('temp=="27C"')
    m2 = mcurr.query('temp=="17C"')
    mm = m1.reset_index().merge(m2.reset_index(),
                                on=['ZTime_int',],
                                how='inner',
                                sort=False)


    tdf = pyutil.init_DF(
        (rnaseq.reindex(columns = mm.DataAcc_x).values 
           - rnaseq.reindex(columns = mm.DataAcc_y).values ),
        
        rowName = rnaseq.index, colName = mm.DataAcc_x,)

    tdf = scount.countMatrix(tdf,colMeta=meta.reindex(mm.DataAcc_x))

    # tdf = scount.countMatrix(tdf)
    tdf.vlim = [-2,2]
    tdf.relabel('ZTime')
    tdf.name_ ='type=logFC_contrast=27C-17C_gtype=Col'
    rnaseq_wt_27C17C = tdf

    print(tdf.name)

    tdf.head(2)

    # tdf.columns

    rnaseq= scount.countMatrix(rnaseq)
    mcurr = meta.query('SpecAcc=="Ath" & temp == "27C"')
    m1 = mcurr.query('gtype=="pif7"')
    m2 = mcurr.query('gtype=="Col"')
    mm = m1.reset_index().merge(m2.reset_index(),on=['ZTime_int','Age'],how='inner',sort=True)


    tdf = pyutil.init_DF(
        (rnaseq.reindex(columns = mm.DataAcc_x).values 
         - rnaseq.reindex(columns = mm.DataAcc_y).values ),    
        rowName = rnaseq.index,colName = mm.DataAcc_x,)

    tdf = scount.countMatrix(tdf,colMeta=meta.reindex(mm.DataAcc_x))

    tdf.name_ = 'type=logFC_contrast=pif7-Col_temp=27C'
    tdf.relabel('ZTime')
    tdf.vlim = [-2,2]

    rnaseq_pif7col_27C = tdf

    # dfcc = tdf
    tdf.head(2)
    # tdf.columns

    mm.DataAcc_x

    rnaseq= scount.countMatrix(rnaseq)
    mcurr = meta.query('SpecAcc=="Ath"')
    m1 = mcurr.query('gtype=="pif7" & temp == "27C"')
    # m1 = mcurr.query('gtype=="pif7" & temp == "17C"')
    m2 = mcurr.query('gtype=="Col" & temp == "17C"')

    mm = m1.reset_index().merge(m2.reset_index(),on=['ZTime_int',],how='inner',sort=True)


    tdf = pyutil.init_DF(
        (rnaseq.reindex(columns = mm.DataAcc_x).values 
           - rnaseq.reindex(columns = mm.DataAcc_y).values ),
        
        rowName = rnaseq.index,colName = mm.DataAcc_x,)

    tdf = scount.countMatrix(tdf,colMeta=meta.reindex(mm.DataAcc_x))

    tdf.relabel('ZTime')
    rnaseq_pif7col = tdf
    # dfcc = tdf

    tdf = scount.countMatrix(tdf)
    tdf.name_ = 'type=logFC_contrast=pif7-Col_temp=27C-17C'
    tdf.vlim = [-2,2]
    rnaseq_pif727C_wt17C = tdf
    print(tdf.name)

    tdf.head(2)
    # tdf.columns

    meta = pyutil.readData('/home/feng/meta/meta_rna.tsv')
    meta = meta.loc[~meta.index.isna()]
    rnaseq= scount.countMatrix(rnaseq)
    mcurr = meta.query('SpecAcc=="Ath" & temp == "27C"')
    m1 = mcurr.query('gtype=="pif4-101"')
    m2 = mcurr.query('gtype=="col"')
    mm = m1.reset_index().merge(m2.reset_index(),on='ZTime_int',how='inner',sort=True)


    tdf = pyutil.init_DF(
        (rnaseq.reindex(columns = mm.DataAcc_x).values 
           - rnaseq.reindex(columns = mm.DataAcc_y).values ),
        
        rowName = rnaseq.index,colName = mm.DataAcc_x,)

    tdf = scount.countMatrix(tdf,colMeta=meta.reindex(mm.DataAcc_x))

    tdf.name_ = 'type=logFC_contrast=pif4-101-col_temp=27C'
    tdf.relabel('ZTime')
    tdf.vlim = [-2,2]

    rnaseq_pif4col_27C = tdf

    print(tdf.name)
    # dfcc = tdf
    tdf.head(2)
    # tdf.columns