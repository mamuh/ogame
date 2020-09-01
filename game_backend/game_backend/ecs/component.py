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

    def serialise(self):
        initial_dict = self.to_dict()

        additional_properties = {}
        for attr_name, attr in self.__class__.__dict__.items():
            if attr_name == "entity":
                continue
            if isinstance(attr, property):
                additional_properties[attr_name] = getattr(self, attr_name)

        return {**initial_dict, **additional_properties}
