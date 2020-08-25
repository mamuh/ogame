#!/usr/bin/env python3

from dataclasses import dataclass
from typing import List, Dict
from enum import Enum

from dataclasses_jsonschema import JsonSchemaMixin


class Resources(Enum):
    Metal = 0


@dataclass
class Component(JsonSchemaMixin):
    pass


@dataclass
class UpgradableComponent(Component, JsonSchemaMixin):
    base_cost: float
    upgrade_cost_factor: float


@dataclass
class ProducerComponent(Component, JsonSchemaMixin):
    production_rate: Dict[Resources, float]


@dataclass
class Building(JsonSchemaMixin):
    pass


@dataclass
class Mine(Building, JsonSchemaMixin):
    producer_component: ProducerComponent
    upgradable_component: UpgradableComponent


@dataclass
class Factory(Building, JsonSchemaMixin):
    pass


@dataclass
class Cannon(Building, JsonSchemaMixin):
    pass


@dataclass
class Planet(JsonSchemaMixin):
    id: str
    name: str
    size: int
    buildings: List[Building]


@dataclass
class World(JsonSchemaMixin):
    planets: Dict[str, Planet]


@dataclass
class Player(JsonSchemaMixin):
    id: str
    name: str


@dataclass
class GameState(JsonSchemaMixin):
    world: World
    players: Dict[str, Player]
