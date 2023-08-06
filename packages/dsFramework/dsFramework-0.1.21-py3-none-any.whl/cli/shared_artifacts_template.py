#!/usr/bin/env python
# coding: utf-8

import json
from dsFramework.base.pipeline.artifacts.shared_artifacts import ZIDS_SharedArtifacts

class generatedClass(ZIDS_SharedArtifacts):

    def __init__(self) -> None:
        super().__init__()
        self.load_config()

    def load_config(self):
        f = open('config.json', )
        data = json.load(f)
        for item in data:
            setattr(self, item, data[item])
