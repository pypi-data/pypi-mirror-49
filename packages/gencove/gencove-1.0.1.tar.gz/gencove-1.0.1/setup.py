from setuptools import setup

import version

setup(
    name='gencove',
    description='Gencove API and CLI tool',
    url='http://docs.gencove.com',
    author='Tomaz Berisa',
    email='tomaz.berisa@gmail.com',
    licence='Apache 2.0',
    version=version.version(),
    packages=['gencove'],
    install_requires=[
        'Click>=7.0',
        'requests>=2.19.1',
        'PyJWT>=1.6.4',
        'awscli>=1.16.96'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest<5.0.0',
        'responses'
    ],
    entry_points='''
        [console_scripts]
        gencove=gencove.cli:cli
    ''',
    package_data={
        'gencove': ['version/*'],
    }
)
