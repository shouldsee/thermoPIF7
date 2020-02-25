#!/usr/bin/env python
#from setuptools import setup
from distutils.core import setup
#import setuptools
import os,glob,sys
def parse_requirements(FILE = 'requirements.txt'):
    req = []
    dep = []
    for x in open(FILE,'r'):
      x = x.strip()
      if x.startswith("#"):
          pass
      elif "@" in x:
        req.append(x)
      return req,dep
required, dependency_links = parse_requirements()
print(required)
setup(
	name='thermoPIF7',
	version='0.0.1',
    packages=['.',],
	include_package_data=True,
	license='MIT',
	author='Feng Geng',
	author_email='shouldsee.gem@gmail.com',
	long_description=open('README.md').read(),
	# dependency_links=dependency_links,
  install_requires=[
    x.strip() for x in open("requirements.txt","r")
          if x.strip() and not x.strip().startswith("#")
  ],
	# install_requires=required,

)
