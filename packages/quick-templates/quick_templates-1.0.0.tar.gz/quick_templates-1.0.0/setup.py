# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['quick_templates']
setup_kwargs = {
    'name': 'quick-templates',
    'version': '1.0.0',
    'description': 'quickly create templates on Pug, Twig, Blade',
    'long_description': None,
    'author': 'matyukov stas',
    'author_email': 'matyukov_stas@mail.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
