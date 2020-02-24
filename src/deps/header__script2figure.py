DEBUG = 0

import matplotlib as mpl
mpl.use('agg')
execfile('/home/feng/meta/header_0903.py')
import synotil.jobs as sjob;reload(sjob)
import pymisca.jinja2_util as pyjin;reload(pyjin)
import sys
sys.stderr.write(sys.executable+'\n')
sys.stderr.write('\n'.join(sys.path))


figs = pyutil.collections.OrderedDict()

# bwMeta=meta = pyutil.readData('/home/feng/meta/meta_chip.tsv')
# rnaMeta = pyutil.readData('/home/feng/meta/meta_rna_prog.tsv')
# rnaMeta = rnaMeta.query('~index.duplicated()')
