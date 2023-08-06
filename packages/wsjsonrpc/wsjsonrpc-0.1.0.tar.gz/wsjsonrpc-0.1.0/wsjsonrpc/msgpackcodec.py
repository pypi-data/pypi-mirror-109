#!/usr/bin/env python
"""Serialize/deserialize messages using u-msgpack-python."""


import umsgpack


is_binary = True


serialize = umsgpack.packb


def deserialize(data):
    """Deserialize msgpack serialized object."""
    return umsgpack.unpackb(data, use_tuple=True, use_ordered_dict=True)
