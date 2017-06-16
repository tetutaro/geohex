#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from setuptools import setup, find_packages
import geohex


def setup_package():
	metadata = dict()
	metadata['name'] = geohex.__package__
	metadata['version'] = geohex.__version__
	metadata['description'] = geohex.description_
	metadata['author'] = geohex.author_
	metadata['url'] = geohex.url_
	metadata['license'] = 'MIT'
	metadata['packages'] = find_packages()
	metadata['include_package_data'] = False
	metadata['setup_requires'] = ['pytest-runner']
	metadata['tests_require'] = ['pytest']
	setup(**metadata)


if __name__ == "__main__":
	setup_package()
