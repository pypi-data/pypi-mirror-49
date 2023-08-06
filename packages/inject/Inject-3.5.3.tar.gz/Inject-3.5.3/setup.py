# encoding: utf-8
import sys

from setuptools import setup


def read_description():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='Inject',
    version='3.5.3',
    url='https://github.com/ivankorobkov/python-inject',
    license='Apache License 2.0',

    author='Ivan Korobkov',
    author_email='ivan.korobkov@gmail.com',

    description='Python dependency injection framework',
    long_description=read_description(),
    long_description_content_type="text/markdown",

    package_dir={'': 'src'},
    py_modules=['inject'],
    data_files=[
        (
            'lib/python{}.{}/site-packages'.format(*sys.version_info[:2]),
            ['src/inject.py']
        )
    ],

    install_requires=['typing; python_version<"3.5"'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules']
)
