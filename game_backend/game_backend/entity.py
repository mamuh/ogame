#!/usr/bin/env python3
from uuid import uuid4

from dataclasses import dataclass
from dataclasses_jsonschema import JsonSchemaMixin


@dataclass
class Entity(JsonSchemaMixin):
    name: str
    id: str = None

    def __post_init__(self):
        self.id: str = self.id or str(uuid4())
        EntityCatalog.register(self)


class EntityCatalog:
    def __init__(self):
        self.entities: Dict[str, Entity] = {}

    def register(self, entity: Entity):
        if entity.id not in self.entities:
            self.entities[entity.id] = entity
        else:
            raise Exception(f"An entity with this id already exists in the catalog")


EntityCatalog = EntityCatalog()