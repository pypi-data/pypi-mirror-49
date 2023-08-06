#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2019, Matjaž Guštin <dev@matjaz.it> <https://matjaz.it>.
# Released under the BSD 3-Clause License

"""Package setup for the Rangeforce library."""

from distutils.core import setup

# noinspection PyUnresolvedReferences
import setuptools

setup(
    name='Rangeforce',
    version='1.0.0',
    description='Developer-friendly range checks with user-friendly error '
                'messages',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Matjaž Guštin',
    author_email='dev@matjaz.it',
    url='https://github.com/TheMatjaz/Rangeforce',
    license='BSD',
    py_modules=[
        'rangeforce',
    ],
    keywords=[
        'range',
        'domain',
        'limited',
        'validation',
        'user-input',
        'friendly',
        'understandable',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3',
)
