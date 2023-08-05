#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['telstar', 'telstar.com']

package_data = \
{'': ['*'], 'telstar': ['tests/*']}

install_requires = \
['redis', 'peewee']

setup(name='telstar',
      version='0.1.2',
      description='Telstar is a package to write producer and consumers groups against redis streams.',
      author='Bitspark',
      author_email='kai.koenig@bitspark.de',
      url='https://bitspark.de',
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      python_requires='>=3.6',
     )
