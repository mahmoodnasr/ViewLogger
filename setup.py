import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='ViewLogger',
    version='1.6.1',
    packages=find_packages(exclude=['docs','tests*']),
    include_package_data=True,
    license='MIT',
    description='Log view hits over time so that you know who enter this view and when.',
    long_description=README,
    url='https://github.com/mahmoodnasr/ViewLogger/',
    author='Mahmood Nasr',
    author_email='mahmood.nasr.fcis@gmail.com',
classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

