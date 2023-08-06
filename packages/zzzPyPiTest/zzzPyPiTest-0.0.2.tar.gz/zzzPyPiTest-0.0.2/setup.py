#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='zzzPyPiTest',
    version='0.0.2',
    author='zhaozizhe',
    author_email='214839648@qq.com',
    url='https://github.com/namezzz/PO-DRL',
    description=u'pypi测试',
    packages=['test'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'helloTest=test:hello',
            'version=test:version'
        ]
    }
)