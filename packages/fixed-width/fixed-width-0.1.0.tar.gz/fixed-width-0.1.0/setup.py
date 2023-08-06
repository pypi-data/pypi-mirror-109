# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['fixed_width']
setup_kwargs = {
    'name': 'fixed-width',
    'version': '0.1.0',
    'description': 'Working with fixed width types.',
    'long_description': '',
    'author': 'supakeen',
    'author_email': 'cmdr@supakeen.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/supakeen/fixed-width',
    'py_modules': modules,
}


setup(**setup_kwargs)
