from setuptools import setup

lib_classifiers = [
    "Development Status :: 3 - Alpha",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Framework :: Django",
    "Framework :: Django :: 1.8",
    "Framework :: Django :: 1.9",
    "Framework :: Django :: 1.10",
    "Framework :: Django :: 1.11",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
]

packages = [
    'django_echarts',
    'django_echarts.management',
    'django_echarts.management.commands',
    'django_echarts.plugins',
    'django_echarts.templatetags',
    'django_echarts.views',

]

setup(
    name='django-echarts',
    version='0.1.1',
    packages=packages,
    url='https://github.com/kinegratii/django-echarts',
    install_requires=['pyecharts', 'Django', 'pluck'],
    include_package_data=True,
    license='MIT',
    author='Kinegratii',
    author_email='kinegratii@gmail.com',
    description='A echarts library for django based on chenjiandongx/pyecharts .'
)
