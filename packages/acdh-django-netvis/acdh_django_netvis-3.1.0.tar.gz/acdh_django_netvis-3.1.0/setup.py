#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='acdh_django_netvis',
    version="3.1.0",
    description="""App to visualize model objects as network graph""",
    long_description=readme + '\n\n' + history,
    author='Peter Andorfer',
    author_email='peter.andorfer@oeaw.ac.at',
    url='https://github.com/acdh-oeaw/acdh-django-netvis',
    packages=[
        'netvis',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=3.1',
    ],
    license="MIT",
    zip_safe=False,
    keywords='acdh_django_netvis',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
    ],
)
