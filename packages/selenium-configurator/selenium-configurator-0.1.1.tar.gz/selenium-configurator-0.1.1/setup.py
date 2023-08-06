# -*- coding: utf-8 -*-
import io
from setuptools import setup


def parse_requirements(file):
    required = []
    with open(file) as f:
        for req in f.read().splitlines():
            if not req.strip().startswith('#'):
                required.append(req)
    return required


def read(*args, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in args:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


requires = parse_requirements('requirements.txt')
long_description = read('README.rst', 'CHANGES.rst')
LGPLv3 = 'License :: OSI Approved :: GNU Lesser General Public License v3 or' \
         ' later (LGPLv3+)'

setup(
    name='selenium-configurator',
    version='0.1.1',
    description='Helper API to define multiple webdrivers in config files.',
    long_description=long_description,
    author='Pierre Verkest',
    author_email='pverkest@anybox.fr',
    url='https://github.com/anybox/selenium-configurator',
    packages=[
        'selenium_configurator',
        'selenium_configurator.drivers'
    ],
    install_requires=requires,
    tests_require=requires + ['nose'],
    license='LGPL-3.0',
    keywords='nose selenium CI',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        LGPLv3,
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.7',
    ]
)
