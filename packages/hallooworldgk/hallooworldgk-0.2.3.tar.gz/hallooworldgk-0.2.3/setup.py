from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.2.3'
DESCRIPTION = 'A basic hello package'
LONG_DESCRIPTION = 'A basic hello package long desc'

# Setting up
setup(
    name="hallooworldgk",
    version=VERSION,
    author="Hew",
    author_email="<hew92932@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    url="https://github.com/",
    license="GPL 3",
    install_requires=['PyQt5', 'librosa'],
    keywords=['hello', 'world'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],

    entry_points =
    {   "console_scripts":
        [
            "halloo = libname:helloworld",
            "jahman = libname:jah"
        ]
    }

)