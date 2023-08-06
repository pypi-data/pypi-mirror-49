#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='mendelmd',
      version='1.1',
      packages=find_packages(),
      scripts=['bin/mendelmd'],
      install_requires=[
          'wheel',
          'django',
          'pysam',
          'cython'
      ],
      # entry_points={  # Optional
      #         'console_scripts': [
      #             'mendelmd=mendelmd.main:main',
      #         ],
      # },
      )
