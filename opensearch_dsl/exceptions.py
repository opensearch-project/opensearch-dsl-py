# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


class OpenSearchDslException(Exception):
    pass


class UnknownDslObject(OpenSearchDslException):
    pass


class ValidationException(ValueError, OpenSearchDslException):
    pass


class IllegalOperation(OpenSearchDslException):
    pass
