from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

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
      tests_require=['nose'])
