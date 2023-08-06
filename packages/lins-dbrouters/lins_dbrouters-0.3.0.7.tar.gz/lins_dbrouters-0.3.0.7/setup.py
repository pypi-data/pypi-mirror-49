#!/usr/bin/env python

import os
import sys
from distutils.core import setup
from setuptools import find_packages


def get_version():
    return open('version.txt', 'r').read().strip()

setup(
    author='Lucas Lehnen',
    author_email='lucas@lojaspompeia.com.br',
    description='Database routers para django rest framework.',
    license='MIT',
    name='lins_dbrouters',
    packages=find_packages(),
    url='https://bitbucket.org/grupolinsferrao/pypck-lins_dbrouters/',
    version=get_version()
)
