import sys
import pymisca.header
import pymisca.ext as pyext
import matplotlib; matplotlib.use('agg') 
import matplotlib.pyplot as plt
from tree_worker import job_process,plotters
plt.rcParams['font.size'] = 14.
plt.rcParams['xtick.labelsize'] = 16.
plt.rcParams['axes.titlepad'] = 24.