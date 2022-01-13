# coding=utf8

import pathlib
import re

from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent
txt = (here / 'django_echarts' / '__init__.py').read_text()
__version__ = re.findall(r"^__version__ = '([^']+)'\r?$", txt, re.M)[0]

lib_classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3 :: Only",
    "Framework :: Django",
    "Framework :: Django :: 2.0",
    "Framework :: Django :: 2.1",
    "Framework :: Django :: 2.2",
    "Framework :: Django :: 3.0",
    "Framework :: Django :: 3.1",
    "Framework :: Django :: 3.2",
    "Framework :: Django :: 4.0",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
    'Operating System :: OS Independent'
]

setup(
    name='django-echarts',
    version=__version__,
    packages=find_packages(exclude=['tests']),
    url='https://github.com/kinegratii/django-echarts',
    include_package_data=True,
    license='MIT',
    author='kinegratii',
    author_email='kinegratii@gmail.com',
    description='A django app for Echarts integration with pyecharts as chart builder. ',
    classifiers=lib_classifiers,
    install_requires=['borax~=3.5']
)
