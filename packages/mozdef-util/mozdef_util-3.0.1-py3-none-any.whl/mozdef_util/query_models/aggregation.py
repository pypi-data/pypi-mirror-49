#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Copyright (c) 2017 Mozilla Corporation


from elasticsearch_dsl import A


def Aggregation(field_name, aggregation_size=20):
    return A('terms', field=field_name, size=aggregation_size)
