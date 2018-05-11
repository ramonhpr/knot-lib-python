import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "knot",
    version = "0.1",
    author = "Ramon Ribeiro",
    author_email = "rhpr@cesar.org.br",
    description = ("API to access data from knot devices"),
    license = "BSD",
    keywords = "IoT dataAnalytics API web",
    url = "https://github.com/ramonhpr/knot-python-api",
    install_requires=['socketIO_client'],
    packages=find_packages(),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)