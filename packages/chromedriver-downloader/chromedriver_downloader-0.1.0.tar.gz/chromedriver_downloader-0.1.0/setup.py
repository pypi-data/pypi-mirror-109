#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt', 'r') as f:
    requirements = [x for x in f.read().split('\n') if x.strip()]

with open('requirements_test.txt', 'r') as f:
    test_requirements = [x for x in f.read().split('\n') if x.strip()]

setup(
    author="Marcos Lima",
    author_email='marcos.j.s.lima@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: Portuguese',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Downloader for chromedriver",
    install_requires=requirements,
    license="Apache Software License 2.0",
    # long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='chromedriver_downloader',
    name='chromedriver_downloader',
    packages=find_packages(include=['chromedriver_downloader',
                                    'chromedriver_downloader.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/marcoslima/chromedriver_downloader',
    version='0.1.0',
    zip_safe=False,
)
