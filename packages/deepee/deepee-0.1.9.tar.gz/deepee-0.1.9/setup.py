# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepee']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'deepee',
    'version': '0.1.9',
    'description': 'Fast (and cheeky) differentially private gradient-based optimisation in PyTorch',
    'long_description': '# `deepee`\n\n`deepee` is a library for differentially private deep learning in PyTorch. More precisely, `deepee` implements the Differentially Private Stochastic Gradient Descent (DP-SGD) algorithm originally described by [Abadi et al.](https://arxiv.org/pdf/1607.00133.pdf). Despite the name, `deepee` works with any (first order) optimizer, including Adam, AdaGrad, etc. \n\nIt wraps a regular `PyTorch` model and takes care of calculating per-sample gradients, clipping, noising and accumulating gradients with an API which closely mimics the `PyTorch` API of the original model.\n\nCheck out the documentation [here](http://g-k.ai/deepee/)\n\n# For paper readers\nIf you would like to reproduce the results from our paper, please go [here](https://github.com/gkaissis/deepee/tree/results)',
    'author': 'Georgios Kaissis',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gkaissis/deepee',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
