# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rt_pie',
 'rt_pie.rt_pie_lib',
 'rt_pie.rt_pie_lib.config',
 'rt_pie.rt_pie_lib.converters',
 'rt_pie.rt_pie_lib.metrics',
 'rt_pie.rt_pie_lib.metrics.unvoiced_detector',
 'rt_pie.rt_pie_lib.networks']

package_data = \
{'': ['*'], 'rt_pie': ['serialized_models/*']}

install_requires = \
['librosa>=0.8.0,<0.9.0',
 'matplotlib>=3.2,<3.3',
 'mir_eval>=0.6,<0.7',
 'numpy>=1.19,<1.20',
 'sounddevice>=0.4.1,<0.5.0',
 'tensorflow>=2.4.1,<3.0.0']

entry_points = \
{'console_scripts': ['rt_pie = rt_pie:main']}

setup_kwargs = {
    'name': 'rt-pie',
    'version': '0.1.15',
    'description': 'Real Rime PItch Estimator',
    'long_description': '# RT PIE<br>Real Time PItch Estimator\n\n[**pypi link**](https://pypi.org/project/rt-pie)\n\nTo demonstrate the predictions of the various models used throughout the thesis, a simple demonstration application was developed.\nThe demonstrator app is a python command line application. It comes pre-packaged with various deep learning models used in this thesis. The CREPE models as well as the DEEPF0_256 models are not available through this package, due to the 100MB package limitation on pypi.\n\nThe demonstrator app takes a WAVE audio file as input and saves a spectrogram including the pitch predictions to disk under the name `spectrogram.png`.\n\n## Installation\n\n    pip install rt_pie\n\n## Usage\n\n    rt_pie --help\n\n#### Authors\nKaspar Wolfisberg<br>\nLuca Di Lanzo\n\n',
    'author': 'Kaspar Wolfisberg',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wolfisberg/rt-pie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.8',
}


setup(**setup_kwargs)
