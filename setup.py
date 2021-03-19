from setuptools import setup, find_packages
from xpt import __version__

with open('LICENSE') as f:
    license = f.read()

setup(
    name='xperiaplaytools',
    version=__version__,
    description='Blah',
    author='soup-bowl',
    author_email='code@soupbowl.io',
    url='https://github.com/soup-bowl/XperiaPlay-Tools',
    license=license,
    packages=find_packages(exclude=('tests'))
)
