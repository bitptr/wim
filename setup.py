#!/usr/bin/env python

# much of this is taken from https://github.com/novel/lc-tools
# by Roman Bogorodskiy

import os
import subprocess

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
        install.do_egg_install(self)

        self._install_data("share/applications")
        self._install_data("man")

    def _install_data(self, directory):
        abs_d = abspath("./%s/" % directory)
        prefix = self.prefix
        if prefix is None:
            if self.user:
                home = os.getenv('HOME')
                prefix = "%s/.local" % home
            else:
                raise "Cannot figure out the prefix"
        output = subprocess.Popen([os.path.join(abs_d, "install.sh")],
                stdout=subprocess.PIPE,
                cwd=abs_d,
                env=dict({"PREFIX": prefix}, **dict(os.environ))).communicate()[0]
        print output


setup(name='wim',
      version='0.1',
      description='Keyboard controls for your WM',
      long_description=readme(),
      classifiers=[
      ],
      keywords='x wm repl shell',
      url='http://github.com/bitptr/wim',
      author='Mike Burns',
      author_email='mike@mike-burns.com',
      license='BSD',
      packages=['wim'],
      entry_points={
          'console_scripts': ['wim-gtk = wim.main:main'],
      },
      test_suite='nose.collector',
      tests_require=['nose'],
      install_requires=['pyparsing'],
      cmdclass={"install": installer},)
