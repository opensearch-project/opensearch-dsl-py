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

import nox

SOURCE_FILES = (
    "setup.py",
    "noxfile.py",
    "opensearch_dsl/",
    "tests/",
    "utils/",
)


@nox.session(python=["2.7", "3.4", "3.5", "3.6", "3.7", "3.8", "3.9"])
def test(session):
    session.install(".[develop]")

    if session.posargs:
        argv = session.posargs
    else:
        argv = (
            "-vvv",
            "--cov=opensearch_dsl",
            "tests/",
        )
    session.run("pytest", *argv)


@nox.session()
def format(session):
    session.install("black", "isort")
    session.run(
        "black",
        "--skip-string-normalization",
        "--target-version=py33",
        "--target-version=py37",
        *SOURCE_FILES
    )
    session.run("isort", *SOURCE_FILES)
    session.run("python", "utils/license-headers.py", "fix", *SOURCE_FILES)

    lint(session)


@nox.session
def lint(session):
    session.install("flake8", "black", "isort")
    session.run(
        "black",
        "--check",
        "--skip-string-normalization",
        "--target-version=py33",
        "--target-version=py37",
        *SOURCE_FILES
    )
    session.run("isort", "--check", *SOURCE_FILES)
    session.run("flake8", "--ignore=E501,E741,W503", *SOURCE_FILES)
    session.run("python", "utils/license-headers.py", "check", *SOURCE_FILES)
