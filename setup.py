#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='pyoptionchain',
    version="1.1",
    description="Google Option Chain + Tk + Pandas DataFrame",
    author='Ferdinand Silva',
    author_email='ferdinandsilva@ferdinandsilva.com',
    packages=['pyoptionchain'],
    install_requires=['requests', 'demjson', 'pandas', 'xlwt'],
    url='http://ferdinandsilva.com',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'License :: Freeware',
    ),
    entry_points = {
        'console_scripts': [
            'pyoptionchain = pyoptionchain.commands:pyoptionchain']
    },
    download_url='http://ferdinandsilva.com',
)