#!/usr/bin/env python

import os
import sys
from distutils.core import setup
from setuptools import find_packages


def get_version():
    return open('version.txt', 'r').read().strip()

setup(
    author='Cristiano Lemos',
    author_email='cristianolemos@lojaspompeia.com.br',
    description='Execução de tarefas em segundo plano para django rest framework.',
    license='MIT',
    name='lins_tasks',
    packages=find_packages(),
    url='https://bitbucket.org/grupolinsferrao/pypck-lins_tasks/',
    version=get_version()
)
