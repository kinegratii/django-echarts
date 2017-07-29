from setuptools import setup

lib_classifiers = [
    "Development Status :: 1 - Planning",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
]

setup(
    name='django-echarts',
    version='0.0.1',
    packages=['django_echarts'],
    url='https://github.com/kinegratii/django-echarts',
    license='MIT',
    author='Kinegratii',
    author_email='kinegratii@gmail.com',
    description='A echarts library for django based on chenjiandongx/pyecharts .'
)
