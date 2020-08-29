#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import Dict, List

from dataclasses_jsonschema import JsonSchemaMixin

from game_backend.ecs.component import Component
from game_backend.resources import Resources


@dataclass
class BuildingComponent(Component, JsonSchemaMixin):
    name: str
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
    owner_id: str


@dataclass
class PlayerComponent(Component, JsonSchemaMixin):
    name: str
    id: str
    resources: Dict[Resources, float] = field(
        default_factory=lambda: {resource: 0.0 for resource in Resources}
    )
