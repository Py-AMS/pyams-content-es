#
# Copyright (c) 2015-2019 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""
This module contains PyAMS content ES package
"""
import os
from setuptools import setup, find_packages


DOCS = os.path.join(os.path.dirname(__file__),
                    'docs')

README = os.path.join(DOCS, 'README.rst')
HISTORY = os.path.join(DOCS, 'HISTORY.rst')

version = '2.2.1'
long_description = open(README).read() + '\n\n' + open(HISTORY).read()

tests_require = [
    'pyramid_zcml',
    'zope.exceptions'
]

setup(name='pyams_content_es',
      version=version,
      description="Elasticsearch integration package for PyAMS content",
      long_description=long_description,
      classifiers=[
          "License :: OSI Approved :: Zope Public License",
          "Development Status :: 4 - Beta",
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='Pyramid PyAMS',
      author='Thierry Florac',
      author_email='tflorac@ulthar.net',
      url='https://pyams.readthedocs.io',
      license='ZPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=[],
      include_package_data=True,
      package_data={'': ['*.zcml', '*.txt', '*.pt', '*.pot', '*.po', '*.mo',
                         '*.png', '*.gif', '*.jpeg', '*.jpg', '*.css', '*.js']},
      zip_safe=False,
      # uncomment this to be able to run tests with setup.py
      test_suite="pyams_content_es.tests.test_utilsdocs.test_suite",
      tests_require=tests_require,
      extras_require=dict(test=tests_require),
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'elasticsearch',
          'elasticsearch_dsl',
          'persistent',
          'pyams_catalog',
          'pyams_content >= 2.0.0',
          'pyams_elastic',
          'pyams_form >= 2.1.0',
          'pyams_i18n',
          'pyams_layer',
          'pyams_security',
          'pyams_sequence',
          'pyams_site',
          'pyams_skin',
          'pyams_table',
          'pyams_template',
          'pyams_thesaurus',
          'pyams_utils > 2.1.0',
          'pyams_viewlet',
          'pyams_workflow',
          'pyams_zmi',
          'pyams_zmq',
          'pyramid',
          'transaction',
          'zope.annotation',
          'zope.container',
          'zope.dublincore',
          'zope.interface',
          'zope.intid',
          'zope.lifecycleevent',
          'zope.schema'
      ],
      entry_points={
          'console_scripts': [
              'pyams_es_index = pyams_content_es.scripts:pyams_index_cmd'
          ]
      })
