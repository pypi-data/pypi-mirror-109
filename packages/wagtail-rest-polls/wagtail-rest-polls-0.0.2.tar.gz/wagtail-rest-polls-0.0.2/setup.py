import os
from setuptools import setup, find_packages

import polls


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='wagtail-rest-polls',
    version=polls.__version__,
    description='A simple polls app for wagtail in django',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT License',
    author='jkearney126',
    author_email='josh.kearney@covalentcareers.com',
    url='https://github.com/covalentcareers/wagtail-polls',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django',
    ],
)