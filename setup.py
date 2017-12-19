# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


version = '0.1'

install_requires = [
    'setuptools',
    ]

tests_require = [
    'pytest',
    ]

transaction_requires = [
    'zope.interface',
    'transaction',
]

setup(name='cromlech.session',
      version=version,
      description="Cromlech server-side session components.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='Cromlech',
      author='The Dolmen team',
      author_email='dolmen@list.dolmen-project.org',
      url='http://gitweb.dolmen-project.org/',
      license='ZPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['cromlech',],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      install_requires=install_requires,
      extras_require={
          'test': tests_require,
          'transaction': transaction_requires,
      },
)
