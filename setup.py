# coding=utf8

from setuptools import setup, find_packages

from django_echarts import __version__, __author__

lib_classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3 :: Only",
    "Framework :: Django",
    "Framework :: Django :: 1.11",
    "Framework :: Django :: 2.0",
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
    author=__author__,
    author_email='kinegratii@gmail.com',
    description='A django app for Echarts integration with pyecharts as chart builder. ',
    classifiers=lib_classifiers,
    install_requires=['borax']
)
