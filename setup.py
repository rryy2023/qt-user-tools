#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包配置
使用PyInstaller打包为可执行文件
"""

from setuptools import setup, find_packages

setup(
    name="qiantu-tools",
    version="1.0.0",
    description="千图网问题解决工具",
    author="千图网",
    packages=find_packages(),
    install_requires=[
        "PyQt6>=6.6.0",
        "requests>=2.28.0",
        "beautifulsoup4>=4.11.0",
        "lxml>=4.9.0",
        "netifaces>=0.11.0",
    ],
    entry_points={
        "console_scripts": [
            "qiantu-tools=gui.main:main",
        ],
    },
)
