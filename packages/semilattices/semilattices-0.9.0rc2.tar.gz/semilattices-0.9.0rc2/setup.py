# semilattices
# Copyright (C) 2018-2019 
# Massachusetts Institute of Technology                    The University of Texas at Austin
# Uncertainty Quantification group                and      Center for Computational Geosciences and Optimization
# Department of Aeronautics and Astronautics               The Oden Institute for Computational Engineering and Sciences
# 
# Authors: Daniele Bigoni and Joshua Chen
# Contact: dabi@mit.edu / joshuawchen@utexas.edu
# Website: 
# Support:
#

import os
import os.path
import sys, getopt, re
from setuptools import setup, find_packages

global include_dirs
include_dirs = []

######################
# DEPENDENCIES
# (mod_name, use_wheel)
setup_requires = []
install_requires = [
    'future-fstrings',
    'numpy',
    'scipy',
    'six',
    'sortedcontainers',
]
opt_inst_req = {
    'PLOTTING': [
        'matplotlib',
        'networkx',
    ],
    'SPHINX': [
        'Sphinx',
        'sphinxcontrib-bibtex', 
        'sphinx-prompt',
        'robpol86-sphinxcontrib-googleanalytics',
        # 'sphinxcontrib-googleanalytics',
        'sphinxcontrib-contentui',
        'nbsphinx',
        'ipython', 
        'sphinx_rtd_theme', 
        'tabulate',
        'pandoc',
    ],
}

#################################
# WRITE requirements.txt files
with open('requirements.txt','w') as f:
    for r in install_requires:
        f.write(r+"\n")
f.close()
for opt in opt_inst_req:
    with open('requirements-'+opt+'.txt', 'w') as f:
        for r in opt_inst_req[opt]:
            f.write(r+"\n")
    f.close()

# Get version string
local_path = os.path.split(os.path.realpath(__file__))[0]
version_file = os.path.join(local_path, 'semilattices/_version.py')
version_strline = open(version_file).read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, version_strline, re.M)
if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (version_file,))

# Get optional pip flags
PIP_FLAGS = os.getenv('PIP_FLAGS')
if PIP_FLAGS is None:
    PIP_FLAGS = ''

setup(name = "semilattices",
      version = version,
      packages=find_packages(),
      include_package_data=True,
      url="https://semilattices.readthedocs.io/en/latest/",
      author = "Joshua Chen",
      author_email = "joshuawchen@utexas.edu",
      license="LGPLv3",
      description="",
      long_description=open("README.md").read(),
      include_dirs=include_dirs,
      setup_requires=setup_requires,
      install_requires=install_requires,
      zip_safe = False,         # I need this for debug purposes
      classifiers=[],
      test_suite='tests',
      )
