from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='hedron',
      version='0.0.3',
      description='A python package project for doing analysis on coordinates and clustering them.',
      long_description=long_description,
      author='Odos Matthews',
      author_email='odosmatthews@gmail.com',
      packages=['hedron'],
      intall_requires=['pandas', 'pygeodesy', 'staticmaps', 'range-key-dict'])

