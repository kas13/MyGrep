from setuptools import setup, find_packages
from os.path import dirname, join

setup(
    name='mygrep',
    version='1.1',
    include_package_data=True,
    packages=['files'],
    package_data={'':['app.py', 'mygrep.py']},
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    entry_points={
        'console_scripts':
            ['mygrep = files.app:main']
        }
)
