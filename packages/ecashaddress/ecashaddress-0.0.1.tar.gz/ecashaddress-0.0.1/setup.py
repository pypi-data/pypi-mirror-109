import os
from distutils.core import setup
from setuptools import find_packages


def get_readme():
    """Returns content of README.md file"""
    dirname = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(dirname, "README.md")
    with open(filename, "r", encoding="utf-8") as fp:
        long_description = fp.read()
    return long_description


setup(name='ecashaddress',
      version='0.0.1',
      packages=find_packages(),
      description='Python library for converting cashaddr',
      url='https://github.com/PiRK/ecashaddress/',
      python_requires='>=3.7',
      keywords=['ecash', 'bcha', 'bitcoincash', 'bch', 'address', 'cashaddress', 'legacy', 'convert'],
      classifiers=[
          'Programming Language :: Python :: 3',
      ],
     # long_description=get_readme()
)
