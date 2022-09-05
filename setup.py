#-*- coding: utf8 -*-

from setuptools import find_packages, setup

setup(
    name='auth-demo',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points = {
        'console_scripts': [
        ],
    },
    python_requires='>=3.7.7',
    install_requires=[
    ],
)