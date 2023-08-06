#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: LiangjunFeng
# Mail: zhumavip@163.com
# Created Time:  2018-4-16 19:17:34
#############################################

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name="python_example",      #这里是pip项目发布的名称
    version="0.0.1",  #版本号，数值大的会优先被pip
    keywords=("pip", "python", "example"),
    description="python example scripts",
    long_description="python example scripts",
    license="MIT Licence",

    url="https://github.com/",     #项目相关文件地址，一般是github
    author="linyin",
    author_email="showersh@163.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["django"]          #这个项目需要的第三方库
)