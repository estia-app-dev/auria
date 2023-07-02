from setuptools import setup, find_packages

setup(
    name='auria',
    version='0.0.2',
    author='N.i.d.a.l',
    description='Auria package',
    packages=find_packages(),
    install_requires=[
        'flask',
        'sqlalchemy'
    ],
)