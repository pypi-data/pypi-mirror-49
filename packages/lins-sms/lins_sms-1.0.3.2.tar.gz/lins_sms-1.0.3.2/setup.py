#!/usr/bin/env python

import os
import sys
from distutils.core import setup
from setuptools import find_packages


def get_version():
    return open('version.txt', 'r').read().strip()

setup(
    author='Halyson Sampaio',
    author_email='halyson@lojaspompeia.com.br',
    description='Pacote de envio de sms',
    license='MIT',
    name='lins_sms',
    packages=find_packages(),
    url='https://bitbucket.org/grupolinsferrao/pypck-lins_sms/',
    version=get_version()
)

