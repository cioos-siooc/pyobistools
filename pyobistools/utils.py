#!/usr/bin/env python
# coding=utf-8


def removesuffix(obj: str, suffix: str) -> str:
    # https://peps.python.org/pep-0616/
    if suffix and obj.endswith(suffix):
        return obj[:-len(suffix)]
    else:
        return obj[:]
