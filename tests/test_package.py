# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import opensearch_dsl


def test__all__is_sorted():
    assert opensearch_dsl.__all__ == sorted(opensearch_dsl.__all__)
