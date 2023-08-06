#!/usr/bin/env python
"""Serialize/deserialize messages using JSON."""


import json


is_binary = False


def serialize(data):
    """Return utf-8 encoded json serialized data."""
    return json.dumps(data).encode("utf-8")


deserialize = json.loads
