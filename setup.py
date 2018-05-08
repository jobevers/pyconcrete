#!/usr/bin/env python
#
# Copyright 2015 Falldog Hsieh <falldog7@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import imp
import hashlib
import sysconfig
from os.path import join
from distutils.core import setup, Extension, Command
from distutils.dist import Distribution
from distutils.command.build import build
from distutils.command.build_ext import build_ext
from distutils.command.install import install
from src.config import DEFAULT_KEY, TEST_DIR, SRC_DIR, PY_SRC_DIR, EXT_SRC_DIR, EXE_SRC_DIR, SECRET_HEADER_PATH

version_mod = imp.load_source('version', join(PY_SRC_DIR, 'version.py'))
version = version_mod.__version__

PY2 = sys.version_info[0] < 3


# .rst should created by pyconcrete-admin
if os.path.exists('README.rst'):
    readme_path = 'README.rst'
else:
    readme_path = 'README.md'
with open(readme_path, 'r') as f:
    readme = f.read()


setup(
    name='pyconcrete',
    version=version,
    description='Protect your python script, encrypt it as .pye and decrypt when import it',
    long_description=readme,
    keywords='python source encryption obfuscation',
    author='Falldog',
    author_email='falldog7@gmail.com',
    url='https://github.com/Falldog/pyconcrete',
    license="Apache License 2.0",
    scripts=[
        'pyconcrete-admin.py',
    ],
    packages=[
        'pyconcrete',
    ],
    package_dir={
        '': SRC_DIR,
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: Apache Software License',
    ]
)
