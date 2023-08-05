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


setup(
    name='Flask-Githubcard',
    version='1.0',
    url='https://flask-githubcard.2dogz.cn',
    license='MIT',
    author='jiangwei',
    author_email='qq804022023@gmail.com',
    description='generator a github card for flask web application',
    long_description=__doc__,
    py_modules=['flask_githubcard'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['Flask', 'Requests'],
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
