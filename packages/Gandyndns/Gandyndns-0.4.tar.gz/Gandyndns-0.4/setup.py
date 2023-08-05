import sys
import os
from setuptools import setup

assert sys.version_info >= (3,0)

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "Gandyndns",
    version = "0.4",
    author = "Elie ROUDNINSKI",
    author_email = "xademax@gmail.com",
    description = ("Gandi dynamic ip updater."),
    license = "MIT",
    keywords = "gandi dyndns",
    url = "https://github.com/marmeladema/gandyndns",
    download_url = 'https://github.com/marmeladema/gandyndns/archive/0.4.tar.gz',
    packages=['gandyndns'],
    scripts=['scripts/gandyndns'],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=['requests', 'appdirs'],
    python_requires='>=3',
    data_files = [('share/gandyndns', ['sample.json'])],
)
