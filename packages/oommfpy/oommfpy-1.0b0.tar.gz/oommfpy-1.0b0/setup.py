# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oommfpy', 'oommfpy.tools']

package_data = \
{'': ['*'], 'oommfpy.tools': ['clib/*', 'clib/tmp/*']}

install_requires = \
['Cython>=0.29.23,<0.30.0',
 'click>=7.1,<8.0',
 'matplotlib>=3.3.4,<4.0.0',
 'numpy>=1.20.3,<2.0.0',
 'scipy>=1.6.3,<2.0.0']

entry_points = \
{'console_scripts': ['omf2vtk = oommfpy.tools.omf2vtk:omf2vtk_cli',
                     'plot_omf = '
                     'oommfpy.tools.plot_slices:plot_omf_slices_cli']}

setup_kwargs = {
    'name': 'oommfpy',
    'version': '1.0b0',
    'description': 'Minimal Python lib to process OOMMF format output files',
    'long_description': None,
    'author': 'David Cortés-Ortuño',
    'author_email': 'd.i.cortes@uu.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
