#!/usr/bin/env python3

from dataclasses import dataclass
from abc import ABC

from dataclasses_jsonschema import JsonSchemaMixin


@dataclass
class Component(ABC, JsonSchemaMixin):
    @property
    def entity(self):
        # HACK
        from game_backend.ecs.entity import EntityCatalog

        return EntityCatalog.entities_index[self._entity_id]
