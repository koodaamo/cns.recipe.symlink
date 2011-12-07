# -*- coding: utf-8 -*-
"""
This module contains the tool of cns.recipe.symlink
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.2.3'

long_description = (
    read('README.txt')
    + '\n' +
    'Contributors\n'
    '==============\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Change history\n'
    '================\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
   'Download\n'
    '==========\n')

entry_point = 'cns.recipe.symlink:Recipe'
entry_points = {"zc.buildout": ["default = %s" % entry_point]}

tests_require = ['zope.testing', 'zc.buildout']

setup(name='cns.recipe.symlink',
      version=version,
      description="",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Zope Public License',
        ],
      keywords='buildout',
      author='Radim Novotny, Petri Savolainen',
      author_email='novotny.radim@gmail.com, petri.savolainen@koodaamo.fi',
      url='http://github.com/koodaamo/cns.recipe.symlink',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['cns', 'cns.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout'
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite='cns.recipe.symlink.tests.test_docs.test_suite',
      entry_points=entry_points,
      )
