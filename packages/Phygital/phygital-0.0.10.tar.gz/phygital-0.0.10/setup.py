# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 11:07:52 2019

@author: Innotechway
"""
import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="phygital",
    version="0.0.10",
    author="Renuka Angole",
    author_email="renuka.angole@gmail.com",
    description="A powerful package to work on IoT projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RenukaAngole1/phygital/tree/master/PhygitalLib/phygital",
    packages=setuptools.find_packages(),
    include_package_data=True,
    
    install_requires=["pyserial","requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
   
   
)