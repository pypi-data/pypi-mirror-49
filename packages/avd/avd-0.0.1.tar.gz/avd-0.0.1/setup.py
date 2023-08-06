# encoding: utf-8

import pip

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = [
    'avd',
]


def get_reqs():
    kwargs = {'session': 'fake session'}
    install_reqs = pip.req.parse_requirements('requirements.pip', **kwargs)
    return [str(ir.req) for ir in install_reqs]


setup(
    name='avd',
    version='0.0.1',
    url="http://avd.apsara9.com",
    description='Apsara vulnerability database library',
    long_description=open('README.md').read(),
    author="Apsara9 Team",
    author_email = "avd@apsara9.com",
    packages=packages,
    install_requires=get_reqs(),
)
