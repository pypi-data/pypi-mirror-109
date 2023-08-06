# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='gitlabui',
    version='1.0.4',
    author='batou9150',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'requests',
        'flask'
    ],
    description="Flask App over Gitlab Api to browse projects tags and to search into repository files",
    long_description=readme,
    long_description_content_type='text/markdown',
    url="https://github.com/batou9150/gitlabui",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
