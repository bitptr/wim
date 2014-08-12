#!/usr/bin/env python

# much of this is taken from https://github.com/novel/lc-tools
# by Roman Bogorodskiy

import os
import shutil
import subprocess
import sys

from setuptools import setup
from setuptools.command.install import install

def readme():
    with open('README.rst') as f:
        return f.read()

def abspath(path):
    """A method to determine absolute path
    for a relative path inside project's directory."""

    return os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), path))

class installer(install):
    def run(self):
        install.run(self)

        man_dir = abspath("./man/")

        output = subprocess.Popen([os.path.join(man_dir, "install.sh")],
                stdout=subprocess.PIPE,
                cwd=man_dir,
                env=dict({"PREFIX": self.prefix}, **dict(os.environ))).communicate()[0]
        print output


setup(name='wim',
      version='0.1',
      description='Keyboard controls for your WM',
      long_description=readme(),
      classifiers=[
      ],
      keywords='x wm repl shell',
      url='http://github.com/mike-burns/wim',
      author='Mike Burns',
      author_email='mike@mike-burns.com',
      license='BSD',
      packages=['wim'],
      entry_points={
          'console_scripts': ['wimsh = wim.wimsh:main'],
      },
      test_suite='nose.collector',
      tests_require=['nose'],
      requires=['pyparsing (==2.0.1)'],
      cmdclass={"install": installer},)
