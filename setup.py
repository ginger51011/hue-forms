#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_descritiption = fh.read()

setup(
    name='hue_forms',
    version='1.0.1',
    author='Emil Jonathan Eriksson',
    author_email='eje1999@gmail.com',
    description='Control Philips Hue with Google Forms',
    long_description=long_descritiption,
    long_description_content_type="text/markdown",
    url="https://github.com/ginger51011/hue-forms",
    packages=find_packages(),
    entry_points = {
        "console_scripts": [
            "hue_forms = hue_forms.__main__:parse"
        ]
    },
    python_requires=">3.5.0",
    install_requires=[      # So that pip also installs required packages
        'requests',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib'
    ],
)
