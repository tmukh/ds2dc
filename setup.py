from setuptools import setup,find_packages
import os
import sys

with open('README.MD', encoding='utf-8') as f:
        long_description = f.read()
setup(
    name='DsToDc',
    version='0.5.1b',
    description='Data Conversion and Docker Image Generation Tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Tarik Abu Mukh',
    author_email='t_abu20@cs.uni-kl.de',
    url='https://github.com/tmukh',
    license='MPL-2.0',
    packages=find_packages(),
    install_requires=[
        find_packages()
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.6',
    ],
)