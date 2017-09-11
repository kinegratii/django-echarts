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

packages = [
    'django_echarts',
    'django_echarts.management',
    'django_echarts.management.commands',
    'django_echarts.plugins',
    'django_echarts.templatetags',

]

setup(
    name='django-echarts',
    version='0.1.1',
    packages=packages,
    url='https://github.com/kinegratii/django-echarts',
    install_requires=['pyecharts', 'django', 'pluck'],
    include_package_data=True,
    license='MIT',
    author='Kinegratii',
    author_email='kinegratii@gmail.com',
    description='A echarts library for django based on chenjiandongx/pyecharts .'
)
