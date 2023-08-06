from setuptools import setup, find_packages
from os import path
from io import open
here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='imagestoanimation',
    version='0.1.0',
    description="Converts a series of images to an animation using OpenCV",

    long_description=long_description ,
    long_description_content_type="text/markdown" ,

    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
    ],

    packages=find_packages(),

    install_requires=[
        'opencv-python (>=4.1,<5.0)',
        'configargparse (>=0.14.0,<0.15.0)',
    ],

    include_package_data=True,
)
