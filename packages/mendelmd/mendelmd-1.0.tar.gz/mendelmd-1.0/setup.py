#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='mendelmd',
      version='1.0',
      packages=find_packages(),
      scripts=['manage.py', 'bin/mendelmd'],
      # entry_points={  # Optional
      #         'console_scripts': [
      #             'mendelmd=mendelmd.main:main',
      #         ],
      # },
      )
