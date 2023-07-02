from setuptools import setup, find_packages

setup(
    name='auria',
    version='0.0.1',
    author='N.i.d.a.l',
    description='Auria package',
    packages=find_packages(),
    install_requires=[
        'flask',
        'sqlalchemy',
        'pymysql',
        'jsonschema',
        'pycryptodome',
        'requests',
        'pillow',
        'firebase_admin'
    ],
)