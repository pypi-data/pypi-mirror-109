#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='Catkins_Dream',
    version="0.0.1",
    author='徐嘉志',
    author_email='X_jaguar@163.com',
    description=u'任生命烟花般绽放于夜空，似絮梦留过人间。旭日，东升',
    packages=find_packages(),
    url='https://blog.csdn.net/qq_43071318/article/details/109384574?spm=1001.2014.3001.5501',
    install_requires=[],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'Catkins_Dream=Catkins_Dream.out_interface:编译运行'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)