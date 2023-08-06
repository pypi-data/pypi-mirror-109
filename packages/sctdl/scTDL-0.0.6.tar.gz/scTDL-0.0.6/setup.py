# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deeptl', 'deeptl.plotting', 'deeptl.preprocessing', 'deeptl.tools']

package_data = \
{'': ['*']}

install_requires = \
['anndata>=0.7.5',
 'h5py>=2.9.0',
 'numba>=0.41.0',
 'numpy>=1.17.0',
 'pandas>=1.0',
 'scikit-learn>=0.21.2',
 'torch>=1.7.0',
 'tqdm>=4.56.0']

setup_kwargs = {
    'name': 'sctdl',
    'version': '0.0.6',
    'description': '',
    'long_description': '# DeepTL_dev\n\n### Version: 0.0.6_dev\n\n0.0.1_dev update: integrate deeptl with anndata\n\n0.0.2_dev update: support pyscenic regulons\n\n0.0.3_dev update: support large scale data analysis\n\n0.0.4_dev update: support random state\n\n0.0.5_dev update: support trajectory draw graph\n\n0.0.6_dev update: integrate scanpy pca\n\n\n\n\n\n\n\n\n\n',
    'author': 'Lequn Wang',
    'author_email': 'wlq762@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0',
}


setup(**setup_kwargs)
