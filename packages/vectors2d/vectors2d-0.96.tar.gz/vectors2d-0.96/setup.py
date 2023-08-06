import setuptools
from distutils.core import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'vectors2d',
  packages = setuptools.find_packages(),
  version = '0.96',
  license='MIT',
  description = 'Small module to work with vectors in 2 dimensions. Allows natively add, subtract, multiply vectors and many more.',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Dmitry Popov',
  author_email = 'thedmitryp@ukr.net',
  url = 'https://github.com/MitryP/vectors',
  download_url = 'https://github.com/MitryP/vectors/archive/0.96.tar.gz',
  keywords = ['vectors', '2-dimensional', 'flat', 'coordinates', 'open-source'],
  install_requires=[],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)