"""
# coding:utf-8
@Time    : 2021/06/09
@Author  : jiangwei
@mail    : qq804022023@gmail.com
@File    : setup.py
@Desc    : setup
@Software: PyCharm
"""
from setuptools import setup
from os import path
from codecs import open

basedir = path.abspath(path.dirname(__file__))

with open(path.join(basedir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Flask-Githubcard',
    version='1.0.1',
    url='https://flask-githubcard.2dogz.cn',
    license='MIT',
    author='jiangwei',
    author_email='qq804022023@gmail.com',
    description='generator a github card for flask web application',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['flask_githubcard'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['Flask', 'Requests'],
    keywords='flask extension development',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
