# -*- coding: utf-8 -*-

import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# root path
ROOT = os.path.dirname(os.path.realpath(__file__))

# README
with open(os.path.join(ROOT, 'README.md'), encoding='utf-8') as file:
    long_desc = file.read()

# version string
__version__ = '0.7.3'

# set-up script for pip distribution
setup(
    name='f2format',
    version=__version__,
    author='Jarry Shaw',
    author_email='jarryshaw@icloud.com',
    url='https://github.com/JarryShaw/f2format',
    license='Apache Software License',
    keywords='fstring format conversion',
    description='Back-port compiler for Python 3.6 f-string literals.',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    python_requires='>=3.3',
    # include_package_data=True,
    zip_safe=True,
    install_requires=[
        'parso~=0.5.0',     # universal AST support
        'tbtrim>=0.2.1',    # traceback trim support
    ],
    py_modules=['f2format'],
    # packages=[
    #     'f2format',
    # ],
    entry_points={
        'console_scripts': [
            # 'f2format = f2format.__main__:main',
            'f2format = f2format:main',
        ]
    },
    package_data={
        '': [
            'LICENSE',
            'README.md',
            'CHANGELOG.md',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ]
)
