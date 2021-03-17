from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='xperiaplaytools',
    version='0.1.0',
    description='Blah',
    long_description=readme,
    author='soup-bowl',
    author_email='code@soupbowl.io',
    url='https://github.com/soup-bowl/XperiaPlay-Tools',
    license=license,
    packages=find_packages(exclude=('tests'))
)
