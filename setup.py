# coding=utf8


from setuptools import setup, find_packages

lib_classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Framework :: Django",
    "Framework :: Django :: 2.0",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
    'Operating System :: OS Independent'
]

setup(
    name='django-echarts',
    version='0.3.0',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/kinegratii/django-echarts',
    install_requires=['Django'],
    include_package_data=True,
    license='MIT',
    author='Kinegratii',
    author_email='kinegratii@gmail.com',
    description='A django app for Echarts integration with pyecharts as chart builder. ',
    classifiers=lib_classifiers
)
