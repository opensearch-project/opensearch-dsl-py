# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

from elasticsearch.serializer import JSONSerializer

from .utils import AttrList


class AttrJSONSerializer(JSONSerializer):
    def default(self, data):
        if isinstance(data, AttrList):
            return data._l_
        if hasattr(data, "to_dict"):
            return data.to_dict()
        return super(AttrJSONSerializer, self).default(data)


serializer = AttrJSONSerializer()
