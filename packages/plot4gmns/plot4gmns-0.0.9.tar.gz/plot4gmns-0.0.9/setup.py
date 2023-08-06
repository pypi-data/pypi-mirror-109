# -*- coding: utf-8 -*-
# @Time    : 2021/4/16 19:35
# @Author  : CZY
# @File    : setup.py
# @Software: PyCharm
import setuptools
setuptools.setup(
    name='plot4gmns',
    version='0.0.9',
    author='Dr.Junhua Chen, Zanyang Cui',
    author_email='cjh@bjtu.edu.cn, zanyangcui@outlook.com',
    url='https://github.com/PariseC/plot4gmns',
    description='An open-source academic research tool for visualizing multimodal networks for transportation system modeling and optimization',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license='Apache License 2.0',
    packages=['plot4gmns'],
    python_requires=">=3.6.0",
    install_requires=['pandas', 'shapely','numpy','seaborn','matplotlib <=3.3.0','scipy','chardet'],
    classifiers=['License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python :: 3']
)
