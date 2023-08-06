import os
import sys
import atexit
import tarfile
from zipfile import ZipFile

from urllib import request
from setuptools import setup, find_packages
from setuptools.command.install import install

NAME = 'tomodapi'

MALLET_URI = 'http://mallet.cs.umass.edu/dist/mallet-2.0.8.tar.gz'
MALLET_FILE = 'mallet.tar.gz'

GLOVE_URI = 'http://nlp.stanford.edu/data/glove.6B.zip'
GLOVE_FILE = 'glove.zip'


def find_module_path():
    for p in sys.path:
        if os.path.isdir(p) and NAME in os.listdir(p):
            return os.path.join(p, NAME)


class PostInstallCommand(install):
    def run(self):
        atexit.register(self.download_mallet)
        atexit.register(self.download_glove)
        install.run(self)

    def download_mallet(self):
        main_dir = find_module_path()
        os.makedirs(main_dir, exist_ok=True)

        print('downloading mallet')
        request.urlretrieve(MALLET_URI, MALLET_FILE)
        print('extracting mallet')
        tar = tarfile.open(MALLET_FILE, "r:gz")
        tar.extractall(path=main_dir)
        tar.close()
        print('mallet installed')

        os.remove(MALLET_FILE)

    def download_glove(self):
        main_dir = os.path.join(find_module_path(), 'glove')
        os.makedirs(main_dir, exist_ok=True)

        print('downloading glove')
        request.urlretrieve(GLOVE_URI, GLOVE_FILE)
        print('extracting glove')
        with ZipFile(GLOVE_FILE, 'r') as file:
            file.extractall(path=main_dir)

        print('glove installed')

        os.remove(GLOVE_FILE)


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

required = []
extra_required = []
for r in requirements:
    if r.startswith('git'):
        extra_required.append(r)
    else:
        required.append(r)

setup(
    name=NAME,
    version='1.2',
    install_requires=required,
    data_files=[('txt', ['requirements.txt'])],
    py_modules=["tomodapi"],
    dependency_links=extra_required,

    # metadata to display on PyPI
    author='Pasquale Lisena',
    author_email='pasquale.lisena@eurecom.com',
    description='A framework for performing topic modelling',
    license="Apache 2.0",
    keywords='topic-model topic nlp',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    cmdclass={
        'install': PostInstallCommand,
    },
    url="https://github.com/D2KLab/ToModAPI",  # project home page, if any
    project_urls={
        'Bug Tracker': 'https://github.com/D2KLab/tomodapi/issues/',
        'Documentation': 'https://github.com/D2KLab/tomodapi/blob/master/README.md',
        'Source Code': 'https://github.com/D2KLab/tomodapi/',
    },
)
