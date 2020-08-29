#!/usr/bin/env python3
from uuid import uuid4
from dataclasses import dataclass
from typing import Dict, List

from dataclasses_jsonschema import JsonSchemaMixin

from game_backend.resources import Resources
from game_backend.entity import EntityCatalog


@dataclass
class Component(JsonSchemaMixin):
    def __post_init__(self):
        self.entity_id = self.entity_id if hasattr(self, "entity_id") else ""
        self.id: str = str(uuid4())
        ComponentCatalog.register(self)

    @property
    def entity(self):
        return EntityCatalog.entities.get(self.entity_id)


@dataclass
class BuildingComponent(Component, JsonSchemaMixin):
    base_cost: float
    upgrade_cost_factor: float
    level: int = 0


@dataclass
class ProducerComponent(Component, JsonSchemaMixin):
    production_rate: Dict[Resources, float]


@dataclass
class PlanetComponent(Component, JsonSchemaMixin):
    name: str
    size: int
    building_ids: List[str]
    owner_id: str


class ComponentCatalog:
    def __init__(self):
        self.components: Dict[str, Component] = {}

    def register(self, component: Component):
        self.components[component.id] = component


ComponentCatalog = ComponentCatalog()
