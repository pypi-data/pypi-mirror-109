#!/usr/bin/env python

import os
from setuptools import setup

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='coffer_mac',
    packages=['coffer_mac'],
    version='0.1.1',
    description='Tiny Python API for performing MAC address lookups using Coffer.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/vesche/coffer_mac',
    author='Austin Jackson',
    author_email='vesche@protonmail.com',
    install_requires=['beautifulsoup4', 'requests'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Security',
    ]
)