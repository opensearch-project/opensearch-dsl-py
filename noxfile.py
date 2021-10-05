# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

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
        "black", "--target-version=py27", "--target-version=py37", *SOURCE_FILES
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
        "--target-version=py27",
        "--target-version=py37",
        *SOURCE_FILES
    )
    session.run("isort", "--check", *SOURCE_FILES)
    session.run("flake8", "--ignore=E501,E741,W503", *SOURCE_FILES)
    session.run("python", "utils/license-headers.py", "check", *SOURCE_FILES)
