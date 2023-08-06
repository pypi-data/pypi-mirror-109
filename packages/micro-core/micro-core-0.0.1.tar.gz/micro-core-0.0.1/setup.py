#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from pathlib import Path
from setuptools import setup, find_packages

# 说明文档
readme = Path.cwd().joinpath('LETSGO.md').open().read()

# CLI命令
script = ['micro=micro_core.cli.main:main']

# 安装描述
setup(
    name='micro-core',
    version='0.0.1',
    author='limanman',
    long_description=readme,
    url='https://github.com/micro-org/',
    license='Apache License, Version 2.0',
    long_description_content_type='text/markdown',
    install_requires=[
        'typing==3.7.4.3',
        'eventlet==0.31.0',
    ],
    entry_points={'console_scripts': script},
    packages=find_packages(exclude=['test', 'test.*']),
)
