# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 09:59:41 2019

@author: guoyi
"""

from setuptools import setup

def readme_file():
    with open("README.rst",encoding="utf-8") as rf:
        return rf.read()

setup(name="gyte",version="1.0.1",description="This is a test library！",packages=["gyte"],py_modules=["Tool"],author="GuoYi",author_eamil="guoyigoo@gmail.com",long_description=readme_file(),url="https://github.com/")