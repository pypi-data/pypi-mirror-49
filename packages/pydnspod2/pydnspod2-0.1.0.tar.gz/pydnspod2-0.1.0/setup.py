#!/usr/bin/python
# coding=utf-8

from io import open
from setuptools import setup, find_packages
from pydnspod import __version__


setup(
    name='pydnspod2',
    version=__version__,
    description='pydnspod - a dnspod api sdk',
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    author='solos',
    author_email='lxl1217@gmail.com',
    maintainer='Harry Lee',
    maintainer_email='tclh123@gmail.com',
    url='https://github.com/tclh123/pydnspod',
    keywords=['DNSPod', 'DNS', 'SDK'],
    license="MIT License",
    platforms=["any"],
    packages=find_packages(exclude=['examples*', 'tests*']),
    include_package_data=True,
    zip_safe=False,
    install_requires=['six'],
)
