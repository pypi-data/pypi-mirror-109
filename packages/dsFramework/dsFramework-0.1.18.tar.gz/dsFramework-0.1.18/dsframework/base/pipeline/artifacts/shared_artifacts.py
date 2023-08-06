#!/usr/bin/env python
# coding: utf-8

from typing import List, Any

class ZIDS_SharedArtifacts():

    def __init__(self) -> None:
        pass

    def get(self, key, default=None):
        if key in self.__dict__:
            return self.__dict__[key]
        return default