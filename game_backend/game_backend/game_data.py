#!/usr/bin/env python3

from dataclasses import dataclass
from game_backend.entity import Entity
from game_backend.components import (
    ProducerComponent,
    BuildingComponent,
    PlanetComponent,
)
from game_backend.resources import Resources


@dataclass
class Mine(Entity):
    name: str = "Mine"
    producer_component: ProducerComponent = ProducerComponent(
        production_rate={Resources.Metal: 1}
    )
    building_component: BuildingComponent = BuildingComponent(
        base_cost=100, upgrade_cost_factor=1.1
    )


@dataclass
class OilRig(Entity):
    name: str = "Oil Rig"
    producer_component: ProducerComponent = ProducerComponent(
        production_rate={Resources.Oil: 0.01}
    )
    building_component: BuildingComponent = BuildingComponent(
        base_cost=200, upgrade_cost_factor=1.2
    )


@dataclass
class Planet(Entity):
    name: str = "Planet"
    planet_component: PlanetComponent = None
