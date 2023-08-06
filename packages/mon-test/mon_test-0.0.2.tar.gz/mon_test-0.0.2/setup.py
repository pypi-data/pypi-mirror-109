from setuptools import setup, find_packages
import os
import mon_test

setup(name = 'mon_test',
version = mon_test.__version__,
author = 'Scyther',
author_email = 'leroy_mathieu@live.fr',
keywords = 'test packages',
classifiers = ['Topic :: Education'],
url='https://github.com/NewtonExpertise/test_pip.git',
packages = find_packages(),
description = 'test_ajout_pip',
long_description = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read(),
license = 'GPL V3',
plateformes = 'ALL',
)