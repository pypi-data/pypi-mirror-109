import setuptools

with open ("README.md", "r") as fh:
  long_description = fh.read ()

setuptools.setup (
  name='giseo',  
  version='1.0.0',
  scripts=[],
  author="Yaroslav Wigard",
  author_email="rsedrisev@yandex.ru",
  description="Giseo package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/wigarddev/giseo.py",
  packages=setuptools.find_packages (),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
 )