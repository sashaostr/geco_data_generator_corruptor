#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from pkg_resources import resource_string, resource_listdir

from distutils.core import setup


exec(compile(open('geco_data_generator_corruptor/__init__.py').read(),
                  'geco_data_generator_corruptor/__init__.py', 'exec'))

setup(name='geco_data_generator_corruptor',
      version=__version__,
      description='data generator and corruptor originaly created by Peter Christen et al.',
      maintainer='sashaostr (Alexander Ostrikov)',
      maintainer_email='sasha.ostrikov@verint.com',
      # url='https://github.com/sashaostr/datasu.git',
      packages=find_packages(),#['geco_data_generator_corruptor'],
      package_data={'':['*.csv']},
      # keywords=['data science', 'utils', 'pandas', 'sklearn'],
      install_requires=[
      ],
      # tests_require=['pytest', 'mock'],
      # cmdclass={'test': PyTest},
      )