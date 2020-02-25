import subprocess
import shutil
import glob
from path import Path
DIR = Path(__file__).dirname()
with (DIR / 'src').realpath() as d:
	for _d in d.glob("*.result"):
		shutil.rmtree(_d)
	SCRIPTS = '''
0224_venn_pif7.py
'''.strip().splitlines()
	for script in SCRIPTS:
		print('[RUNNING]%s'%script)
		res = subprocess.check_output(['python2', script,])
#	res = subprocess.check_output(['python2','0224_venn_pif7.py'])
	pass
pass
