#!/usr/bin/env python3
# pragma: no cover

from functools import reduce
from urllib.parse import urlparse


def fieldUrlScheme(message, key, scheme):
    try:
        val = reduce(lambda m, k: m[k], key if isinstance(key, list) else [key], message)
        return urlparse(val).scheme == scheme
    except:
        return False
