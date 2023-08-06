#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################

# File Name: setup.py

# Author: jianzhihua

# Mail: jianzhihua@woodcol.com

# Created Time: 2021-06-04 14:17:34

#############################################
from os import path as os_path
from setuptools import setup, find_packages
import common_extractor
curr_dir = os_path.abspath(os_path.dirname(__file__))


# 读取文件内容
def read_file(filename):
    with open(os_path.join(curr_dir, filename)) as f:
        long_description = f.read()
    return long_description


# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]

setup(
    name='common_extractor',  # 包名
    python_requires='>=2.7.9', # python环境
    version=common_extractor.__version__, # 包的版本
    description="common table or text extractor",  # 包简介，显示在PyPI上
    long_description=read_file('README.md'), # 读取的Readme文档内容
    long_description_content_type="text/markdown",  # 指定包文档格式为markdown
    author="jianzhihua", # 作者相关信息
    author_email='jianzhihua@datagrand.com',
    url='https://github.datagrand.com',
    # 指定包信息，还可以用find_packages()函数
    packages=[
        'common_extractor',
        'common_extractor.table_common_extract',
        'common_extractor.text_common_extract'
    ],
    install_requires=read_requirements('requirements.txt'),  # 指定需要安装的依赖
    include_package_data=True,
    license="MIT",
    keywords=['extractor', 'table', 'text'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.9'
    ],
)

