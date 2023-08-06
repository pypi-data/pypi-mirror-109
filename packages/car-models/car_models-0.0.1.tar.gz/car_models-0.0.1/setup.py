from setuptools import setup, find_packages
import codecs
import os
VERSION = '0.0.1'
DESCRIPTION = 'This packages provides info about car_models.'
LONG_DESCRIPTION = 'Refer README.md'

# Setting up
setup(
    name='car_models',
    version=VERSION,
    author="Advait Shiralkar",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[''],
    keywords=['car', 'car models', 'car_models'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
