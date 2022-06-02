# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
#
#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

from os.path import dirname, join

from setuptools import find_packages, setup

VERSION = (2, 0, 1)
__version__ = VERSION
__versionstr__ = ".".join(map(str, VERSION))

f = open(join(dirname(__file__), "README.md"))
long_description = f.read().strip()
f.close()

install_requires = [
    "six",
    "python-dateutil",
    "opensearch-py>=2.0.0",
    # ipaddress is included in stdlib since python 3.3
    'ipaddress; python_version<"3.3"',
]

develop_requires = [
    "mock",
    "pytest>=3.0.0",
    "pytest-cov",
    "pytest-mock<3.0.0",
    "pytz",
    "coverage<5.0.0",
    "sphinx",
    "sphinx_rtd_theme",
]

setup(
    name="opensearch-dsl",
    description="Python client for OpenSearch",
    license="Apache-2.0",
    url="https://github.com/opensearch-project/opensearch-dsl-py",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=__versionstr__,
    author="Honza Král, Guian Gumpac",
    author_email="honza.kral@gmail.com, guiang@bitquilltech.com",
    maintainer="Charlene Solonynka, Yury Fridlyand, Guian Gumpac",
    maintainer_email="charlenes@bitquilltech.com, yuryf@bitquilltech.com, guiang@bitquilltech.com",
    packages=find_packages(where=".", exclude=("tests*",)),
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    install_requires=install_requires,
    extras_require={"develop": develop_requires},
)
