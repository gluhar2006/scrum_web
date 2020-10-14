# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="scrum cards",
    description="Scrum cards service",
    packages=find_packages(exclude=["docs"]),
    zip_safe=False,
    install_requires=[
        'sanic',
        'jinja2',
    ],
)
