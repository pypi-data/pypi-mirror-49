from setuptools import setup, find_packages

name             = 'lura'
version          = '0.3.17'
author           = 'eckso'
author_email     = 'eckso@eckso.io'
url              = 'https://github.com/ecks0/lura'
description      = 'syntactic sugar'

long_description              = open('README.md').read()
long_description_content_type = 'text/markdown'

python_requires  = ">= 3.6"
install_requires = open('requirements.txt').read().strip().splitlines()

setup(
  name = name,
  version = version,
  author = author,
  author_email = author_email,
  description = description,
  long_description = long_description,
  long_description_content_type = long_description_content_type,
  python_requires = python_requires,
  install_requires = install_requires,
  packages = find_packages(),
  include_package_data = True,
)
