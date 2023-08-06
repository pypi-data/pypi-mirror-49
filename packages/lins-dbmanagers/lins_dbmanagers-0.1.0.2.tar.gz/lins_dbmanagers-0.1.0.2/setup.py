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
    description='Managers com funcionalidades extras para os models Django.',
    license='MIT',
    name='lins_dbmanagers',
    packages=find_packages(),
    url='https://bitbucket.org/grupolinsferrao/pypck-lins_dbmanagers/',
    version=get_version()
)