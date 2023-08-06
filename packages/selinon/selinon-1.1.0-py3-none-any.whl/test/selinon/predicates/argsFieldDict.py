#!/bin/env python3
# pragma: no cover

from functools import reduce


def argsFieldDict(node_args, key):
    try:
        val = reduce(lambda m, k: m[k], key if isinstance(key, list) else [key], node_args)
        return isinstance(val, dict)
    except:
        return False
