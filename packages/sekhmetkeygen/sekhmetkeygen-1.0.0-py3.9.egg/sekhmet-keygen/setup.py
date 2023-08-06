from setuptools import setup

setup(name='sekhmetkeygen',
    version='1.0.0',
    description='sekhmet key generation python tool',
    url='https://rndwww.nce.amadeus.net/git/scm/apsc/sekhmet-keygen.git',
    author='Hardev Singh Rajpoot',
    author_email='hardevsingh.rajpoot@amadeus.com',
    packages=['sekhmet-keygen'],
    install_requires=[
     "requests",
     "pyopenssl"
    ])
