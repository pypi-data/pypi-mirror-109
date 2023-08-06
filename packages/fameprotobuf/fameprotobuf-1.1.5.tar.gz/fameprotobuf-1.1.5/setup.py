# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import fileinput
from setuptools import setup, find_packages
import xml.etree.ElementTree as ElementTree

__author__ = ["Christoph Schimeczek", "Ulrich Frey", "Marc Deissenroth-Uhrig", "Benjamin Fuchs", "Felix Nitsch"]
__copyright__ = "Copyright 2021, German Aerospace Center (DLR)"

__license__ = "Apache License 2.0"
__maintainer__ = "Felix Nitsch"
__email__ = "fame@dlr.de"
__status__ = "Production"

PACKAGE_DIR = "src/main/python/fameprotobuf/"


def readme():
    with open('README.md') as f:
        return f.read()


def generate_init():
    """Generates an empty `__init__.py` file in the `fameprotobuf` folder and passes if already existent"""
    try:
        file = open(PACKAGE_DIR + "__init__.py", "x")
        file.close()
    except FileExistsError:
        pass


def adapt_imports():
    """Changes imports in fameprotobuf from `import ...` to `from fameprotobuf import ...`"""
    for file_name in os.listdir(PACKAGE_DIR):
        with fileinput.FileInput(os.path.join(PACKAGE_DIR, file_name), inplace=True) as file:
            for line in file:
                if "import" in line and "_pb2" in line and "from fameprotobuf" not in line:
                    line = line.replace("import", "from fameprotobuf import")
                print(line, end='')


def ensure_version_compiled(version: str) -> None:
    """Ensures that in target/ folder a file ending with `version_string`.jar exists"""
    file_path = "./target/protobuf-" + version + ".jar"
    if not os.path.isfile(file_path):
        raise Exception("Could not find compiled java files for version '{}'. Compile project first!".format(version))


def get_version_from_pom() -> str:
    """Returns version from pom.xml"""
    pom = ElementTree.parse('pom.xml')
    version = pom.find('//{http://maven.apache.org/POM/4.0.0}version').text
    if not version:
        raise Exception("Could not extract version from pom.xml")
    else:
        print("Building for version number: " + version)
        return version


if __name__ == '__main__':
    version_string = get_version_from_pom()
    ensure_version_compiled(version_string)  # ToDo: build python sources with maven instead
    generate_init()
    adapt_imports()

    setup(name='fameprotobuf',
          version=version_string,
          description='Protobuf definitions converted to python classes for use in `fameio`',
          keywords=['FAME', 'agent-based modelling', 'fameio'],
          url='https://gitlab.com/fame-framework/fame-protobuf/',
          author=', '.join(__author__),
          author_email=__email__,
          license=__license__,
          package_dir={'': 'src/main/python'},
          packages=find_packages(where='src/main/python'),
          classifiers=[
              "Programming Language :: Python :: 3",
              "License :: OSI Approved :: Apache Software License",
              "Operating System :: OS Independent",
          ],
          install_requires=['protobuf'],
          zip_safe=False,
          python_requires='>=3.6',
          )
