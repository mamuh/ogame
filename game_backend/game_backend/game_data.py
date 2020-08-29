#!/usr/bin/env python3

from dataclasses import dataclass
from game_backend.entities import Building
from game_backend.components import (
    ProducerComponent,
    BuildingComponent,
    PlanetComponent,
)
from game_backend.resources import Resources


def Mine() -> Building:
    return Building(
        components={
            ProducerComponent: ProducerComponent(production_rate={Resources.Metal: 1}),
            BuildingComponent: BuildingComponent(
                name="Mine", base_cost=100, upgrade_cost_factor=1.1
            ),
        }
    )


def OilRig() -> Building:
    return Building(
        components={
            ProducerComponent: ProducerComponent(production_rate={Resources.Oil: 0.01}),
            BuildingComponent: BuildingComponent(
                name="OilRig", base_cost=200, upgrade_cost_factor=1.2
            ),
        }
    )
