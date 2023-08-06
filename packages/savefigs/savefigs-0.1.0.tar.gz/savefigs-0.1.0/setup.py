# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['savefigs']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.0,<4.0']

setup_kwargs = {
    'name': 'savefigs',
    'version': '0.1.0',
    'description': 'Save all open Matplotlib figures',
    'long_description': '# savefigs\n\n[![CI workflow status](https://github.com/zmoon/savefigs/actions/workflows/ci.yml/badge.svg)](https://github.com/zmoon/savefigs/actions/workflows/ci.yml)\n[![Version on PyPI](https://img.shields.io/pypi/v/savefigs.svg)](https://pypi.org/project/savefigs/)\n\nThe goal is to make it easy to save all open Matplotlib figures, with names that are useful.\n\n## Usage\n\nAssume we have a script `some_script.py` that creates multiple Matplotlib figures.\n\nImport the `savefigs` function:\n```python\nfrom savefigs import savefigs\n```\n\nThe below examples assume the figures do not have a label (`fig.get_label()`, set using the `num` argument to `plt.figure()`).\nIf a figure does have a label, it will be used in place of `fig{N}`.\n\nDefault save settings:\n```python\nsavefigs()\n# ./some_script_fig1.png, ./some_script_fig2.png, ...\n```\n\nSpecify directory:\n```python\nsavefigs(save_dir="figs")  # must exist\n# ./figs/some_script_fig1.png, ./figs/some_script_fig2.png, ...\n```\n\nSpecify a prefix to the base stem format:\n```python\nsavefigs(stem_prefix="run1")\n# ./run1_fig1.png, ./run1_fig2.png, ...\n```\n\nSave in multiple file formats:\n```python\nsavefigs(formats=["png", "pdf"])\n# ./some_script_fig1.png, ./some_script_fig1.pdf, ...\n```\n\nAvoid overwriting files:\n```python\nsavefigs(clobber=False, clobber_method="add_num")\n```\n',
    'author': 'zmoon',
    'author_email': 'zmoon92@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zmoon/savefigs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
