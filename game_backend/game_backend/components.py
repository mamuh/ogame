#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import Dict, List

from dataclasses_jsonschema import JsonSchemaMixin

from game_backend.ecs.component import Component
from game_backend.resources import Resources


@dataclass
class BuildingComponent(Component, JsonSchemaMixin):
    name: str
    base_cost: Dict[Resources, float]
    upgrade_cost_factor: float
    upgrade_prod_factor: float = 1
    level: int = 0


@dataclass
class ProducerComponent(Component, JsonSchemaMixin):
    production_rate: Dict[Resources, float]
    energy_consumption: int
    energy_production: int = 0


@dataclass
class PlanetComponent(Component, JsonSchemaMixin):
    name: str
    size: int
    owner_id: str
    resources: Dict[Resources, float] = field(
        default_factory=lambda: {resource: 0.0 for resource in Resources}
    )


@dataclass
class PlayerComponent(Component, JsonSchemaMixin):
    name: str
    id: str
