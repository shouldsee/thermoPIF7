import pymisca.ext as pyext
import pandas as pd
import shutil
datasets_index = [
       u'syno1-001R-0-col', u'syno1-001R-1-col', u'syno1-001R-2-col',
       u'syno1-001R-3-col', u'syno1-001R-4-col', u'syno1-001R-5-col',
       u'2_24R_08-pif4-101', u'2_25R_08-pif4-101', u'2_26R_08-pif4-101',
       u'2_27R_08-pif4-101', u'2_28R_08-pif4-101', u'2_29R_08-pif4-101',
       u'2_30R_08-pif4-101', u'2_31R_08-pif4-101', 
       u'185RS3', u'185RS6',
       u'185RS2', u'185RS8', u'185RS11', u'185RS15', u'185RS18', u'185RS21',
       u'185RS1', u'185RS5', u'185RS9', u'185RS12', u'185RS14', u'185RS17',
       u'185RS20', u'185RS22', u'185RS24', u'185RS26', u'185RS4', u'185RS7',
       u'185RS10', u'185RS13', u'185RS16', u'185RS19', u'185RS23', u'185RS25',
       u'185RS27', u'185RS28']       



{
       'header_import.py':'import packages',
       'deps/key_ath.csv':'information of key genes of interest',
       'deps/meta_rna.csv':'meta information for the concerning RNA experiemnt',
       'deps/rnaseq_log2p1.pk': 'RNASEQ count table /home/feng/envs/Fig_PIF/1031__rnaseq__log2p1.pk'
}

OF = 'deps/meta_rna.csv'
IF = '/home/feng/meta/meta_rna.tsv' 
df = pyext.readData(IF,guess_index=1)
df = df.loc[~df.index.isna()]
df.reindex(datasets_index).to_csv(OF)
print(OF)


OF = 'deps/key_ath.csv'
IF = '/home/feng/meta/key_ath.csv'  
with open(OF,'w') as f:
       f.write(open(IF,'r').read())
print(OF)

OF = 'deps/rnaseq_log2p1.pk'
IF = '/home/feng/envs/Fig_PIF/1031__rnaseq__log2p1.pk'
shutil.copy2(IF,OF)
print(OF)
