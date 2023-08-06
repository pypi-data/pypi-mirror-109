# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepthought3',
 'deepthought3..experiments',
 'deepthought3..experiments.audiomostly2014',
 'deepthought3..experiments.bcmi2015',
 'deepthought3..experiments.hamr2015',
 'deepthought3..experiments.ismir2014',
 'deepthought3..experiments.nips2014',
 'deepthought3..experiments.nips2014.scripts',
 'deepthought3..experiments.nips2014.templates.fftbins',
 'deepthought3..experiments.nips2014.templates.h0',
 'deepthought3..experiments.nips2014.templates.h1',
 'deepthought3..pylearn2ext',
 'deepthought3..pylearn2ext.costs',
 'deepthought3..pylearn2ext.monitor',
 'deepthought3.analysis',
 'deepthought3.analysis.tempo',
 'deepthought3.datasets',
 'deepthought3.datasets.eeg',
 'deepthought3.datasets.mpi2015',
 'deepthought3.datasets.openmiir',
 'deepthought3.datasets.openmiir.preprocessing',
 'deepthought3.datasets.rwanda2013rhythms',
 'deepthought3.mneext',
 'deepthought3.spearmint',
 'deepthought3.util']

package_data = \
{'': ['*'],
 'deepthought3..experiments.audiomostly2014': ['.ipynb_checkpoints/*'],
 'deepthought3..experiments.ismir2014': ['plots/*',
                                         'plots/.ipynb_checkpoints/*'],
 'deepthought3..experiments.nips2014': ['.ipynb_checkpoints/*'],
 'deepthought3.datasets.openmiir': ['notebooks/ERPs/*',
                                    'notebooks/beats/*',
                                    'notebooks/preprocessing/*']}

install_requires = \
['black>=21.5b2,<22.0',
 'librosa>=0.8.1,<0.9.0',
 'matplotlib>=3.4.2,<4.0.0',
 'mne>=0.23.0,<0.24.0',
 'openpyxl>=3.0.7,<4.0.0',
 'samplerate>=0.1.0,<0.2.0',
 'scikit-learn>=0.24.2,<0.25.0',
 'six>=1.16.0,<2.0.0',
 'watchdog>=2.1.2,<3.0.0',
 'xlrd>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'deepthought3',
    'version': '0.1.4',
    'description': 'a deep learning library for decoding brain activity',
    'long_description': None,
    'author': 'chanhakim',
    'author_email': 'chanhakim17@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
