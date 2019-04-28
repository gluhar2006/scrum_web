# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="scrum cards",
    description="Scrum cards service",
    packages=find_packages(exclude=["docs"]),
    zip_safe=False,
    install_requires=[
        'flask-socketio==3.2.2',
        'gevent-websocket==0.10.1',
    ],
)
