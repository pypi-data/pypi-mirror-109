#setup.py

from setuptools import setup

setup(
    name = "httpcase",
    version = "1.0.0",
    author = "Mr.K",
    author_email = "roseboy@live.com",
    description = ("HttpCase - api auto test tool."),
    url = "https://github.com/roseboy/httpcase",
    packages=['src'],
    entry_points={
        'console_scripts': ['hc=src.httpcase:main'],
    }
)